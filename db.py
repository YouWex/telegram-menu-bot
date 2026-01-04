import os
import psycopg2

DATABASE_URL = os.getenv("postgresql://postgres:WBGNhsAfDbnTJgVKQMJGEVkvGDDPxkKI@postgres.railway.internal:5432/railway")

conn = psycopg2.connect(postgresql://postgres:WBGNhsAfDbnTJgVKQMJGEVkvGDDPxkKI@postgres.railway.internal:5432/railway, sslmode="require")
cursor = conn.cursor()

def init_db():
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id BIGINT PRIMARY KEY,
        username TEXT,
        is_admin BOOLEAN DEFAULT FALSE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.commit()

def add_user(user_id, username):
    cursor.execute(
        "INSERT INTO users (user_id, username) VALUES (%s, %s) ON CONFLICT DO NOTHING",
        (user_id, username)
    )
    conn.commit()

def is_admin(user_id):
    cursor.execute("SELECT is_admin FROM users WHERE user_id=%s", (user_id,))
    row = cursor.fetchone()
    return row and row[0]
