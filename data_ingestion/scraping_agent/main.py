from fastapi import FastAPI
import requests
from bs4 import BeautifulSoup

app = FastAPI()

@app.get("/earnings_summary")
def get_earnings_summary(ticker: str):
    url = f"https://finance.yahoo.com/quote/{ticker}/analysis"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find earnings estimate table
        tables = soup.find_all("table")
        if not tables:
            return {"error": "No earnings data found"}

        # Just return the first table's text as a demo
        return {
            "ticker": ticker,
            "earnings_table_snippet": tables[0].get_text()
        }

    except Exception as e:
        return {"error": str(e)}
