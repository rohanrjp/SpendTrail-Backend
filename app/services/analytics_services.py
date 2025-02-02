from app.core.utils import get_ist_datetime
from sqlalchemy.orm import Session
from sqlalchemy.sql import extract,func
from app.models.incomes import Incomes
from app.models.expenses import Expenses
from app.models.budgets import Budgets



def get_monthlyData(db:Session,user):
    
    current_month=get_ist_datetime().month
    current_year=get_ist_datetime().year
    MONTHNUMBER_TO_MONTH={
        1:"Jan",
        2:"Feb",
        3:"Mar",
        4:"Apr",
        5:"May",
        6:"Jun",
        7:"Jul",
        8:"Aug",
        9:"Sep",
        10:"Oct",
        11:"Nov",
        12:"Dec"
    }
    monthlyData=[]
    
    for i in range(1,current_month+1):
        
        incomes=db.query(Incomes).filter(Incomes.owner==user.id,extract('month',Incomes.income_created_date)==i,extract('year',Incomes.income_created_date)==current_year).all()
        expenses=db.query(Expenses).filter(Expenses.owner==user.id,extract('month',Expenses.expense_created_date)==i,extract('year',Expenses.expense_created_date)==current_year).all()
        current_month_in_str=MONTHNUMBER_TO_MONTH[i]
        total_income_for_month=sum( income.income_amount for income in incomes) if incomes else 0
        total_expense_for_month=sum(expense.expense_amount for expense in expenses) if expenses else 0
        monthlyData.append({"name":current_month_in_str,"income":total_income_for_month,"expense":total_expense_for_month})
    
    return monthlyData
    
    
def get_savingsData(db:Session,user):
        
    current_month=get_ist_datetime().month
    current_year=get_ist_datetime().year
    MONTHNUMBER_TO_MONTH={
        1:"Jan",
        2:"Feb",
        3:"Mar",
        4:"Apr",
        5:"May",
        6:"Jun",
        7:"Jul",
        8:"Aug",
        9:"Sep",
        10:"Oct",
        11:"Nov",
        12:"Dec"
    }
    savingsData=[]
    for i in range(1,current_month+1):
        incomes=db.query(Incomes).filter(Incomes.owner==user.id,extract('month',Incomes.income_created_date)==i,extract('year',Incomes.income_created_date)==current_year).all()
        expenses=db.query(Expenses).filter(Expenses.owner==user.id,extract('month',Expenses.expense_created_date)==i,extract('year',Expenses.expense_created_date)==current_year).all()
        current_month_in_str=MONTHNUMBER_TO_MONTH[i]
        total_income = sum(income.income_amount for income in incomes) if incomes else 0
        total_expense = sum(expense.expense_amount for expense in expenses) if expenses else 0
        total_savings_for_month = total_income - total_expense
        savingsData.append({"name":current_month_in_str,"amount":total_savings_for_month})
        
    return savingsData    
    
def get_expenseGrowthData(db:Session,user):
    
    current_date = get_ist_datetime()
    current_month = current_date.month
    current_year = current_date.year

    last_month = 12 if current_month == 1 else current_month - 1
    last_year = current_year - 1 if current_month == 1 else current_year

    last_month_expenses = db.query(
        Expenses.expense_category, func.sum(Expenses.expense_amount).label("total")
    ).filter(
        Expenses.owner == user.id,
        extract('month', Expenses.expense_created_date) == last_month,
        extract('year', Expenses.expense_created_date) == last_year
    ).group_by(Expenses.expense_category).all()

    current_month_expenses = db.query(
        Expenses.expense_category, func.sum(Expenses.expense_amount).label("total")
    ).filter(
        Expenses.owner == user.id,
        extract('month', Expenses.expense_created_date) == current_month,
        extract('year', Expenses.expense_created_date) == current_year
    ).group_by(Expenses.expense_category).all()

    last_month_dict = {category: total for category, total in last_month_expenses}

    expenseGrowthData = []
    
    for category, total_expense in current_month_expenses:
        last_month_expense = last_month_dict.get(category, 0)  

        growth_rate = ((total_expense - last_month_expense) / last_month_expense * 100) if last_month_expense else 0

        expenseGrowthData.append({
            "category": category,
            "growthRate": round(growth_rate, 2)  
        })

    return expenseGrowthData
    
def get_overviewData(db:Session,user):
    
    current_month=get_ist_datetime().month
    current_year=get_ist_datetime().year
    MONTHNUMBER_TO_MONTH={
        1:"Jan",
        2:"Feb",
        3:"Mar",
        4:"Apr",
        5:"May",
        6:"Jun",
        7:"Jul",
        8:"Aug",
        9:"Sep",
        10:"Oct",
        11:"Nov",
        12:"Dec"
    }
    
    overviewData=[]
    
    for i in range(1,current_month+1):
        
        expenses=db.query(Expenses).filter(Expenses.owner==user.id,extract('month',Expenses.expense_created_date)==i,extract('year',Expenses.expense_created_date)==current_year).all()
        budgets=db.query(Budgets).filter(Budgets.owner==user.id,extract('month',Budgets.budget_created_date)==i,extract('year',Budgets.budget_created_date)==current_year).all()
        current_month_in_str=MONTHNUMBER_TO_MONTH[i]
        total_expense_for_month=sum(expense.expense_amount for expense in expenses) if expenses else 0
        total_budget_for_month=sum( budget.budget_amount for budget in budgets) if budgets else 0
        overviewData.append({"name":current_month_in_str,"expenses":total_expense_for_month,"budget":total_budget_for_month,})
    
    return overviewData 
    
            