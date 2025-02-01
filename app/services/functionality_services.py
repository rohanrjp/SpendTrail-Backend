from app.models.expenses import Expenses
from app.models.incomes import Incomes
from app.models.budgets import Budgets
from app.schemas.functionality_schemas import expense,updated_expense,income,budget,updated_budget
from sqlalchemy.orm import Session
from app.core.utils import get_ist_datetime
from fastapi import HTTPException,status
from sqlalchemy import extract
from datetime import datetime


def get_expenses(db:Session,user):
    current_month=get_ist_datetime().month
    current_year=get_ist_datetime().year
    
    return db.query(Expenses).filter(Expenses.owner==user.id,extract('month',Expenses.expense_created_date)==current_month,extract('year',Expenses.expense_created_date)==current_year).all()

def create_new_expense(user, db: Session, input_expense: expense):
    current_month = get_ist_datetime().month
    current_year = get_ist_datetime().year

    corresponding_budget = db.query(Budgets).filter(
        Budgets.budget_category == input_expense.expense_category,
        Budgets.owner == user.id,
        extract('month', Budgets.budget_created_date) == current_month,
        extract('year', Budgets.budget_created_date) == current_year
    ).first()

    if not corresponding_budget:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"No corresponding budget exists for category '{input_expense.expense_category}' in the current month. Create a budget for this category to record an expense"
        )

    existing_expense = db.query(Expenses).filter(
        Expenses.expense_category == input_expense.expense_category,
        Expenses.owner == user.id,
        extract('month', Expenses.expense_created_date) == current_month,
        extract('year', Expenses.expense_created_date) == current_year
    ).first()

    if existing_expense:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"An expense already exists for category '{input_expense.expense_category}' this month."
        )

    try:
        expense_created_date = get_ist_datetime()
        new_expense = Expenses(
            expense_amount=input_expense.expense_amount,
            expense_category=input_expense.expense_category,
            expense_emoji=input_expense.expense_emoji,
            expense_created_date=expense_created_date,
            owner=user.id
        )
        db.add(new_expense)
        db.commit()
        db.refresh(new_expense)

        return new_expense

    except Exception as e:
        db.rollback() 
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while creating the expense: {str(e)}"
        )
    
def update_expense(user,db:Session,category:str,amount_to_add:updated_expense):
    current_month = get_ist_datetime().month
    current_year = get_ist_datetime().year

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
    
def get_incomes(db:Session,user):
    current_month=get_ist_datetime().month
    current_year=get_ist_datetime().year
    
    return db.query(Incomes).filter(Incomes.owner==user.id,extract('month',Incomes.income_created_date)==current_month,extract('year',Incomes.income_created_date)==current_year).all()
  

def create_new_income(db: Session, user, input_income: income):
    current_month = datetime.now().month
    current_year = datetime.now().year

    existing_income = db.query(Incomes).filter(
        Incomes.income_category == input_income.income_category,
        Incomes.owner == user.id,
        extract('month', Incomes.income_created_date) == current_month,
        extract('year', Incomes.income_created_date) == current_year
    ).first()

    if existing_income:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"An income already exists for category '{input_income.income_category}' this month."
        )

    try:
        income_created_date = get_ist_datetime()
        new_income = Incomes(
            income_amount=input_income.income_amount,
            income_category=input_income.income_category,
            income_emoji=input_income.income_emoji,
            income_created_date=income_created_date,
            owner=user.id
        )

        db.add(new_income)
        db.commit()
        db.refresh(new_income)

        return new_income  

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while creating the income: {str(e)}"
        )     
    
    
def update_income(db:Session,user,category:str,amount_to_add:float):
    current_month = get_ist_datetime().month
    current_year = get_ist_datetime().year

    income = db.query(Incomes).filter(
        Incomes.income_category == category,
        Incomes.owner == user.id,
        extract('month', Incomes.income_created_date) == current_month,
        extract('year', Incomes.income_created_date) == current_year
    ).first()

    if not income:
        raise HTTPException(status_code=404, detail="Income category not found or not owned by the user")

    amount_to_add = float(amount_to_add)

    income.income_amount += amount_to_add

    income.recent_income_amount = amount_to_add
    income.recent_income_date = get_ist_datetime()

    db.commit()
    db.refresh(income)          
    
def create_new_budget(db: Session, user, input_budget: budget):
    current_month = get_ist_datetime().month
    current_year = get_ist_datetime().year

    existing_budget = db.query(Budgets).filter(
        Budgets.budget_category == input_budget.budget_category,
        Budgets.owner == user.id,
        extract('month', Budgets.budget_created_date) == current_month,
        extract('year', Budgets.budget_created_date) == current_year
    ).first()

    if existing_budget:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"A budget already exists for category '{input_budget.budget_category}' this month."
        )

    try:
        budget_created_date = get_ist_datetime()
        new_budget = Budgets(
            budget_amount=input_budget.budget_amount,
            budget_category=input_budget.budget_category,
            budget_emoji=input_budget.budget_emoji,
            budget_created_date=budget_created_date,
            owner=user.id
        )

        db.add(new_budget)
        db.commit()
        db.refresh(new_budget)

        return new_budget  

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while creating the budget: {str(e)}"
        )
        
def get_budgets(db:Session,user):
    
    current_month=get_ist_datetime().month
    current_year=get_ist_datetime().year      
    
    return db.query(Budgets).filter(Budgets.owner==user.id,extract('month',Budgets.budget_created_date)==current_month,extract('year',Budgets.budget_created_date)==current_year).all()

def update_budget(db:Session,user,category,update_budget_request:updated_budget):
    
    current_month=datetime.now().month
    current_year=datetime.now().year
    
    budget_to_be_updated=db.query(Budgets).filter(Budgets.owner==user.id,extract('month',Budgets.budget_created_date)==current_month,extract('year',Budgets.budget_created_date)==current_year,Budgets.budget_category==category).first()
    
    budget_to_be_updated.budget_amount+=update_budget_request.amount_to_add
    
    budget_to_be_updated.recent_budget_amount=update_budget_request.amount_to_add
    budget_to_be_updated.recent_budget_date=get_ist_datetime()
    
    db.commit()
    db.refresh(budget_to_be_updated)
    
def get_all_budget_details(db:Session,user):
    
    current_month=get_ist_datetime().month 
    current_year=get_ist_datetime().year
    
    budgets=db.query(Budgets).filter(Budgets.owner==user.id,extract('month',Budgets.budget_created_date)==current_month,extract('year',Budgets.budget_created_date)==current_year).all()
    expenses=db.query(Expenses).filter(Expenses.owner==user.id,extract('month',Expenses.expense_created_date)==current_month,extract('year',Expenses.expense_created_date)==current_year).all()
    
    expenses_by_category = {expense.expense_category: expense.expense_amount for expense in expenses}
    
    budget_details=[]
    for budget in budgets:
        spent=expenses_by_category.get(budget.budget_category,0)
        remaining=budget.budget_amount-spent
        budget_details.append({
            "id": budget.id,
            "category": budget.budget_category,
            "total_budget_amount": budget.budget_amount,
            "emoji":budget.budget_emoji,
            "spent": spent,
            "remaining": remaining
        })

    return budget_details

    