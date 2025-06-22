import pandas as pd
import numpy as np

def get_csv_data(path_file):
    df = pd.read_csv(path_file, sep=';')
    df.fillna("",inplace=True)
    df = df["category"].drop_duplicates()
    return df
