import pytest
import os
import requests
from solr_connection import get_solr_connection, SOLR_BASE_URL, SOLR_USER, SOLR_PASS

def test_random_job_extraction():
    """Test that we can connect to 'job' core and fetch a random document."""
    core = "job"
    solr = get_solr_connection(core)
    
    results = solr.search('*:*', rows=1)
    
    assert len(results) > 0, f"No documents found in core '{core}'"
    job = results.docs[0]
    # In the 'job' core, the unique key is 'url'
    print(f"\n[Random Job] URL (UniqueKey): {job.get('url')}")
    print(f"Title: {job.get('title')}")
    assert 'url' in job

def test_company_field_extraction():
    """Test that we can connect to 'company' core and see the fields of a document."""
    core = "company"
    solr = get_solr_connection(core)
    
    results = solr.search('*:*', rows=1)
    
    assert len(results) > 0, f"No documents found in core '{core}'"
    company = results.docs[0]
    print(f"\n[Company Fields] Keys found: {list(company.keys())}")
    print(f"Sample Company: {company.get('company') or company.get('name')}")

def test_extract_solr_schema():
    """Fetch the actual schema fields from Solr for both cores."""
    for core in ["job", "company"]:
        print(f"\n--- Full Schema for core: {core} ---")
        url = f"{SOLR_BASE_URL}/{core}/schema/fields"
        response = requests.get(url, auth=(SOLR_USER, SOLR_PASS))
        
        if response.status_code == 200:
            fields = response.json().get('fields', [])
            field_names = sorted([f['name'] for f in fields if not f['name'].startswith('_')])
            print(f"Fields in Solr: {field_names}")
        else:
            print(f"❌ Failed to fetch schema for {core}: {response.status_code}")

def test_schema_vs_readme_models():
    """Compare Solr schema fields with models defined in readme.md."""
    models = {
        "job": ["url", "title", "company", "cif", "location", "tags", "workmode", "date", "status", "vdate", "expirationdate", "salary"],
        "company": ["id", "company", "brand", "group", "status", "location", "website", "career", "lastScraped", "scraperFile"]
    }
    
    for core, expected_fields in models.items():
        print(f"\n[Validation] Checking {core} core schema against README...")
        url = f"{SOLR_BASE_URL}/{core}/schema/fields"
        response = requests.get(url, auth=(SOLR_USER, SOLR_PASS))
        
        if response.status_code == 200:
            actual_fields = [f['name'] for f in response.json().get('fields', [])]
            missing = [f for f in expected_fields if f not in actual_fields]
            
            if missing:
                print(f"⚠️ Missing fields in {core} core: {missing}")
            else:
                print(f"✅ All expected fields found in {core} core.")
        else:
            print(f"❌ Could not fetch schema for {core}")

if __name__ == "__main__":
    test_random_job_extraction()
    test_company_field_extraction()
    test_extract_solr_schema()
    test_schema_vs_readme_models()
