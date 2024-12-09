from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from core.config import Config

engine=create_engine(Config.DATABASE_URL)
Session_Local=sessionmaker(bind=engine,autoflush=False,autocommit=False)
Base=declarative_base()

def init_db():
    Base.metadata.create_all(bind=engine) 
    print("Tables created succesfully")