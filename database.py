"""
    This module contains database configs and ORM initializer
"""

import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DB = os.environ["DB"]
DB_PORT = os.environ["DB_PORT"]
DB_HOST = os.environ["DB_HOST"]
DB_PASS = os.environ["DB_PASS"]
DB_USER = os.environ["DB_USER"]
db_url = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB}"

engine = create_engine(db_url)
session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
base = declarative_base()
