import pandas as pd
import os

# Default paths
path_train = "data/OHSUMED/train-00000-of-00001.parquet"
path_train = os.path.abspath(path_train)

path_test = "data/OHSUMED/test-00000-of-00001.parquet"
path_test = os.path.abspath(path_test)


def load_parquet_as_df(data_path: str) -> pd.DataFrame:
    df = pd.read_parquet(data_path)
    return df

