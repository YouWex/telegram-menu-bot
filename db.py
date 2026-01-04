import os
import psycopg2

DATABASE_URL = os.getenv(postgresql://postgres:cMtUoPbZButVHqPWeOiTLtRNVkxOMaeQ@postgres-8ied.railway.internal:5432/railway)

if not DATABASE_URL:
    raise Exception("DATABASE_URL tanımlı değil")

def get_conn():
    return psycopg2.connect(DATABASE_URL, sslmode="require")

def init_db():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id BIGINT PRIMARY KEY,
            is_admin BOOLEAN DEFAULT FALSE
        )
    """)
    conn.commit()
    cur.close()
    conn.close()

def add_user(user_id):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO users (user_id) VALUES (%s) ON CONFLICT DO NOTHING",
        (user_id,)
    )
    conn.commit()
    cur.close()
    conn.close()

def is_admin(user_id):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "SELECT is_admin FROM users WHERE user_id = %s",
        (user_id,)
    )
    row = cur.fetchone()
    cur.close()
    conn.close()
    return row and row[0]
