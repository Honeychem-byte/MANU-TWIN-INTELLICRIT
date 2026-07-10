import os
import requests
import streamlit as st

# First try Streamlit Cloud Secrets
try:
    API_KEY = st.secrets["API_KEY"]
    API_URL = st.secrets["API_URL"]

# If running locally, use .env
except Exception:
    from dotenv import load_dotenv

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

    response.raise_for_status()

    data = response.json()

    return data["choices"][0]["message"]["content"]