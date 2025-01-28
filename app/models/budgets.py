from sqlalchemy import Column,Integer,String,ForeignKey,Float,DateTime
from sqlalchemy.sql import func
from app.core.db import Base

class Budgets(Base):
    
    __tablename__="budgets"
    
    id = Column(Integer, primary_key=True, index=True)
    budget_amount = Column(Float, nullable=False)
    recent_budget_amount = Column(Float, default=0, nullable=False)  
    budget_category = Column(String, nullable=False)
    budget_emoji = Column(String, nullable=False)
    budget_created_date = Column(DateTime, default=func.now(), nullable=False)  
    recent_budget_date = Column(DateTime, nullable=True)  
    updated_date = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)  
    owner = Column(Integer, ForeignKey("user_details.id"), nullable=False)