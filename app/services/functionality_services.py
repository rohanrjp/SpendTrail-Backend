from app.models.expenses import Expenses
from app.schemas.functionality_schemas import expense,updated_expense
from sqlalchemy.orm import Session
from app.core.utils import get_ist_datetime
from fastapi import HTTPException
from sqlalchemy import extract
from datetime import datetime


def get_expenses(db:Session,user):
    current_month=datetime.now().month
    current_year=datetime.now().year
    
    return db.query(Expenses).filter(Expenses.owner==user.id,extract('month',Expenses.expense_created_date)==current_month,extract('year',Expenses.expense_created_date)==current_year).all()

def create_new_expense(user,db,input_expense:expense):
    expense_created_date=get_ist_datetime()
    new_expense=Expenses(expense_amount=input_expense.expense_amount,expense_category=input_expense.expense_category,expense_emoji=input_expense.expense_emoji,expense_created_date=expense_created_date,owner=user.id)
    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)
    
    
def update_expense(user,db:Session,category:str,amount_to_add:updated_expense):
    current_month = datetime.now().month
    current_year = datetime.now().year

    expense = db.query(Expenses).filter(
        Expenses.expense_category == category,
        Expenses.owner == user.id,
        extract('month', Expenses.expense_created_date) == current_month,
        extract('year', Expenses.expense_created_date) == current_year
    ).first()

    if not expense:
        raise HTTPException(status_code=404, detail="Expense category not found or not owned by the user")

    amount_to_add = float(amount_to_add)

    expense.expense_amount += amount_to_add

    expense.recent_expense_amount = amount_to_add
    expense.recent_expense_date = get_ist_datetime()

    db.commit()
    db.refresh(expense)  
    