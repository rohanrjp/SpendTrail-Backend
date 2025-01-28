from fastapi import APIRouter
from app.services.ai_services import get_ai_response,generate_prompt,format_expense_data,format_budget_data,format_income_data
from app.core.dependancies import db_dependancy
from app.core.auth_dependacies import user_dependancy

ai_router=APIRouter(prefix="/api/ai",tags=["Ai"])

@ai_router.get("")
async def ai_feature(db:db_dependancy,user:user_dependancy):
    expenses=format_expense_data(db,user)
    budgets=format_budget_data(db,user)
    incomes=format_income_data(db,user)
    prompt=generate_prompt(expenses=expenses,budgets=budgets,incomes=incomes)
    response = get_ai_response(prompt)
    return response