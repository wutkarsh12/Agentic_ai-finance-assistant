# AI Finance Assistant 

A modular, multi-agent AI system that delivers **spoken Asia tech market briefs** using FastAPI microservices, Google Gemini LLM, FAISS vector search, and Streamlit UI.


##  Use Case: Morning Market Brief

-"What’s our risk exposure in Asia tech stocks today, and highlight any earnings surprises?"

The system responds verbally:
-"Today, your Asia tech allocation is 22% of AUM. TSMC beat estimates by 4%, Samsung missed by 2%. Sentiment is neutral due to rising yields."

---

##  Architecture Diagram

```
[Streamlit UI]
     ↓
[Voice Input (optional)]
     ↓
[Orchestrator (FastAPI)]
     ↳ API Agent (8001)        
     ↳ Scraping Agent (8002)
     ↳ Retriever Agent (8005)
     ↳ Analytics Agent (8006)
     ↳ Language Agent (8004) ➔ Gemini LLM
     ↳ Voice Output (pyttsx3)
```


##  Setup & Run

###  Prerequisites

* Python 3.9+
* Google Gemini API Key

### ⚙ Installation

```bash
# 1. Clone the repo
https://github.com/yourusername/ai-finance-agent
cd ai-finance-agent

# 2. Set up virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Add your .env file
cp .env.example .env
# Edit .env to include your Gemini key
```

### Run Agents

```bash
# From project root:
uvicorn data_ingestion.api_agent.main:app --port 8001
uvicorn data_ingestion.scraping_agent.main:app --port 8002
uvicorn retriever_agent.main:app --port 8005
uvicorn analytics_agent.main:app --port 8006
uvicorn language_agent.main:app --port 8004
uvicorn orchestrator.main:app --port 8003
```

###  Launch Streamlit App

```bash
streamlit run streamlit_app/app.py
```

---

## Frameworks & Toolkits

| Component   | Tool/Library          |
| ----------- | --------------------- |
| LLM         | Google Gemini         |
| API Server  | FastAPI               |
| TTS         | pyttsx3               |
| Embeddings  | sentence-transformers |
| Vector DB   | FAISS                 |
| UI          | Streamlit             |
| Environment | python-dotenv         |

---

## Bonus

* Multi-agent orchestration
* RAG (Retriever-Augmented Generation)
* Spoken summary

---

##  Deployment

Deployed on Streamlit Community Cloud:


---

## 📃 License

MIT License

---

## ✍️ Credits

> Reach out if you want help deploying or debugging!