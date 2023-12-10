from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import config
import os

db_name = os.getenv(config.CONF_OPT_DB_NAME)
db_user = os.getenv(config.CONF_OPT_DB_USER)
db_password = os.getenv(config.CONF_OPT_DB_PASSWORD)
db_host = os.getenv(config.CONF_OPT_DB_HOST)
DATABASE_URL = f"postgresql://{db_user}:{db_password}@{db_host}/{db_name}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
