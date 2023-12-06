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

pd.set_option("display.max_rows", None)  # for better display
request = {"code1": "shA", "code2": "W"}  # for testing requests

code1_mask = df["code1"].str.startswith(request["code1"], na=False)
code2_mask = df["code2"].str.startswith(request["code2"], na=False)
df_copy_with_general_codes = df[code1_mask & code2_mask]
df_copy_with_general_codes.loc[:, "code1"] = request["code1"]
df_copy_with_general_codes.loc[:, "code2"] = request["code2"]
df_copy_with_general_codes = df_copy_with_general_codes[
    ["code1", "code2", "source"]
].drop_duplicates()
grouped_df_copy = (
    df_copy_with_general_codes.groupby(["code1", "code2"])["source"]
    .agg(list)
    .to_dict()
)
