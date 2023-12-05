import pandas as pd
import numpy as np


df = pd.read_csv("db_table.csv")
df["bitCode"] = (df["source"] == "S1").astype(int)

conditions = [
    ((df["code3"] == "AP") | (df["code3"] == "AH")),
    (df["code3"] == "PRD"),
    (df["code3"] == "YLD"),
]
bitCodeOne = (df["bitCode"] == 1).astype(object)
bitCodeZero = (df["bitCode"] == 0).astype(object)
bitCodeOne[bitCodeOne] = np.select(
    conditions, ["A", "B", "BpA"], default=np.nan
)
bitCodeZero[bitCodeZero] = np.select(
    conditions, ["H", "T", "TpH"], default=np.nan
)
df["siCode"] = np.where(df["bitCode"] == 1, bitCodeOne, bitCodeZero)

unique_combinations = df[["code1", "code2", "source"]].drop_duplicates()
possible_requests = (
    unique_combinations.groupby(["code1", "code2"])["source"]
    .agg(list)
    .reset_index()
)
sources_for_requests = dict(
    zip(
        zip(possible_requests["code1"], possible_requests["code2"]),
        possible_requests["source"],
    )
)

data_for_requests = dict(
    zip(
        zip(
            unique_combinations["code1"],
            unique_combinations["code2"],
            unique_combinations["source"],
        ),
        zip(
            df["updateDate"],
            df["code1"],
            df["code2"],
            df["code3"],
            df["value"],
            df["siCode"],
            df["bitCode"],
        ),
    )
)
