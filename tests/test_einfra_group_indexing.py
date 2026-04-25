import unittest
from solr_connection import get_solr_connection

class TestEInfraGroupIndexing(unittest.TestCase):
    def setUp(self):
        self.solr_company = get_solr_connection("company")
        self.solr_job = get_solr_connection("job")
        
        self.expected_companies = [
            "E-INFRA S.A.",
            "ELECTROGRUP SA",
            "NOVA POWER & GAS S.A.",
            "NETCITY TELECOM S.A.",
            "DIRECT ONE SA",
            "WIND ENERGY SERVICE EAST EUROPE SRL"
        ]

    def test_companies_indexed(self):
        results = self.solr_company.search('group:"E-INFRA"', rows=10)
        found_names = [doc['company'] for doc in results.docs]
        
        for name in self.expected_companies:
            with self.subTest(company=name):
                self.assertIn(name, found_names, f"{name} should be indexed in the E-INFRA group")

    def test_jobs_indexed(self):
        active_companies = [
            "E-INFRA S.A.",
            "ELECTROGRUP SA",
            "NOVA POWER & GAS S.A.",
            "DIRECT ONE SA"
        ]
        
        for company in active_companies:
            with self.subTest(company=company):
                query = f'company:"{company}"'
                results = self.solr_job.search(query, rows=0)
                self.assertGreater(results.hits, 0, f"Company {company} should have at least one job indexed")

if __name__ == "__main__":
    unittest.main()
