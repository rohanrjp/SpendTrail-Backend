from app.core.config import Config
import google.generativeai as genai


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
You are a financial analysis AI. Based on the given data for expenses, incomes, and budgets, provide a brief but detailed paragraph summarizing the user's financial situation. The summary should highlight:

1. The overall financial health (income vs. expenses).
2. Any significant overspending or underspending in categories (e.g., Food, Entertainment, Transport).
3. Insights into how well the user is sticking to their budget.
4. A short recommendation on what action the user should take next (e.g., adjust a category, consider savings, or review their spending patterns).

Here is the data:

Expenses: {expenses}
Incomes: {incomes}
Budgets: {budgets}

Your response should be a paragraph with all the important points, focusing on overall financial health, key observations, and any advice. Do not break it into sections, just provide a single coherent summary.
"""
    return prompt


def get_ai_response(prompt:str):
    response = model.generate_content(contents=prompt)
    return response.text