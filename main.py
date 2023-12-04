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
mask_one = bitCodeOne == True
bitCodeZero = (df["bitCode"] == 0).astype(object)
mask_zero = bitCodeZero == True
bitCodeOne[mask_one] = np.select(conditions, ["A", "B", "BpA"], default=np.nan)
bitCodeZero[mask_zero] = np.select(conditions, ["H", "T", "TpH"], default=np.nan)
df["siCode"] = np.where(df["bitCode"] == 1, bitCodeOne, bitCodeZero)
