# Life Expectancy Data Cleaning
[![CI/CD Workflow](https://github.com/majkah0/nos-lp-foundations-workspace/actions/workflows/python-package.yml/badge.svg?branch=ci)](https://github.com/majkah0/nos-lp-foundations-workspace/actions/workflows/python-package.yml)

This project is designed to load and clean Eurostat life expectancy data from a provided CSV file. The purpose of the code is to clean the data, convert it into a more usable format, and export data for any given country/region as a CSV file. 
The structure of this project is as it follows:
```bash
└── life_expectancy
    └── data
    ├── tests
    ├── cleaning.py
    ├── README.md
└── pyproject.toml
```
All the code is in the `cleaning.py` file.

## Table of Contents

- [Introduction](#introduction)
- [Usage](#usage)
- [Functionality](#functionality)
- [Requirements](#requirements)
- [Installation](#installation)

## Introduction

Life expectancy data comes in formats typical for the issueing institution. It has to be preprocessed and cleaned before performing any analysis. This code provides a solution for loading, cleaning, and saving life expectancy data for a specific country/region. It reshapes the data for an easier analysis, corrects text formatting errors, handles missing values, and converts data types. It then exports the data for the selected country/region as a csv file.

## Usage

To use the script, follow these steps:

1. Make sure you have the necessary requirements installed (see [Requirements](#requirements)).
2. Download the raw life expectancy data file (`eu_life_expectancy_raw.tsv`) and place it in the `life_expectancy/data` directory.
3. Open a terminal or command prompt.
4. Navigate to the project directory.
5. Run the script using the following command, replacing `REGION_NAME` with the desired region's name in the string format (e.g., "PT" for Portugal):

```bash
python cleaning.py --region REGION_NAME
```

The cleaned and processed data will be saved as `<REGION_NAME>_life_expectancy.csv` in the `data` directory, with `REGION_NAME` equal to the input parameter.

## Functionality

The script performs the following tasks:

1. **Loading Data**: The script loads the raw life expectancy data from a provided CSV file (`eu_life_expectancy_raw.tsv`).

2. **Data Cleaning**: It preprocesses the data by splitting a column containing multiple variables and cleaning column names.

3. **Data Reshaping**: The script melts the DataFrame to turn all year columns into a single year column for an easier analysis.

4. **Flag Extraction**: It separates the life expectancy values from the accompanying flags indicating the data provenance. The flags are currently not kept in the exported data, but might be useful in downstream analysis.

5. **NaN Handling and Type Conversion**: The script identifies NaN-like values in specified columns. It then converts all values into the appropriate data types. It also removes any rows with missing data.

6. **Region Selection**: It filters the data to keep only the rows corresponding to the specified region.

7. **Saving Data**: The filtered data is saved as `<REGION_NAME>_life_expectancy.csv` in the `data` directory.

## Requirements

- Python <=3.8
- pandas
- numpy

## Installation

1. Clone or download this repository.

```bash
git clone git@github.com/majkah0/nos-lp-foundations-workspace.git
```
