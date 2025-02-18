import unittest
from unittest.mock import patch, MagicMock
from api.routes import register_routes  
from api.db import query_db

class TestRoutes(unittest.TestCase):
    def setUp(self):
        """Set up a test client for the Flask app."""
        self.app = app.test_client()
        self.app.testing = True

    @patch('api.routes.render_template')
    def test_homepage(self, mock_render_template):
        """Test the homepage route."""
        mock_render_template.return_value = "Mocked HTML Page"
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b"Mocked HTML Page")

    @patch('api.routes.query_db')
    def test_get_vulnerabilities(self, mock_query_db):
        """Test the /cves/list route with valid parameters."""
        mock_query_db.side_effect = [
            [{'total': 100}],  # Mock total count query
            [{'id': 1, 'cve_id': 'CVE-2024-0001', 'description': 'Test CVE'}]  # Mock data query
        ]
        response = self.app.get('/cves/list?page=1&rows=10')
        self.assertEqual(response.status_code, 200)
        self.assertIn('total_pages', response.json)
        self.assertEqual(response.json['total_pages'], 10)
        self.assertEqual(len(response.json['data']), 1)

    @patch('api.routes.query_db')
    def test_get_vulnerabilities_invalid_rows(self, mock_query_db):
        """Test the /cves/list route with an invalid rows parameter."""
        response = self.app.get('/cves/list?page=1&rows=25')
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid number of rows', response.json['message'])

    @patch('api.routes.query_db')
    def test_get_metrics_by_id(self, mock_query_db):
        """Test the /cves/id/<int:id> route with a valid ID."""
        mock_query_db.return_value = [{'id': 1, 'cvss_score': 9.8}]
        response = self.app.get('/cves/id/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn('cvss_score', response.json[0])

    @patch('api.routes.query_db')
    def test_get_metrics_by_id_not_found(self, mock_query_db):
        """Test the /cves/id/<int:id> route with a non-existing ID."""
        mock_query_db.return_value = []  # Simulate no data found
        response = self.app.get('/cves/id/999')
        self.assertEqual(response.status_code, 404)
        self.assertIn('Metrics not found', response.json['message'])

if __name__ == '__main__':
    unittest.main()
