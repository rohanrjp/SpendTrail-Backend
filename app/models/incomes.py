from sqlalchemy import Column,Integer,String,ForeignKey,Float,DateTime
from sqlalchemy.sql import func
from app.core.db import Base

class Incomes(Base):
    
    __tablename__="incomes"
    
    id = Column(Integer, primary_key=True, index=True)
    income_amount = Column(Float, nullable=False)
    recent_income_amount = Column(Float, default=0, nullable=False)  
    income_category = Column(String, nullable=False)
    income_emoji = Column(String, nullable=False)
    income_created_date = Column(DateTime, default=func.now(), nullable=False)  
    recent_income_date = Column(DateTime, nullable=True)  
    updated_date = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)  
    owner = Column(Integer, ForeignKey("user_details.id"), nullable=False)