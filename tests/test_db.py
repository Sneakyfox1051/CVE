import unittest
from unittest.mock import patch, MagicMock
from flask import Flask, g
from api.db import get_db_connection, query_db, close_db_connection

class TestDatabase(unittest.TestCase):

    def setUp(self):
        """Set up a Flask app context for testing."""
        self.app = Flask(__name__)
        self.ctx = self.app.app_context()
        self.ctx.push()

    def tearDown(self):
        """Tear down the Flask app context."""
        self.ctx.pop()

    @patch('api.db.psycopg2.connect')
    def test_get_db_connection(self, mock_connect):
        """Test that database connection is established."""
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn

        conn = get_db_connection()
        self.assertEqual(conn, mock_conn)
        self.assertIn('db_conn', g)  # Ensure connection is stored in Flask's `g`

    @patch('api.db.get_db_connection')
    def test_query_db(self, mock_get_conn):
        """Test query execution and return values."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [{"id": 1, "name": "Test"}]
        mock_conn.cursor.return_value = mock_cursor
        mock_get_conn.return_value = mock_conn

        result = query_db("SELECT * FROM test_table")
        self.assertEqual(result, [{"id": 1, "name": "Test"}])

    @patch('api.db.get_db_connection')
    def test_query_db_no_results(self, mock_get_conn):
        """Test query execution with no results."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = []
        mock_conn.cursor.return_value = mock_cursor
        mock_get_conn.return_value = mock_conn

        result = query_db("SELECT * FROM test_table WHERE id = 999")
        self.assertEqual(result, [])

    @patch('api.db.g', new_callable=dict)
    def test_close_db_connection(self, mock_g):
        """Test closing the database connection."""
        mock_conn = MagicMock()
        mock_g['db_conn'] = mock_conn

        close_db_connection()
        mock_conn.close.assert_called_once()
        self.assertNotIn('db_conn', mock_g)  # Ensure connection is removed

    @patch.dict('os.environ', {'DB_NAME': '', 'DB_USER': '', 'DB_PASSWORD': '', 'DB_HOST': '', 'DB_PORT': ''})
    @patch('api.db.psycopg2.connect')
    def test_missing_env_vars(self, mock_connect):
        """Test handling of missing environment variables."""
        mock_connect.side_effect = Exception("Missing environment variables")
        with self.assertRaises(Exception) as context:
            get_db_connection()
        self.assertIn("Missing environment variables", str(context.exception))

if __name__ == '__main__':
    unittest.main()
