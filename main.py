import pandas as pd
import numpy as np


def add_bitcode_column(df: pd.DataFrame) -> pd.DataFrame:
    df["bitCode"] = (df["source"] == "S1").astype(int)
    return df


def add_sicode_column(df: pd.DataFrame) -> pd.DataFrame:
    conditions = [
        ((df["code3"] == "AP") | (df["code3"] == "AH")),
        (df["code3"] == "PRD"),
        (df["code3"] == "YLD"),
    ]
    bit_code_one = (df["bitCode"] == 1).astype(object)
    bit_code_zero = (df["bitCode"] == 0).astype(object)
    bit_code_one[bit_code_one] = np.select(
        conditions, ["A", "B", "BpA"], default=np.nan
    )
    bit_code_zero[bit_code_zero] = np.select(
        conditions, ["H", "T", "TpH"], default=np.nan
    )
    df["siCode"] = np.where(df["bitCode"] == 1, bit_code_one, bit_code_zero)
    return df


def get_code_masks(df: pd.DataFrame, request: dict):
    code1_mask = df["code1"].str.startswith(request["code1"], na=False)
    code2_mask = df["code2"].str.startswith(request["code2"], na=False)
    return code1_mask, code2_mask


def group_codes_with_sources(df: pd.DataFrame, request: dict) -> dict:
    code1_mask, code2_mask = get_code_masks(df, request)
    df_copy_with_general_codes = df[code1_mask & code2_mask][
        ["code1", "code2", "source"]
    ]
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
    return grouped_df_copy


def get_values_for_sources(
    df: pd.DataFrame, sources: list, request: dict
) -> list:
    code1_mask, code2_mask = get_code_masks(df, request)
    result = []

    for source in sources:
        source_mask = df["source"] == source
        suitable_data = df[code1_mask & code2_mask & source_mask][
            ["updateDate", "code1", "code2", "code3", "value", "siCode"]
        ]
        result.append(
            {
                (
                    request["code1"],
                    request["code2"],
                    source,
                ): suitable_data.values.tolist()
            }
        )
    return result


def main(sample_request: dict[str, str], file_name: str) -> None:
    df = pd.read_csv(file_name)
    df = add_bitcode_column(df)
    df = add_sicode_column(df)
    grouped_df = group_codes_with_sources(df, sample_request)
    result = get_values_for_sources(
        df, list(grouped_df.values())[0], sample_request
    )

    print("First output\n", grouped_df)
    print("\nSecond output")

    for data_for_source in result:
        print(data_for_source)


if __name__ == "__main__":
    main({"code1": "shC", "code2": "C"}, "db_table.csv")
