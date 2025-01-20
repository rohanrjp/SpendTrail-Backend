from fastapi import APIRouter
from app.core.dependancies import db_dependancy
from app.core.auth_dependacies import user_dependancy
from app.schemas.functionality_schemas import expense,updated_expense
from app.services.functionality_services import get_expenses,create_new_expense,update_expense

functionality_router=APIRouter(prefix="/api",tags=["Functionality"])

@functionality_router.get("/expenses")
async def get_all_expenses(db:db_dependancy,user:user_dependancy):
    all_expenses=get_expenses(db,user)
    return all_expenses

@functionality_router.post("/create_expense")
async def new_expense(db:db_dependancy,input_expense:expense,user:user_dependancy):
    create_new_expense(user,db,input_expense)
    return{"message":"Expense created"}

@functionality_router.put("/update_expense/{category}")
async def update_expense_route(db:db_dependancy,user:user_dependancy,category:str,update_expense_request:updated_expense):
    update_expense(user,db,category,update_expense_request.amount_to_add)
    return{"message":"Expense updated"}
    
       