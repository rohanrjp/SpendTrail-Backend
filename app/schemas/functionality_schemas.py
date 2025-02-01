from pydantic import BaseModel,Field
from typing import Literal
from datetime import datetime
from app.core.utils import get_ist_datetime

class expense(BaseModel):
   expense_amount:float
   expense_category:str
   expense_emoji:str 
   
class updated_expense(BaseModel):
   amount_to_add:float   
   
class income(BaseModel):
   income_amount:float
   income_category:str
   income_emoji:str 
   
class updated_income(BaseModel):
   amount_to_add:float
   
class budget(BaseModel):
   budget_amount:float
   budget_category:str
   budget_emoji:str        
   
class updated_budget(BaseModel):
   amount_to_add:float
      
class input_income_goal(BaseModel):
   amount_to_update:float      
   
class InputSavingsGoal(BaseModel):
   amount_to_update:float   

def get_current_year():
   return get_ist_datetime().year   
   
class PastRecord(BaseModel):
   month:Literal["January","February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"]
   year:int=Field(...,ge=2000,le=get_current_year(),description="Year should be between 2000 and the current year")