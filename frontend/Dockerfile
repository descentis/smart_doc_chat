FROM python:3.11-slim

WORKDIR /app
COPY frontend/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY frontend ./frontend

EXPOSE 8501

# Streamlit config (avoid telemetry prompt)
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0
ENV STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

CMD ["streamlit", "run", "frontend/app.py"]

