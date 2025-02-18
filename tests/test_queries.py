import unittest
from api.queries import (
    get_vulnerabilities_by_cve_id,
    get_total_vulnerabilities_count,
    get_vulnerabilities_by_product_id,
    get_all_vulnerabilities,
    get_metrics_by_id,
)

class TestQueries(unittest.TestCase):
    
    def test_get_vulnerabilities_by_cve_id(self):
        """Test SQL query for retrieving vulnerabilities by CVE ID."""
        query = get_vulnerabilities_by_cve_id('CVE-2023-1234')
        self.assertIn("WHERE cve_id = %s", query)
        self.assertIn("LIMIT 10", query)
    
    def test_get_total_vulnerabilities_count(self):
        """Test SQL query for retrieving total vulnerability count."""
        query = get_total_vulnerabilities_count()
        self.assertIn("SELECT COUNT(*)", query)
        self.assertIn("FROM cve_entries", query)
    
    def test_get_vulnerabilities_by_product_id(self):
        """Test SQL query for retrieving vulnerabilities by product ID."""
        query = get_vulnerabilities_by_product_id(1)
        self.assertIn("WHERE products.id = %s", query)
        self.assertIn("LIMIT 10", query)
    
    def test_get_all_vulnerabilities(self):
        """Test SQL query for retrieving all vulnerabilities with pagination."""
        query = get_all_vulnerabilities(2, 50, 50)
        self.assertIn("LIMIT 50 OFFSET", query)
        self.assertIn("FROM cve_entries", query)
    
    def test_invalid_rows_raises_error(self):
        """Test invalid row values raise an error."""
        with self.assertRaises(ValueError):
            get_all_vulnerabilities(1, 10, 5)
    
    def test_get_metrics_by_id(self):
        """Test SQL query for retrieving metrics by ID."""
        query = get_metrics_by_id(1)
        self.assertIn("WHERE id = %s", query)

if __name__ == '__main__':
    unittest.main()
