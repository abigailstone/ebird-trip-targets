"""
eBird Trip Targets

Create spreadsheet of target species across multiple regions using
bar chart data from eBird.
"""
import os
import argparse
from glob import glob

from bar_charts import process_barcharts, create_target_pivot
from life_list import join_life_list
from taxonomy import join_taxonomy

def get_trip_targets(
        data_path: str,
        month: int,
        week: int,
        key: str | None,
        species_only: bool,
        life_list_path: str | None
    ):
    """
    :param data_path: path to bar chart .txt files
    :param month: target month number
    :param week: target week number
    :param key: eBird API key
    :param species_only: include only species (no hybrid, slash, or spuh)
    :param life_list_path: path to life list data (if applicable)
    """

    data_files = glob(f"{data_path}/*.txt")

    # extract frequencies from bar charts
    freqs, sample_sizes = process_barcharts(data_files)

    # create pivot table (species by region)
    pivot = create_target_pivot(freqs, month, week)

    # join taxonomy
    if key:
        result = join_taxonomy(pivot, api_key=key, species_only=species_only)
    else:
        result = pivot

    # join life list data if path is given
    if life_list_path:
        result = join_life_list(result, life_list_path)

    result.to_csv("trip_targets.csv", index=False)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Generate trip targets from eBird bar chart files."
    )

    parser.add_argument(
        "data_path", type=str,
        help="Path to directory of barchart .txt files for target regions"
    )

    parser.add_argument(
        "month", type=int,
        help="Month (1-12) for which to calculate targets"
    )

    parser.add_argument(
        "week", type=int,
        help="Week of month (1-4) for which to calculate targets"
    )

    parser.add_argument(
        "--sort", type=bool,
        default=True, help="Whether to sort by taxonomy (requires eBird API key)"
    )

    parser.add_argument(
        "--species-only", type=bool,
        default=True,
        help="Whether to filter to species only. If False, results include hybrid, slash, and spuh."
    )

    parser.add_argument(
        "--life-list", type=str,
        default=None,
        help="Path to life list .csv"
    )

    args = parser.parse_args()

    # look for API key
    api_key = os.getenv("EBIRD_API_KEY", None) if args.sort else None

    get_trip_targets(
        args.data_path,
        args.month, args.week,
        api_key,
        args.species_only,
        args.life_list
    )
