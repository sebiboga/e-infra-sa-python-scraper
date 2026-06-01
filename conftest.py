import os
import pytest

def pytest_configure(config):
    config.addinivalue_line(
        "markers",
        "solr: mark test as requiring SOLR credentials (SOLR_USER and SOLR_PASS)"
    )

def pytest_collection_modifyitems(config, items):
    skip_solr = pytest.mark.skip(reason="SOLR_USER or SOLR_PASS not set — set .env.local")
    for item in items:
        if "solr" in item.keywords:
            if not os.getenv("SOLR_USER") or not os.getenv("SOLR_PASS"):
                item.add_marker(skip_solr)
