from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

load_dotenv('.env')

DATABASE_URL = "postgresql://" + os.environ.get("DB_USER") + ":" + os.environ.get("DB_PASSWORD") + "@" + os.environ.get("DB_HOST") + "/" + os.environ.get("DATABASE")

engine = create_engine(DATABASE_URL)
session_maker = sessionmaker(autocommit=False, autoflush=False, bind=engine)
