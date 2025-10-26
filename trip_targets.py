"""
eBird Trip Targets

Create spreadsheet of target species across multiple regions using
bar chart data from eBird.
"""
import os
import argparse
from glob import glob

from bar_charts import process_barcharts, create_target_pivot, join_taxonomy

def get_trip_targets(data_path: str, month: int, week: int, key: str | None):
    """
    :param data_path: path to bar chart .txt files
    :param month: target month number (int)
    :param week: target week number (int)
    """

    data_files = glob(f"{data_path}/*.txt")

    # extract frequencies from bar charts
    freqs, sample_sizes = process_barcharts(data_files)

    # create pivot table (species by region)
    pivot = create_target_pivot(freqs, month, week)

    # join taxonomy
    if key:
        result = join_taxonomy(pivot, api_key=key)
    else:
        result = pivot

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

    args = parser.parse_args()

    # look for API key
    api_key = os.getenv("EBIRD_API_KEY", None) if args.sort else None

    get_trip_targets(args.data_path, args.month, args.week, api_key)
