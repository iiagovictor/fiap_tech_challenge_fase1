import pandas as pd

def get_csv_data(path_file):
    try:
        df = pd.read_csv(path_file, sep=';')
        #A coluna de data não vinha com o formato de data, vinha como objetc
        df['created_at'] = pd.to_datetime(df['created_at'], errors='coerce')
        #Evitando que tenham valores negativos nas colunas que tao como float
        df['price_including_tax'] = df['price_including_tax'].apply(lambda x: abs(x))
        df['price_excluding_tax'] = df['price_excluding_tax'].apply(lambda x: abs(x))
        df['tax'] = df['tax'].apply(lambda x: abs(x))
        #Verificando, os campos que vinham com valores vazios era o de categoria
        df['category'] = df['category'].fillna("--")
    except Exception as error:
        return error
    return df

#Aplicar um try para caso não seja possível fazer o filtro
def get_unique_items(df: pd.DataFrame, column_name: str):
    try:
        if column_name not in  df.columns:
            raise ValueError(f"A coluna '{column_name}' não existe na Base de dados")

        unique_items = df[column_name].drop_duplicates().tolist()
        return unique_items        
    except Exception as error:
        return error

# def get_only_categories(df):
#     try:
#         df = df["category"].drop_duplicates()
#         lista_categorias = df.tolist()
#     except Exception as error:
#         return  error
#     return lista_categorias

# def get_only_books(df):
#     try:
#         df = df["title"].drop_duplicates()
#         lista_livros = df.tolist()
#     except Exception as error:
#         return  error
#     return lista_livros

def get_rating(df, name_column,required_number, default_response):
    rating = int(df[name_column].value_counts().get(required_number,default_response))
    return rating