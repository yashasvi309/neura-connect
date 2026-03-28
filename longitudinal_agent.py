import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

FEATHERLESS_API_KEY = os.getenv("FEATHERLESS_API_KEY")
FEATHERLESS_URL = "https://api.featherless.ai/v1/chat/completions"

# Simulated 30-day historical data (Notice how the variance slowly increases over the month)
monthly_variance_data = [
    1.1, 1.0, 1.2, 1.1, 1.3, 1.2, 1.4, 1.5, 1.3, 1.6, 
    1.5, 1.7, 1.8, 1.6, 1.9, 1.8, 2.0, 2.1, 1.9, 2.2, 
    2.1, 2.3, 2.4, 2.2, 2.5, 2.6, 2.4, 2.7, 2.8, 3.1
]

def analyze_patient_history():
    print("🧠 Waking up Neura Connect Predictive Agent...")
    print(f"📊 Analyzing 30 days of TRM variance data: {monthly_variance_data}\n")
    
    prompt = (
        f"You are a neurological AI agent. Analyze this 30-day array of tremor variance scores for a patient: {monthly_variance_data}. "
        "Notice the trend. Provide a concise, 3-sentence clinical prognosis and recommendation. "
        "Do not use markdown. Speak like a doctor."
    )

    headers = {
        "Authorization": f"Bearer {FEATHERLESS_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": "meta-llama/Meta-Llama-3-8B-Instruct",
        "temperature": 0.3,
        "messages": [{"role": "user", "content": prompt}]
    }

    try:
        response = requests.post(FEATHERLESS_URL, headers=headers, json=payload)
        response.raise_for_status()
        analysis = response.json()["choices"][0]["message"]["content"]
        print("🤖 [LLAMA-3 ANALYSIS]:")
        print(analysis)
    except Exception as e:
        print(f"Error reaching AI: {e}")

if __name__ == "__main__":
    analyze_patient_history()