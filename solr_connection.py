import os
import pysolr
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

# Load credentials from .env.local
load_dotenv(".env.local")

# --- Configuration ---
SOLR_BASE_URL = 'https://solr.peviitor.ro/solr'
SOLR_USER = os.getenv("SOLR_USER")
SOLR_PASS = os.getenv("SOLR_PASS")

def get_solr_connection(core_name):
    """
    Establishes a connection to a specific Solr core using credentials from .env.local
    """
    if not SOLR_USER or not SOLR_PASS:
        raise ValueError("SOLR_USER and SOLR_PASS must be set in .env.local")

    url = f"{SOLR_BASE_URL}/{core_name}"
    auth = HTTPBasicAuth(SOLR_USER, SOLR_PASS)
    
    solr = pysolr.Solr(url, always_commit=True, auth=auth)
    return solr

def safe_update(solr_client, unique_key_field, unique_key_value, updates):
    """
    Safely updates a document by fetching the entire record first,
    merging updates, and re-pushing the full document.
    """
    query = f'{unique_key_field}:"{unique_key_value}"'
    results = solr_client.search(query)
    
    if not results:
        full_doc = updates
        full_doc[unique_key_field] = unique_key_value
    else:
        full_doc = results.docs[0]
        full_doc.update(updates)
        
        full_doc.pop('_version_', None)
        full_doc.pop('score', None)

    solr_client.add([full_doc])
    return full_doc

if __name__ == "__main__":
    try:
        core = os.getenv("SOLR_JOB_CORE", "job")
        solr = get_solr_connection(core)
        solr.ping()
        print(f"Successfully connected to the '{core}' core!")
        results = solr.search('*:*', rows=1)
        if results:
            print(f"Successfully retrieved data from Solr. Found {results.hits} documents.")
    except Exception as e:
        print(f"Error: {e}")
