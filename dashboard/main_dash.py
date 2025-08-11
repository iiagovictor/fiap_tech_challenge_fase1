import os
import sys
import streamlit as st
import pandas as pd
from app.models.databases.base import SessionLocal
from app.models.databases.logs import Log

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class RequestDashboard:

    def __init__(self):
        self.df = self.load_data()

    def load_data(self):
        try:
            session = SessionLocal()
            logs = session.query(Log).all()
            data = [
                {
                    "id": log.id,
                    "time": log.time,
                    "status_code": log.status_code,
                    "endpoint": log.endpoint,
                    "message": log.message,
                    "type": log.type,
                    "method": log.method,
                    "latency": log.latency
                }
                for log in logs
            ]
            df = pd.DataFrame(data)
            return df
        except Exception as e:
            st.error(f"Erro ao carregar dados do banco: {e}")
            return pd.DataFrame()

    def num_requests_per_endpoint(self):
        if not self.df.empty:
            return (
                self.df['endpoint']
                .value_counts()
                .reset_index(name='count')
                .rename(columns={'index': 'endpoint'})
            )
        return pd.DataFrame()

    def status_code_distribution(self):
        if not self.df.empty:
            return (
                self.df['status_code']
                .value_counts()
                .reset_index(name='count')
                .rename(columns={'index': 'status_code'})
            )
        return pd.DataFrame()

    def average_latency_per_endpoint(self):
        if not self.df.empty:
            return (
                self.df.groupby('endpoint')['latency']
                .mean()
                .reset_index()
                .rename(columns={'latency': 'average_latency'})
            )
        return pd.DataFrame()

    def total_requests_over_time(self):
        if not self.df.empty:
            self.df['time'] = pd.to_datetime(self.df['time'])
            return (
                self.df.set_index('time')
                .resample('D')
                .size()
                .reset_index(name='count')
            )
        return pd.DataFrame()


def main():
    st.title("Dashboard de Requisições")

    dash = RequestDashboard()

    col2, col3 = st.columns(2)
    col4, col5 = st.columns(2)

    with col2:
        teste = dash.num_requests_per_endpoint()
        st.subheader("Número de requisições por endpoint")
        st.bar_chart(teste, x='endpoint', y='count')

    with col3:
        st.subheader("Distribuição dos códigos de status")
        status_dist = dash.status_code_distribution()
        st.bar_chart(status_dist, x='status_code', y='count')

    with col4:
        st.subheader("Latência média por endpoint")
        avg_latency = dash.average_latency_per_endpoint()
        st.bar_chart(avg_latency, x='endpoint', y='average_latency')

    with col5:
        st.subheader("Total de requisições ao longo do tempo")
        total_requests = dash.total_requests_over_time()
        st.line_chart(total_requests, x='time', y='count')


if __name__ == "__main__":
    main()
    