import psycopg2
from config import DATABASE_URL

def get_connection():
    return psycopg2.connect(DATABASE_URL)

def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS content (
        id SERIAL PRIMARY KEY,
        year TEXT,
        chapter TEXT,
        section TEXT,
        subject TEXT,
        type TEXT,
        file_url TEXT
    )
    """)

    conn.commit()
    cur.close()
    conn.close()
