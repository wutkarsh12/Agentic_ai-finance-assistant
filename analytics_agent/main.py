from fastapi import FastAPI, Request

app = FastAPI()

AUM_TOTAL = 1_000_000_000  # $1B
ASIA_TECH_ALLOC = {
    "TSM": 220_000_000,
    "INFY": 80_000_000,
    "SSNLF": 50_000_000
}

@app.post("/analyze") 
async def analyze(request: Request):
    data = await request.json()
    asia_data = data.get("asia_tech_brief", [])

    # 1. Exposure Calculation
    exposure_usd = sum(ASIA_TECH_ALLOC.values())
    exposure_percent = round((exposure_usd / AUM_TOTAL) * 100, 2)

    # 2. Earnings Surprise Detection
    surprises = []
    for item in asia_data:
        ticker = item.get("ticker")
        summary = item.get("earnings_summary", "")

        try:
            if "Avg. Estimate" in summary and "Year Ago EPS" in summary:
                parts = summary.split("Avg. Estimate")[1]
                estimate = float(parts.split()[0])

                parts2 = summary.split("Year Ago EPS")[1]
                actual = float(parts2.split()[0])

                diff = round(((actual - estimate) / estimate) * 100, 2)
                if diff >= 1:
                    surprises.append(f"{ticker} beat estimates by {diff}%")
                elif diff <= -1:
                    surprises.append(f"{ticker} missed estimates by {abs(diff)}%")
            else:
                surprises.append(f"{ticker}: insufficient earnings data")
        except Exception as e:
            surprises.append(f"{ticker}: error parsing data")

    return {
        "asia_exposure_percent": exposure_percent,
        "earnings_surprises": surprises
    }
