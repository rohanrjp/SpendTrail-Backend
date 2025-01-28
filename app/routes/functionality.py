from fastapi import APIRouter,status
from app.core.dependancies import db_dependancy
from app.core.auth_dependacies import user_dependancy
from app.schemas.functionality_schemas import expense,updated_expense,income,updated_income,budget,updated_budget
from app.services.functionality_services import get_expenses,create_new_expense,update_expense,get_incomes,create_new_income,update_income,create_new_budget,get_budgets,update_budget,get_all_budget_details

functionality_router=APIRouter(prefix="/api",tags=["Functionality"])

@functionality_router.get("/expenses",status_code=status.HTTP_200_OK)
async def get_all_expenses(db:db_dependancy,user:user_dependancy):
    all_expenses=get_expenses(db,user)
    return all_expenses

@functionality_router.post("/create_expense",status_code=status.HTTP_201_CREATED)
async def new_expense(db:db_dependancy,input_expense:expense,user:user_dependancy):
    create_new_expense(user,db,input_expense)
    return{"message":"Expense created"}

@functionality_router.put("/update_expense/{category}")
async def update_expense_route(db:db_dependancy,user:user_dependancy,category:str,update_expense_request:updated_expense):
    update_expense(user,db,category,update_expense_request.amount_to_add)
    return{"message":"Expense updated"}
    
@functionality_router.get('/incomes',status_code=status.HTTP_200_OK)
async def get_all_incomes(db:db_dependancy,user:user_dependancy):
    all_incomes=get_incomes(db,user)
    return all_incomes 

@functionality_router.post('/create_income',status_code=status.HTTP_201_CREATED)
async def new_income(db:db_dependancy,user:user_dependancy,input_income:income):
    create_new_income(db,user,input_income)
    return {"message":"Income created"}

@functionality_router.put("/update_income/{category}")
async def update_income_route(db:db_dependancy,user:user_dependancy,category:str,update_income_request:updated_income):
    update_income(db,user,category,update_income_request.amount_to_add)
    return{"message":"Income updated"}
     
@functionality_router.post('/create_budget',status_code=status.HTTP_201_CREATED)
async def new_budget(db:db_dependancy,user:user_dependancy,input_budget:budget):
    create_new_budget(db,user,input_budget)
    return {"message":"Budget created"}  

@functionality_router.get("/budgets",status_code=status.HTTP_200_OK)
async def get_all_budgets(db:db_dependancy,user:user_dependancy):
    all_budgets=get_budgets(db,user)
    return all_budgets   

@functionality_router.put("/update_budget/{category}",status_code=status.HTTP_200_OK)
async def update_budget_route(db:db_dependancy,user:user_dependancy,category:str,update_budget_request:updated_budget):
    update_budget(db,user,category,update_budget_request)
    return {"message":"Budget updated"}
    
@functionality_router.get("/budget_details",status_code=status.HTTP_200_OK)
async def get_all_budget_details_route(db:db_dependancy,user:user_dependancy):
    all_budget_details=get_all_budget_details(db,user)
    return all_budget_details    