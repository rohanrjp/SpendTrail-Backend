from pydantic import BaseModel

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