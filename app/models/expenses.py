from sqlalchemy import Column,Integer,String,ForeignKey,Float,DateTime
from sqlalchemy.sql import func
from app.core.db import Base

class Expenses(Base):
    
    __tablename__="expenses"
    
    id = Column(Integer, primary_key=True, index=True)
    expense_amount = Column(Float, nullable=False)
    recent_expense_amount = Column(Float, default=0, nullable=False)  
    expense_category = Column(String, nullable=False)
    expense_emoji = Column(String, nullable=False)
    expense_created_date = Column(DateTime, default=func.now(), nullable=False)  
    recent_expense_date = Column(DateTime, nullable=True)  
    updated_date = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)  
    owner = Column(Integer, ForeignKey("user_details.id"), nullable=False)