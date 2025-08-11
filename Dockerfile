FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY app /app/app

COPY banco.db /app/
COPY alembic.ini /app/
COPY modelo_recomendacao.pkl /app/
COPY dashboard /app/dashboard

EXPOSE 8000 8501

RUN ls -l /app/dashboard

CMD uvicorn app.main:app --host 0.0.0.0 --port 8000 & streamlit run /app/dashboard/main_dash.py --server.port 8501 --server.address 0.0.0.0
