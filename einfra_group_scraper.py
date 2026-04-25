import requests
from bs4 import BeautifulSoup
from solr_connection import get_solr_connection

def scrape_einfra_group():
    url = "https://electrogrup.applytojob.com/apply/jobs/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    jobs = []
    
    # Mapping of headers to company names in our system
    company_mapping = {
        "Direct One": "DIRECT ONE SA",
        "E-INFRA": "E-INFRA S.A.",
        "EINFRA": "E-INFRA S.A.",
        "IT": "E-INFRA S.A.",
        "ELECTROGRUP": "ELECTROGRUP SA",
        "Electrogrup SA": "ELECTROGRUP SA",
        "ELECTROGRUP SA": "ELECTROGRUP SA",
        "NOVA Power&Gas": "NOVA POWER & GAS S.A.",
        "Nova Power & Gas": "NOVA POWER & GAS S.A.",
        "Netcity": "NETCITY TELECOM S.A.",
        "WESEE": "WIND ENERGY SERVICE EAST EUROPE SRL"
    }

    current_company = None
    processed_urls = set()
    
    container = soup.find('div', class_='resumator-job-list')
    if not container:
        container = soup.body

    for element in container.find_all(['h3', 'tr', 'div']):
        if element.name == 'h3':
            header_text = element.get_text(strip=True)
            if header_text in company_mapping:
                current_company = company_mapping[header_text]
            else:
                current_company = "ELECTROGRUP SA" 
            
        elif current_company and ('row_job' in element.get('id', '') or element.find('a', class_='job_title_link')):
            link_tag = element.find('a', class_='job_title_link')
            if link_tag:
                title = link_tag.get_text(strip=True)
                link = "https://electrogrup.applytojob.com" + link_tag.get('href')
                
                if link in processed_urls:
                    continue
                processed_urls.add(link)
                
                location = "Romania" 
                loc_tag = element.find('span', class_='resumator_description')
                if loc_tag and "Location:" in loc_tag.get_text():
                    location = loc_tag.get_text().replace("Location:", "").strip()
                elif element.name == 'tr':
                    tds = element.find_all('td')
                    if len(tds) > 1:
                        location = tds[1].get_text(strip=True)
                
                city = "Romania"
                country = "Romania"
                if ',' in location:
                    parts = location.split(',')
                    city = parts[0].strip()
                    country = parts[1].strip()
                else:
                    city = location
                
                location_list = [city]
                
                jobs.append({
                    "title": title,
                    "url": link,
                    "company": current_company,
                    "location": location_list,
                    "country": ["Romania"],
                    "status": "published"
                })

    return jobs

def publish_jobs(jobs):
    solr = get_solr_connection("job")
    print(f"Publishing {len(jobs)} jobs to Solr...")
    
    summary = {}
    for job in jobs:
        c = job['company']
        summary[c] = summary.get(c, 0) + 1
    
    for c, count in summary.items():
        print(f"  - {c}: {count}")
        
    solr.add(jobs)
    print("Done.")

if __name__ == "__main__":
    jobs = scrape_einfra_group()
    if jobs:
        print(f"Found {len(jobs)} jobs.")
        publish_jobs(jobs)
    else:
        print("No jobs found.")
