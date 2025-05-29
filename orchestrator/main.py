from fastapi import FastAPI
import requests

app = FastAPI()

API_AGENT_URL = "http://localhost:8001/stock_info"
SCRAPING_AGENT_URL = "http://localhost:8002/earnings_summary"
RETRIEVER_AGENT_URL = "http://localhost:8005/retrieve"
ANALYTICS_AGENT_URL = "http://localhost:8006/analyze"
LANGUAGE_AGENT_URL = "http://localhost:8004/generate_summary"


ASIA_TECH_TICKERS = ["TSM", "INFY", "SSNLF"]

@app.get("/morning_brief")
def get_morning_brief():
    combined_data = []

    for ticker in ASIA_TECH_TICKERS:
        try:
            # API agent
            api_resp = requests.get(API_AGENT_URL, params={"ticker": ticker})
            api_data = api_resp.json()

            # Scraping agent
            scrap_resp = requests.get(SCRAPING_AGENT_URL, params={"ticker": ticker})
            scrap_data = scrap_resp.json()

            combined_data.append({
                "ticker": ticker,
                "market_data": api_data,
                "earnings_summary": scrap_data.get("earnings_table_snippet", "")
            })

        except Exception as e:
            combined_data.append({
                "ticker": ticker,
                "error": str(e)
            })

    #  Call Retriever Agent
    try:
        retrieval_resp = requests.get(RETRIEVER_AGENT_URL, params={"query": "Asia tech risk and earnings", "k": 3})
        retrieval_data = retrieval_resp.json()
        retrieved_chunks = retrieval_data.get("chunks", [])
    except Exception as e:
        retrieved_chunks = [f"Retriever error: {e}"]

    #  Call Analytics Agent
    try:
        analytics_resp = requests.post(ANALYTICS_AGENT_URL, json={"asia_tech_brief": combined_data})
        analytics_data = analytics_resp.json()
    except Exception as e:
        analytics_data = {"error": str(e)}

    return {
        "asia_tech_brief": combined_data,
        "retrieved_context": retrieved_chunks,
        "analytics": analytics_data
    }
