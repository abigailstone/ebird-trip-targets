# eBird Trip Targets

Python tool for generating a spreadsheet of target species across multiple regions, useful for trip planning.

## Setup
- Install packages from requirements.txt using your favorite package management tool
- If you want to enable taxonomic sorting using the latest taxonomy from eBird, set an [eBird API key](https://support.ebird.org/en/support/solutions/articles/48000838205-download-ebird-data#API) as an environment variable:

```
$ export EBIRD_API_KEY="your-api-key-here"
```

## Basic usage

1. Download eBird bar charts for each target region:

    a. Navigate to the eBird region page for each region that you'll visit. ([Example](https://ebird.org/region/US-VT-001))

    b. Select "Bar Charts" from the "Explore..." part of the left sidebar.

    c. Scroll all the way to the bottom and click "Download Histogram Data"

    d. Place all your downloaded bar charts in a single directory

    **NOTE**: Bar chart files should be *unmodified*, since the processing scripts expect the default formatting and file-naming from eBird.


2. Run the script, specifying the path to the directory containing the bar chart files, and the month and year of your trip.

    ```
    $ python trip_targets.py [path] [month] [week]
    ```

    For example, if you will be visiting your target regions in the second week of May:

    ```
    $ python trip_targets.py /path/to/barcharts/ 5 2
    ```

## Additional features

The following command line arguments are supported:

- `--sort`: Taxonomic sorting is enabled by default. If you wish to skip taxonomic sorting, use `--sort False`. If sorting is disabled (or if you do not have an API key saved as an environment variable), the results will appear in the order in which they appear in the first bar chart file, with additional species found in subsequent bar charts appended to the end.

- `--species-only`: By default, only the "species" taxonomy category is returned. If you wish to have hybrids, slashes, and spuhs included in the output, set `--species_only` to False. If sorting is disabled or no API key is found, all taxonomy categories will be included in the output.

- `--life-list`: Use this option to provide a path to your life list data. The result will merge your life list with the regional results and add an indicator column `on_life_list` to distinguish species that you have already seen vs. species that could be new additions to your life list. Life list data should be an unmodified .csv downloaded from your eBird account (go to https://ebird.org/lifelist). 

