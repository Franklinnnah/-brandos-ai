import psycopg2
from psycopg2.extras import DictCursor
from .config import settings

def get_db_connection():
    conn = psycopg2.connect(settings.database_url)
    return conn

def create_waitlist_table():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS waitlist (
            id SERIAL PRIMARY KEY,
            email VARCHAR(255) UNIQUE NOT NULL,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()
    cur.close()
    conn.close()

def add_to_waitlist(email: str):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=DictCursor)
    try:
        cur.execute("INSERT INTO waitlist (email) VALUES (%s) RETURNING *;", (email,))
        new_entry = cur.fetchone()
        conn.commit()
    except psycopg2.IntegrityError:
        conn.rollback()
        return None # Email already exists
    finally:
        cur.close()
        conn.close()
    return new_entry
