import pandas as pd


def read_cities_ids_from_csv(file_path):
    df = pd.read_csv(file_path, header=None)
    ids = df.applymap(lambda x: pd.to_numeric(x, errors='coerce')).stack().dropna().astype(int).tolist()
    return ids
