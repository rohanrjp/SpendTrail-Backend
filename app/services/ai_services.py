from app.core.config import Config
import google.generativeai as genai
from sqlalchemy.orm import Session
from app.services.functionality_services import get_expenses,get_budgets,get_incomes


genai.configure(api_key=Config.GEMINI_API_KEY)

generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain"
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash-8b",
  generation_config=generation_config,
)
def generate_prompt(expenses: list, budgets: list, incomes: list) -> str:
    prompt = f"""
You are a financial analysis expert tasked with reviewing the provided financial data. Your analysis should be accurate, detailed, and actionable. Carefully analyze the data to ensure no misinterpretation occurs, especially in identifying whether actual expenses are greater than, equal to, or less than the allocated budgets. 

Based on the data, provide a concise yet comprehensive financial summary covering:
1. Overall financial health: Compare total income to total expenses and calculate the surplus or deficit.
2. Spending accuracy: Identify any overspending or underspending in individual categories by comparing actual expenses to their respective budgets. Explicitly state which categories are over or under budget and by how much.
3. Budget adherence: Assess how well the user is sticking to their budget.
4. Actionable insights: Provide specific, tailored recommendations to improve their financial situation. Recommendations should focus on reallocating funds, optimizing spending patterns, or adjusting budgets where necessary. 

Here is the data:

Expenses: {expenses}
Incomes: {incomes}
Budgets: {budgets}

Ensure your analysis is based strictly on the data provided and contains no assumptions or errors. Recheck all calculations twice before generating insights. Your response should be a single, coherent paragraph with clear observations and actionable advice.
"""
    return prompt


def get_ai_response(prompt:str):
    response = model.generate_content(contents=prompt)
    return response.text
  
def format_expense_data(db:Session,user): 
  
  expenses=get_expenses(db,user)
  
  formatted_expense=[
    {"Category":expense.expense_category,"Amount":expense.expense_amount}
    for expense in expenses
  ]
  
  return formatted_expense

def format_budget_data(db:Session,user):
  
  budgets=get_budgets(db,user)
  
  formatted_budget=[
    {"Category":budget.budget_category,"Amount":budget.budget_amount}
    for budget in budgets    
  ]
  
  return formatted_budget

def format_income_data(db:Session,user):
  
  incomes=get_incomes(db,user)
  
  formatted_income=[
    {"Category":income.income_category,"Amount":income.income_amount}
    for income in incomes      
  ]
  
  return formatted_income