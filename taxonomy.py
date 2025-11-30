"""
Functions for reading taxonomy data from the eBird API
and joining with region pivot tables
"""
import pandas as pd
from ebird.api.requests import get_taxonomy


def join_taxonomy(pivot: pd.DataFrame, api_key: str, species_only: bool) -> pd.DataFrame:
    """
    :param pivot: DataFrame of frequencies by region and species
    :param api_key: eBird API key
    :param species_only: include only species (no hybrid, slash, or spuh) in results
    :return: DataFrame with taxonomy ordering from eBird API
    """
    # fetch taxonomy from eBird API
    tax_response = get_taxonomy(api_key)
    taxonomy = pd.json_normalize(tax_response)

    # join relevant columns to frequency outpt
    tax = taxonomy[["sciName", "category", "taxonOrder"]].set_index("sciName")
    joined = pivot.set_index("Sci_Name").join(tax).reset_index()

    # sort by taxonomic order
    joined = joined.sort_values("taxonOrder")

    # keep only "species" entries
    if species_only:
        joined = joined[joined["category"] == "species"]

    joined = joined.drop(columns=["category", "taxonOrder"])

    return joined
