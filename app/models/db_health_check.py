from sqlalchemy import Column,Integer,DateTime
from sqlalchemy.sql import func
from app.core.db import Base

class DBHealthCheck(Base):
    
    __tablename__="db_health_check"
    
    id=Column(Integer,index=True,primary_key=True)
    last_checked_time=Column(DateTime,default=func.now(), onupdate=func.now(),nullable=False)
    