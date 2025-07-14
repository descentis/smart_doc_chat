FROM python:3.11-slim

# System deps
RUN apt-get update && apt-get install -y build-essential python3-dev && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir Cython

WORKDIR /app
COPY backend/requirements.txt .

RUN pip install --no-cache-dir --prefer-binary --timeout=100 --retries=5 -r requirements.txt
COPY backend ./backend

# Expose vectorstore & docs as volumes (optional)
VOLUME /app/vectorstore
VOLUME /app/docs

CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]

