import os
import google.generativeai as genai
from dotenv import load_dotenv
from typing import List, Dict, Optional

# Load env variables immediately
load_dotenv()

class AIContext:
    """Singleton to handle AI configuration and shared resources."""
    _configured = False

    @classmethod
    def setup(cls):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            return False
        
        genai.configure(api_key=api_key)
        cls._configured = True
        return True

    @classmethod
    def is_active(cls):
        return cls._configured

def categorize_transaction(description: str, amount: float) -> str:
    """
    Uses Gemini-Pro to intelligently categorize a transaction description.
    Returns a single category string.
    """
    if not AIContext.is_active():
        if not AIContext.setup():
            return "Uncategorized (No AI Key)"

    model = genai.GenerativeModel('gemini-pro')
    
    # Detailed system instruction for deterministic output
    prompt = f"""
    Role: Financial Data Processor
    Task: Categorize the transaction below into exactly one of these categories:
    [Groceries, Dining, Transport, Utilities, Rent, Entertainment, Health, Shopping, Income, Transfer, Subscription]
    
    Rules:
    1. If unsure, choose 'Shopping'.
    2. Output ONLY the category word. No punctuation.
    3. Context: Amount is ${amount}.
    
    Transaction Description: "{description}"
    """
    
    try:
        # Temperature 0.1 ensures consistent, non-creative answers
        response = model.generate_content(
            prompt, 
            generation_config=genai.types.GenerationConfig(temperature=0.1)
        )
        return response.text.strip()
    except Exception as e:
        # Fail gracefully to allow the app to keep running
        print(f"  [!] AI Categorization failed: {e}")
        return "Uncategorized"

def get_spending_advice(monthly_summary: Dict[str, float]) -> str:
    """
    Sends aggregated data to Gemini for a 'Financial Health Check'.
    """
    if not AIContext.is_active():
        if not AIContext.setup():
            return "AI Analysis unavailable. Please set GEMINI_API_KEY in .env."

    model = genai.GenerativeModel('gemini-pro')

    # Convert dictionary to a readable string list for the LLM
    summary_text = "\n".join([f"- {k}: ${v:.2f}" for k, v in monthly_summary.items()])

    prompt = f"""
    You are a brutal but helpful financial advisor. 
    Analyze the following monthly spending summary for a user.
    
    Spending Data:
    {summary_text}
    
    Task:
    1. Identify the largest expense category.
    2. Provide 1 specific, actionable tip to save money based on these numbers.
    3. Keep the tone professional but direct. Max 100 words.
    """

    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Could not generate insights: {e}"