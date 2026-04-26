#!/usr/bin/env python3
"""
E-INFRA Group Job Validator - Check and remove expired jobs
Run: python tests/validate_einfra_jobs.py --dry-run | --delete
"""

import requests
import json
import sys
import time
import base64

SOLR_URL = "https://solr.peviitor.ro/solr/job/update"
SOLR_AUTH = "solr:SolrRocks"
COMPANIES = ["E-INFRA S.A.", "ELECTROGRUP SA", "NETCITY TELECOM S.A.", "NOVA POWER & GAS S.A.", "DIRECT ONE SA", "WIND ENERGY SERVICE EAST EUROPE SRL"]

def get_jobs(company_name):
    jobs = []
    page = 1
    while True:
        url = f"https://api.peviitor.ro/v1/search/?company={company_name}&page={page}"
        res = requests.get(url, headers={"origin": "https://peviitor.ro", "referer": "https://peviitor.ro/"})
        data = res.json()
        if not data.get("response", {}).get("docs"):
            break
        jobs.extend(data["response"]["docs"])
        page += 1
    return jobs

def check_url(url):
    try:
        # Use GET instead of HEAD to get full content for checking
        res = requests.get(url, allow_redirects=True, timeout=10)
        
        # Check for expired content
        text = res.text.lower()
        expired_indicators = ['nu mai este disponibil', 'acest anunt', 'nu mai este activ', 'expired', '404', 'this job is no longer available']
        
        is_expired = any(indicator in text for indicator in expired_indicators)
        
        return {"status": res.status_code, "ok": not is_expired, "expired": is_expired}
    except Exception as e:
        return {"status": 0, "ok": False, "error": str(e)}

def delete_job(url):
    auth = base64.b64encode(SOLR_AUTH.encode()).decode()
    params = {"commit": "true"}
    delete_query = json.dumps({"delete": {"query": f'url:"{url}'}})
    res = requests.post(
        SOLR_URL,
        params=params,
        headers={
            "Authorization": "Basic " + auth,
            "Content-Type": "application/json"
        },
        data=delete_query
    )
    return res.ok

def main():
    dry_run = "--dry-run" in sys.argv or "--delete" not in sys.argv
    
    mode = "DRY RUN (no changes)" if dry_run else "LIVE (will delete expired)"
    print("=" * 50)
    print("E-INFRA Group Job Validator")
    print("=" * 50)
    print(f"Mode: {mode}\n")
    
    total_active = 0
    total_expired = 0
    
    for company in COMPANIES:
        jobs = get_jobs(company)
        print(f"\n--- {company}: {len(jobs)} jobs ---\n")
        
        if not jobs:
            continue
            
        expired_jobs = []
        
        for job in jobs:
            result = check_url(job["url"])
            
            if result.get("expired"):
                print(f"❌ EXPIRED - {job['job_title'][:40]}")
                print(f"   URL: {job['url']}")
                expired_jobs.append(job)
                total_expired += 1
            elif result["ok"]:
                print(f"✅ {job['job_title'][:50]}")
                total_active += 1
            elif result["status"] in [404, 0]:
                print(f"❌ EXPIRED ({result['status']}) - {job['job_title'][:40]}")
                print(f"   URL: {job['url']}")
                expired_jobs.append(job)
                total_expired += 1
            else:
                print(f"⚠️ STATUS {result['status']} - {job['job_title'][:40]}")
            
            time.sleep(0.3)
        
        if expired_jobs and not dry_run:
            print(f"\nDeleting {len(expired_jobs)} expired jobs...")
            for job in expired_jobs:
                ok = delete_job(job["url"])
                print(f"{'✅' if ok else '❌'} {'Deleted' if ok else 'Failed'}: {job['job_title']}")
                time.sleep(0.5)
    
    print("\n" + "=" * 50)
    print("RESULTS")
    print("=" * 50)
    print(f"Active: {total_active}")
    print(f"Expired: {total_expired}")
    
    if dry_run:
        print("\n⚠️ Dry run - no jobs deleted. Run with --delete to actually remove.")

if __name__ == "__main__":
    main()