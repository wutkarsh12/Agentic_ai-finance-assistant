import os
import google.generativeai as genai
from dotenv import load_dotenv
from fastapi import FastAPI, Request

app = FastAPI()

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel(model_name="models/gemini-1.5-flash-latest")

@app.post("/generate_summary")
async def generate_summary(request: Request):
    data = await request.json()
    input_data = data.get("asia_tech_brief", data.get("received", []))
    context = data.get("retrieved_context", [])
    analytics = data.get("analytics", {})

    if not input_data:
        return {"error": "No data received"}

    summary_lines = []
    for item in input_data:
        if "error" in item:
            continue
        ticker = item.get("ticker", "UNKNOWN")
        market = item.get("market_data", {})
        earnings = item.get("earnings_summary", "No earnings info.")
        latest = market.get("latest_close", "N/A")
        previous = market.get("previous_close", "N/A")

        summary_lines.append(
            f"{ticker} closed at {latest}, previous: {previous}. Earnings: {earnings}"
        )

    context_text = "\n\n".join(context)
    exposure = analytics.get("asia_exposure_percent", "N/A")
    earnings_events = "\n".join(analytics.get("earnings_surprises", []))

    prompt = (
        f"Today, Asia tech exposure is {exposure}% of AUM.\n"
        f"Earnings events:\n{earnings_events}\n\n"
        f" Context:\n{context_text}\n\n"
        f" Market Summary:\n" + "\n".join(summary_lines)
    )

    try:
        response = model.generate_content(prompt)
        return {"summary": response.text.strip()}
    except Exception as e:
        return {"error": str(e)}
