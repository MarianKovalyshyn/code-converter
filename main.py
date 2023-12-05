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

possible_requests = (
    df[["code1", "code2", "source"]]
    .drop_duplicates()
    .groupby(["code1", "code2"])["source"]
    .agg(list)
    .reset_index()
)
sources_for_requests = dict(
    zip(
        zip(possible_requests["code1"], possible_requests["code2"]),
        possible_requests["source"],
    )
)
print(len(sources_for_requests))
