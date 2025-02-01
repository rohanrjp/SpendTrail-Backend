from fastapi import APIRouter,status,Query
from app.core.dependancies import db_dependancy
from app.core.auth_dependacies import user_dependancy
from app.services.dashboard_services import get_dashboard_graph_data,get_aggregate_data,get_recent_expense_data,update_income_goal,update_savings_goal,get_past_financial_data,get_past_dashboard_graph_data
from app.schemas.functionality_schemas import input_income_goal,InputSavingsGoal,PastRecord
from app.core.utils import get_ist_datetime


dashboard_router=APIRouter(prefix='/api/dashboard',tags=["Dashboard"])

def get_current_year():
   return get_ist_datetime().year 

@dashboard_router.get('/graphs',status_code=status.HTTP_200_OK)
async def get_graph_data(db:db_dependancy,user:user_dependancy):
    graph_data=get_dashboard_graph_data(db,user)
    return graph_data

@dashboard_router.get('/financialData',status_code=status.HTTP_200_OK)
async def get_financialData(db:db_dependancy,user:user_dependancy):
    financialData=get_aggregate_data(db,user)
    return financialData

@dashboard_router.get('/recent_expenses',status_code=status.HTTP_200_OK)
async def get_datatable_data(db:db_dependancy,user:user_dependancy):
    recent_expense=get_recent_expense_data(db,user)
    return recent_expense

@dashboard_router.put('/update_income_goal',status_code=status.HTTP_200_OK)
async def update_income_goal_route(db:db_dependancy,user:user_dependancy,input_income_goal:input_income_goal):
    updated_user=update_income_goal(db,user,input_income_goal.amount_to_update)
    return {"message":"Income goals updated","new_income_goal":updated_user.income_goal}

@dashboard_router.put('/update_savings_goal',status_code=status.HTTP_200_OK)
async def update_savings_goal_route(db:db_dependancy,user:user_dependancy,input_savings_goal:InputSavingsGoal):
    updated_user=update_savings_goal(db,user,input_savings_goal.amount_to_update)
    return {"message":"Savings goal updated","new_savings_goal":updated_user.savings_goal}

@dashboard_router.get('/past-reports/',tags=["Past Reports"])
async def get_past_records_route(db:db_dependancy,user:user_dependancy,month:str=Query(...,description="Input month"),year:int=Query(...,ge=2000,le=get_current_year())):
    record=PastRecord(month=month,year=year)
    financialData=get_past_financial_data(db,user,record.month,record.year)
    graph_data=get_past_dashboard_graph_data(db,user,record.month,record.year)
    data={"financialData":financialData,"graph_data":graph_data}
    return data
    
    
    
    