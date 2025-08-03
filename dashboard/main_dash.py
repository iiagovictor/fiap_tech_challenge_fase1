import streamlit as st
import pandas as pd
import os


class BookDashboard:
    def __init__(self, csv_path, delimiter=";"):
        self.csv_path = csv_path
        self.delimiter = delimiter
        self.df = self.load_data()

    def load_data(self):
        try:
            df = pd.read_csv(self.csv_path, delimiter=self.delimiter)
        except Exception as e:
            st.error(f"Erro ao ler CSV: {e}")
            df = pd.DataFrame()
        return df

    def livro_categoria(self):
        if not self.df.empty:
            return self.df.groupby('category').size() \
                .reset_index(name='quantity')
        return pd.DataFrame()

    def preco_medio_categoria(self):
        if not self.df.empty:
            return self.df.groupby('category')['price_including_tax'].mean() \
                .reset_index(name='average_price')
        return pd.DataFrame()


def main():
    dashboard = BookDashboard(os.path.join(os.path.dirname(__file__), "../app/data/books.csv"))  # noqa: E501
    livro_categoria = dashboard.livro_categoria()
    preco_categoria = dashboard.preco_medio_categoria()

    st.title("Dashboard de Livros")
    st.subheader("Quantidade de livros por categoria")
    st.bar_chart(livro_categoria, x='category', y='quantity')

    st.subheader("Preço médio por categoria")
    st.bar_chart(preco_categoria, x='category', y='average_price')


if __name__ == "__main__":
    main()
