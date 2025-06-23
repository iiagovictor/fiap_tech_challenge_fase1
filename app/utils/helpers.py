import pandas as pd

def get_csv_data(path_file):
    df = pd.read_csv(path_file, sep=';')
    #A coluna de data não vinha com o formato de data, vinha como objetc
    df['created_at'] = pd.to_datetime(df['created_at'], errors='coerce')
    #Evitando que tenham valores negativos nas colunas que tao como float
    df['price_including_tax'] = df['price_including_tax'].apply(lambda x: abs(x))
    df['price_excluding_tax'] = df['price_excluding_tax'].apply(lambda x: abs(x))
    df['tax'] = df['tax'].apply(lambda x: abs(x))
    #Verificando, os campos que vinham com valores vazios era o de categoria
    df['category'] = df['category'].fillna("--")
    return df

def get_only_categories(df):
    df = df["category"].drop_duplicates()
    return df