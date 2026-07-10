import os
from urllib import response
import requests
from dotenv import load_dotenv

# Load variables from .env
load_dotenv()

API_KEY = os.getenv("API_KEY")
API_URL = os.getenv("API_URL")


def ask_llm(question, context):

    headers = {
        "Content-Type": "application/json",
        "api-key": API_KEY
    }

    payload = {
        "messages": [
            {
                "role": "system",
                "content": """
You are an AI Plant Engineer.

You are an expert in:
- Root Cause Analysis
- Process Safety
- Predictive Maintenance
- Process Historian
- Refinery Operations
- Digital Twin
- Equipment Diagnostics

Always answer in the following format:

1. Root Cause
2. Evidence
3. Confidence (%)
4. Recommended Actions
5. Preventive Actions
"""
            },
            {
                "role": "user",
                "content": f"""
Question:
{question}

Plant Data:
{context}
"""
            }
        ],
        "temperature": 0.2,
        "max_completion_tokens": 1000
    }

    response = requests.post(
        API_URL,
        headers=headers,
        json=payload,
        timeout=60
    )

    print("Status Code:", response.status_code)
    print("Response:")
    print(response.text)

    response.raise_for_status()

    data = response.json()

    return data["choices"][0]["message"]["content"]