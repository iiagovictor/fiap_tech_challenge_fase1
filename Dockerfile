FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY app /app/app

COPY banco.db /app/
COPY alembic.ini /app/
COPY modelo_recomendacao.pkl /app/
COPY dashboard /app/dashboard
COPY nginx.conf /etc/nginx/nginx.conf

RUN apt-get update && apt-get install -y nginx && rm -rf /var/lib/apt/lists/*

EXPOSE 80

CMD bash -c "uvicorn app.main:app --host 0.0.0.0 --port 8000 & streamlit run /app/dashboard/main_dash.py --server.port 8501 --server.address 127.0.0.1 & nginx -g 'daemon off;'"
