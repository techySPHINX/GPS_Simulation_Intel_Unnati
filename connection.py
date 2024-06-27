import os
from sqlalchemy import create_engine

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("Please set it before running the application.")

engine = create_engine(DATABASE_URL)

DATABASE_URL = engine  

