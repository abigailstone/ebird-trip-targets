"""
Functions for reading life list data and joining with region pivot tables
"""
import pandas as pd
import numpy as np

def join_life_list(pivot: pd.DataFrame, life_list: str | None) -> pd.DataFrame:
    """
    Join life list information to the regional pivot table

    :param pivot: DataFrame of frequencies by region and species
    :param lifelist: path to life list file
    :return: DataFrame of regional pivot joined with life list data
    """

    life = pd.read_csv(f"{life_list}")
    life = life[["Scientific Name", "Countable"]].set_index("Scientific Name")

    # join the life list and use an indicator column
    joined = pd.merge(
        pivot,
        life,
        left_on="Sci_Name",
        right_on="Scientific Name",
        how="left",
        indicator=True
    )

    joined["on_life_list"] = np.where(joined["_merge"] == "both", True, False)

    joined = joined.drop(columns=["_merge", "Countable"])

    return joined
