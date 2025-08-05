from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Float, DateTime, Enum  
from sqlalchemy.sql import func  
from app.core.db import Base  
import enum  
  
class FrequencyType(str, Enum):  
    DAILY = "daily"  
    WEEKLY = "weekly"  
    MONTHLY = "monthly"  
    YEARLY = "yearly"  
  
class Subscriptions(Base):  
    __tablename__ = "subscriptions"  
      
    id = Column(Integer, primary_key=True, index=True)  
    name = Column(String, nullable=False)  
    amount = Column(Float, nullable=False)  
    category = Column(String, nullable=False)  # Must match existing budget category  
    frequency = Column(String, nullable=False)  
    start_date = Column(DateTime(timezone=True), nullable=False)  
    end_date = Column(DateTime(timezone=True), nullable=True)  # Optional  
    repeat_count = Column(Integer, nullable=True)  # Optional  
    current_count = Column(Integer, default=0, nullable=False)  # Track executions  
    is_active = Column(Boolean, default=True, nullable=False)  
    created_date = Column(DateTime, default=func.now(), nullable=False)  
    updated_date = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    updated_isactive_date = Column(DateTime, nullable=True)
    owner = Column(Integer, ForeignKey("user_details.id"), nullable=False)
