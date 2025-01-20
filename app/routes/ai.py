from fastapi import APIRouter
from app.services.ai_services import get_ai_response,generate_prompt

ai_router=APIRouter(prefix="/api/ai",tags=["Ai"])

expenses=[
    { "category": "Food", "amount": 500 },
    { "category": "Transport", "amount": 300 },
    { "category": "Entertainment", "amount": 200 }
]

budgets=[
    { "category": "Food", "amount": 400 },
    { "category": "Transport", "amount": 350 },
    { "category": "Entertainment", "amount": 100 }
]

incomes=[
    { "source": "Salary", "amount": 3000 },
    { "source": "Freelance", "amount": 500 }
]


@ai_router.get("")
async def ai_feature():
    prompt=generate_prompt(expenses=expenses,budgets=budgets,incomes=incomes)
    response = get_ai_response(prompt)
    return response