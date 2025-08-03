from pydantic import BaseModel  
from datetime import datetime  
from typing import Optional, Union  
from enum import Enum  
  
class FrequencyType(str, Enum):  
    DAILY = "daily"  
    WEEKLY = "weekly"  
    MONTHLY = "monthly"  
    YEARLY = "yearly"  
  
class subscription(BaseModel):  
    name: str  
    amount: float  
    category: str  
    frequency: FrequencyType  
    start_date: datetime  
    end_date: Union[datetime, None] = None  
    repeat_count: Union[int, None] = None  
  
class updated_subscription(BaseModel):
    id: int
    name: Union[str, None] = None  
    amount: Union[float, None] = None
    is_active: Union[bool, None] = None
    end_date: Union[datetime, None] = None  
    repeat_count: Union[int, None] = None 