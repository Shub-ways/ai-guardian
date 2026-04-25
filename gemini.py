import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-2.5-flash")


def analyze_text_with_gemini(text):
    prompt = f"""
You are a cybersecurity AI.

Analyze the following message and classify it as:
Safe, Suspicious, or Scam.

Also provide:
1. Risk score (0-100)
2. 2-3 clear reasons

Message:
{text}

Return in JSON format:
{{
  "verdict": "...",
  "risk_score": ...,
  "reasons": ["...", "..."]
}}
"""

    response = model.generate_content(prompt)

    return response.text