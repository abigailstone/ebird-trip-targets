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
