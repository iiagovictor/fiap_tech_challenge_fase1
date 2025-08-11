run-dashboard:
	PYTHONPATH=. streamlit run dashboard/main_dash.py

run-api:
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

lint:
	flake8 app dashboard
