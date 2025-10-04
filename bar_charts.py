"""
Functions for processing eBird bar charts and creating pivot tables by region
"""

from io import StringIO
import pandas as pd

def process_barcharts(file_paths: list[str]) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    :param file_paths: list of file paths for bar chart files
    :return freqs: DataFrame of species frequencies by week for each region
    :return samples: DataFrame of sample sizes by week for each region
    """

    # accumulate frequency data and sample sizes for each region
    freq_list = []
    sample_size = {}

    # create month and week index
    mw = pd.DataFrame([(m, w) for m in range(1, 13) for w in range(1, 5)], columns=["month", "week"])
    week_vars = [f"{m}_{w}" for m, w in zip(mw["month"], mw["week"])]

    # new column names using month and week
    col_names = ["Species"] + week_vars + ["blank"]

    for fp in file_paths:

        # read the bar chart .txt file
        with open(fp, "r", encoding='utf-8') as f:
            lines = f.readlines()

        # extract region name from file path
        region = fp.split('/')[-1].split('_')[1]

        # extract sample size line
        sample_size[region] = pd.Series(lines[14].split('\t'))

        # extract frequencies
        df = pd.read_csv(
            StringIO("\n".join(lines[15:])),
            sep="\t",
            header=None,
            names=col_names,
            dtype={col: "float" for col in week_vars},
            na_values=["", " "]
        )

        # Add region, extract common and scientific names, etc.
        df["Region"] = region
        df["Species"] = df["Species"].str.replace('(<em class="sci">', ",")
        df["Species"] = df["Species"].str.replace('</em>)', "")
        df[["Com_Name", "Sci_Name"]] = pd.DataFrame(df["Species"].str.split(',').to_list())
        df["Com_Name"] = df["Com_Name"].str.strip()

        # append to lists
        freq_list.append(df)

    # compile into DataFrames
    freqs = pd.concat(freq_list)
    samples = pd.DataFrame(sample_size)

    return freqs, samples

def create_target_pivot(freqs: pd.DataFrame, month: int, week: int) -> pd.DataFrame:
    """
    :param freqs: DataFrame of species frequencies
    :param month: target month (int)
    :param week: target week number (int)
    :return: DataFrame of target species by region
    """

    # target column name
    col = f"{month}_{week}"

    # pivot table
    data = freqs[["Region", "Com_Name", "Sci_Name", col]]
    pivot = data.pivot(index=["Com_Name", "Sci_Name"], columns="Region", values=col).reset_index()

    return pivot
