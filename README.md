# eBird Trip Targets

Python tool for generating a spreadsheet of target species across multiple regions. 

## Basic usage

Download eBird bar charts for each target region and put them together in a directory. 

Run the script, specifying the path to the directory containing the bar chart files, and the month and year of your trip. 

For example, if you will be visiting your target regions in the second week of May: 

```
$ python trip_targets.py /path/to/barcharts/ --month 5 --week 2
```

**NOTE**: Bar chart files should be *unmodified*, since the processing scripts expect the default formatting and file-naming from eBird. 
