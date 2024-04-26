from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import time

# from .config import settings

SQLALCHEMY_DATABASE_URL = f'postgresql://copy_trap:n6A5KBCl2yn5KAsdCa1OBeLidIjUkZqb@dpg-colpm5i1hbls7393st2g-a.frankfurt-postgres.render.com/copy_trap'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
