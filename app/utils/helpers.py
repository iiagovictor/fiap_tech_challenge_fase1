import pandas as pd

def get_csv_data(path_file):
    df = pd.read_csv(path_file, sep=';')
    df.fillna("",inplace=True)
    return df

def get_only_categories(df):
    df = df["category"].drop_duplicates()
    return df