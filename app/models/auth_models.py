from sqlalchemy import Column,DateTime,Integer,String,ForeignKey
from app.core.db import Base


class User(Base):
    
    __tablename__="user_details"
    
    id=Column(Integer,index=True,primary_key=True)
    name=Column(String,nullable=False)
    email=Column(String,unique=True,nullable=False)
    hashed_password=Column(String,nullable=False)
    avatar = Column(String, nullable=True)  
    join_date = Column(DateTime, nullable=False) 