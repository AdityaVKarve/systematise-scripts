import openai
from dotenv import load_dotenv
import os

load_dotenv()

openai.api_key = os.getenv("OPENAPI_KEY")

def read_file(filepath):
    with open(filepath, 'r') as f:
        return f.read()

def generate_analysis(process_events_csv, bookkeeping_csv):
    proc_events_content = read_file(process_events_csv)
    bookkeeping_content = read_file(bookkeeping_csv)

    prompt = f"""
You are a business analyst AI.

Analyze the following data:

1) Process and Events log CSV:
{proc_events_content}

2) Revenue and Bookkeeping CSV:
{bookkeeping_content}

Based on this data, provide:
- Summary of revenue and financial performance
- Operational performance insights
- Recommendations for improvement
"""
    print([
            {"role": "system", "content": "You are an insightful business analyst."},
            {"role": "user", "content": prompt}
        ])
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an insightful business analyst."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=1000,
    )

    return response.choices[0].message.content

if __name__ == "__main__":
    analysis = generate_analysis("processes_events.csv", "bookkeeping.csv")
    print("AI Analysis & Recommendations:\n", analysis)
