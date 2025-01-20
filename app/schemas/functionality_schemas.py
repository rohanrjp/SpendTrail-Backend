from pydantic import BaseModel

class expense(BaseModel):
   expense_amount:float
   expense_category:str
   expense_emoji:str 
   
class updated_expense(BaseModel):
   amount_to_add:float   