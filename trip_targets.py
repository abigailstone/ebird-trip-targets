"""
eBird Trip Targets

Create spreadsheet of target species across multiple regions using
bar chart data from eBird.
"""
import argparse
from glob import glob

from bar_charts import process_barcharts, create_target_pivot


def get_trip_targets(data_path: str, month: int, week: int):
    """
    :param data_path: path to bar chart .txt files
    :param month: target month number (int)
    :param week: target week number (int)
    """

    data_files = glob(f"{data_path}/*.txt")

    freqs, sample_sizes = process_barcharts(data_files)

    pivot = create_target_pivot(freqs, month, week)

    pivot.to_csv("trip_targets.csv")

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

    args = parser.parse_args()

    get_trip_targets(args.data_path, args.month, args.week)
