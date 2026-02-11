from openai import OpenAI
import os
import json
from config import OPENAI_API_KEY

# Set OpenAI API key
os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY
client = OpenAI(api_key=OPENAI_API_KEY)

def interpret_query(user_query):
    prompt = f"""
You are a BI query parser.

Convert this business question into structured intent.

Query: "{user_query}"

Return ONLY valid JSON:

{{
  "sector": "",
  "time_range": "this_quarter | this_month | this_year | all",
  "metrics": ["revenue", "pipeline", "forecast", "sector", "risk"]
}}

Rules:
- If query mentions revenue, include "revenue"
- If query mentions pipeline, include "pipeline"
- If query mentions forecast/expected, include "forecast"
- If query mentions sector, include "sector"
- If query mentions risk, include "risk"
- If query mentions quarter, set time_range="this_quarter"
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role":"user","content":prompt}],
            temperature=0
        )

        try:
            return json.loads(response.choices[0].message.content)
        except json.JSONDecodeError:
            print(f"JSON parse error. Raw response: {response.choices[0].message.content}")
            return {
                "sector": "",
                "time_range": "all",
                "metrics": ["revenue"]
            }
    except Exception as e:
        print(f"OpenAI API Error: {e}. Using demo response.")
        # Return mock response for demo
        return {
            "sector": "tech",
            "time_range": "this_quarter",
            "metrics": ["pipeline", "revenue", "forecast"]
        }
