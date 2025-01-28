from sqlalchemy.orm import Session
from sqlalchemy.sql import extract
from app.models.auth_models import User
from app.models.incomes import Incomes
from app.models.expenses import Expenses
from datetime import datetime
from collections import defaultdict
from app.services.functionality_services import get_expenses,get_budgets,get_incomes

def get_dashboard_graph_data(db:Session,user):
    
    current_month=datetime.now().month 
    current_year=datetime.now().year 
    
    
    expenses=db.query(Expenses).filter(Expenses.owner==user.id,extract('month',Expenses.expense_created_date)==current_month,extract('year',Expenses.expense_created_date)==current_year).all()
    incomes=db.query(Incomes).filter(Incomes.owner==user.id,extract('month',Incomes.income_created_date)==current_month,extract('year',Incomes.income_created_date)==current_year).all()
    
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