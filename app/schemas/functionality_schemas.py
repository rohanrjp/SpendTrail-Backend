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