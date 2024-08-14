import pandas as pd
from pandas.errors import EmptyDataError


def read_cities_ids_from_csv(file_path):
    try:
        df = pd.read_csv(file_path, header=None)
        if df.empty:
            return []
        ids = df.applymap(lambda x: pd.to_numeric(x, errors='coerce')).stack().dropna().astype(int).tolist()
        return ids
    except EmptyDataError:
        return []
