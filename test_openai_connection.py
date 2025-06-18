from sqlalchemy import create_engine

url = "postgresql://resume_screener_db_user:uGpGLuhpFXZLbEY6CoyRbnxHQssq7YQ6@dpg-d193no7fte5s73bv75bg-a.oregon-postgres.render.com:5432/resume_screener_db?sslmode=require"
engine = create_engine(url)

try:
    with engine.connect() as conn:
        print("✅ Connected to PostgreSQL successfully!")
except Exception as e:
    print("❌ Error:", e)
