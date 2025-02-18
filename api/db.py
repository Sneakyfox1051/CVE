import os
import psycopg2
from psycopg2.extras import RealDictCursor
from flask import g
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

def get_db_connection():
    """Establish a database connection and store it in the Flask context."""
    if 'db_conn' not in g:
        g.db_conn = psycopg2.connect(
            dbname=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT')
        )
    return g.db_conn

def query_db(query, args=(), one=False):
    """Execute a query and return the results."""
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def close_db_connection(e=None):
    """Close the database connection if it exists."""
    db_conn = g.pop('db_conn', None)
    if db_conn is not None:
        db_conn.close()
