from sqlalchemy import Column,Integer,String,ForeignKey
from core.db import Base


class User(Base):
    
    __tablename__="user_details"
    
    id=Column(Integer,index=True,primary_key=True)
    name=Column(String,nullable=False)
    email=Column(String,unique=True,nullable=False)
    hashed_password=Column(String,nullable=False)
    avatar = Column(String, nullable=True)  