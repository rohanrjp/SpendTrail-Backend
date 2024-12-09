from sqlalchemy import Column,Integer,String,ForeignKey
from app.core.db import Base

class Expenses(Base):
    
    __tablename__="expenses"
    
    id=Column(Integer,index=True,primary_key=True)
    expense_name=Column(String)
    expense_amount=Column(Integer)
    expense_category=Column(String)
    owner=Column(Integer,ForeignKey("user_details.id"))