import psycopg2
from psycopg2 import OperationalError

# 🔗 Replace with your actual Railway DB URL
DATABASE_URL = "postgresql://postgres:UsoNZuqheZOsjLHGlJWXejGsMUnUydQX@switchback.proxy.rlwy.net:14728/railway"

def check_postgres_connection():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        conn.close()
        print("✅ Database is reachable and running.")
    except OperationalError as e:
        print("❌ Database connection failed!")
        print(f"Error: {e}")

check_postgres_connection()
