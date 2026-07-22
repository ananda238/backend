from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

# Ambil DATABASE_URL dari environment variable
DATABASE_URL = os.getenv("DATABASE_URL")

# Validasi agar aplikasi memberikan pesan error yang jelas jika URL database kosong
if not DATABASE_URL:
    raise ValueError("DATABASE_URL belum disetel di environment variable!")

# Buat engine database
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
