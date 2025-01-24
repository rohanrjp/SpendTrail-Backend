from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.core.config import Config

engine=create_engine(Config.DATABASE_URL,pool_pre_ping=True,pool_size=10,max_overflow=5,pool_recycle=1800)
Session_Local=sessionmaker(bind=engine,autoflush=False,autocommit=False)
Base=declarative_base()

def init_db():
    Base.metadata.create_all(bind=engine) 
    print("Tables created succesfully")