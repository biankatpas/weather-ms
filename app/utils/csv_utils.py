import pandas as pd


def read_cities_ids_from_csv(file_path, header=None):
    df = pd.read_csv(file_path, header=header)
    ids = df[0].astype(str).str.split(',').explode().str.strip().dropna().tolist()

    return ids
