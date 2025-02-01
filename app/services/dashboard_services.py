from sqlalchemy.orm import Session
from app.models.auth_models import User
from datetime import datetime
from collections import defaultdict
from app.services.functionality_services import get_expenses,get_budgets,get_incomes
from app.schemas.functionality_schemas import input_income_goal,InputSavingsGoal
from fastapi import HTTPException,status
from app.models.expenses import Expenses
from app.models.budgets import Budgets
from app.models.incomes import Incomes
from sqlalchemy import extract


def get_dashboard_graph_data(db:Session,user):
    
    current_month=datetime.now().month 
    current_year=datetime.now().year 
    
    
    expenses=get_expenses(db,user)
    incomes=get_incomes(db,user)
    
    total_expenses=sum(expense.expense_amount for expense in expenses)
    total_income=sum(income.income_amount for income in incomes)
    total_savings=total_income-total_expenses
    
    incomeExpenseAnalysis=[
        { "label": "Income", "amount": total_income, "fill": "#4CAF50" },
        { "label": "Expenses", "amount": total_expenses, "fill": "#F44336" }, 
        { "label": "Savings", "amount": total_savings, "fill": "#8884d8" },
    ]
    
    expense_categories=defaultdict(float)
    for expense in expenses:
        expense_categories[expense.expense_category]+=expense.expense_amount
    
    Piechart_data=[
        {"name":category,"value":amount}
        for category,amount in expense_categories.items()
    ]
    
    dashboard_graph_data = [
    {"type": "incomeExpenseAnalysis", "data": incomeExpenseAnalysis},
    {"type": "Piechart_data", "data": Piechart_data}
    ]
    
    return dashboard_graph_data
    
    
def get_aggregate_data(db:Session,user):
   
   expenses=get_expenses(db,user)
   incomes=get_incomes(db,user)
   budgets=get_budgets(db,user)
   
   current_user=db.query(User).filter(User.id==user.id).first()
   income_goal=current_user.income_goal
   savings_goal=current_user.savings_goal
   
   current_total_expenses=sum(expense.expense_amount for expense in expenses)
   current_total_budget=sum(budget.budget_amount for budget in budgets)
   current_total_income=sum(income.income_amount for income in incomes)
   current_total_savings=current_total_income-current_total_expenses
   
   financialData={
       "expenses":{"current":current_total_expenses,"goal":current_total_budget},
       "budget":{ "current": current_total_expenses, "goal": current_total_budget },
       "income": { "current": current_total_income, "goal": income_goal },
       "savings": { "current":current_total_savings , "goal": savings_goal },
   } 
   
   return financialData

def get_recent_expense_data(db:Session,user):
    
    expenses=get_expenses(db,user)
    
    recent_expenses=[
        { "category": expense.expense_category , "amount": expense.recent_expense_amount, "date": expense.recent_expense_date.strftime("%d-%m-%Y") if expense.recent_expense_date else "-"}
        for expense in expenses if expense.recent_expense_amount!=0
    ]
    
    return recent_expenses    
    
def update_income_goal(db:Session,user,new_income_goal:float):   
    current_user=db.query(User).filter(User.id==user.id).first()
    if not current_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")
    current_user.income_goal=new_income_goal
    db.commit()
    db.refresh(current_user)
    return current_user

def update_savings_goal(db:Session,user,new_savings_goal:float):
    current_user=db.query(User).filter(User.id==user.id).first()
    if not current_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")
    current_user.savings_goal=new_savings_goal
    db.commit()
    db.refresh(current_user)
    return current_user
    
def get_past_financial_data(db:Session,user,month:str,year:int):
    
    MONTH_NAME_TO_NUMBER = {
    "January": 1, "February": 2, "March": 3, "April": 4, "May": 5, "June": 6,
    "July": 7, "August": 8, "September": 9, "October": 10, "November": 11, "December": 12
    }
    
    month_number = MONTH_NAME_TO_NUMBER.get(month)
    if month_number is None:
        raise ValueError(f"Invalid month name: {month}")
    
    expenses=db.query(Expenses).filter(Expenses.owner==user.id,extract('month',Expenses.expense_created_date)==month_number,extract('year',Expenses.expense_created_date)==year).all()
    incomes=db.query(Incomes).filter(Incomes.owner==user.id,extract('month',Incomes.income_created_date)==month_number,extract('year',Incomes.income_created_date)==year).all()
    budgets=db.query(Budgets).filter(Budgets.owner==user.id,extract('month',Budgets.budget_created_date)==month_number,extract('year',Budgets.budget_created_date)==year).all()

    if not expenses and not incomes and not budgets:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Past expenses/incomes/budgets not found")
    
    current_user=db.query(User).filter(User.id==user.id).first()
    income_goal=current_user.income_goal
    savings_goal=current_user.savings_goal
    
    current_total_expenses=sum(expense.expense_amount for expense in expenses)
    current_total_budget=sum(budget.budget_amount for budget in budgets)
    current_total_income=sum(income.income_amount for income in incomes)
    current_total_savings=current_total_income-current_total_expenses
   
    financialData={
       "expenses":{"current":current_total_expenses,"goal":current_total_budget},
       "budget":{ "current": current_total_expenses, "goal": current_total_budget },
       "income": { "current": current_total_income, "goal": income_goal },
       "savings": { "current":current_total_savings , "goal": savings_goal },
     } 
   
    return financialData
        