import pandas as pd

def get_csv_data(path_file):
    df = pd.read_csv(path_file, sep=';')
    return df
