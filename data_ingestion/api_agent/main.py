from fastapi import FastAPI
import yfinance as yf

app = FastAPI()

@app.get("/stock_info")
def get_stock_info(ticker: str):
    stock = yf.Ticker(ticker)
    hist = stock.history(period="2d")
    
    if hist.empty:
        return {"error": "No data found for ticker"}
    
    return {
        "ticker": ticker,
        "latest_close": hist['Close'][-1],
        "previous_close": hist['Close'][-2]
    }
