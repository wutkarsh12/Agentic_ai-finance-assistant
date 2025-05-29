# Use official Python image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Copy files
COPY . .

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose ports for all services (if testing locally)
EXPOSE 8001 8002 8003 8004 8005 8006 8501

# Use gunicorn for orchestrator, Streamlit runs separately
CMD ["sh", "-c", "uvicorn orchestrator.main:app --host 0.0.0.0 --port 8003 & streamlit run streamlit_app/app.py --server.port=8501 --server.address=0.0.0.0"]

