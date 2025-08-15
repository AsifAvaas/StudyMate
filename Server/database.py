from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from dotenv import load_dotenv
import os


load_dotenv()

database_url=os.getenv("Database_URL")

engine=create_engine(database_url)
LocalSession=sessionmaker(autoflush=False, bind=engine)


Base=declarative_base()

def get_db():
    db=LocalSession()
    try:
        yield db
    finally:
        db.close()