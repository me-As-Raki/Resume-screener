from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import User, Result
from app.extensions import db

# ✅ PostgreSQL connection
postgres_url = 'postgresql://resume_screener_db_user:uGpGLuhpFXZLbEY6CoyRbnxHQssq7YQ6@dpg-d193no7fte5s73bv75bg-a.oregon-postgres.render.com:5432/resume_screener_db?sslmode=require'
pg_engine = create_engine(postgres_url)
PGSession = sessionmaker(bind=pg_engine)
pg_session = PGSession()

# ✅ Create tables only
db.metadata.create_all(pg_engine)

print("✅ PostgreSQL DB is initialized with tables.")
