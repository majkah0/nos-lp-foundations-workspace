"""Module for loading and saving life expectancy data."""

from pathlib import Path
from typing import Optional
import pandas as pd
from load_strategy import LoadData, LoadJson, LoadTsv

BASE_DIR = Path().cwd() / 'life_expectancy' / 'data'

def load_data(load_strategy: LoadData, path: Optional[Path] = None) -> pd.DataFrame:
    """ Read life expectancy data into a DataFrame.
    
    Args:
        path (Optional[Path]): The path to the directory with the csv file.
        load_strategy: How to load the data depending on the file type

    Returns:
        (pd.DataFrame): The data.
    """
    return load_strategy.read_data()

def save_data(df: pd.DataFrame, region: str, path: Optional[Path] = None) -> None:
    """ Save data for the chosen region.
    Args:
        df (pd.DataFrame): The data.
        region (str): The region to select.
        path (Optional[Path]): The path to the export directory.
    """
    file_name = f'{region.lower()}_life_expectancy.csv'
    if path is None:
        path = BASE_DIR / file_name
    else:
        path = path / file_name
    df.to_csv(path, index = False)    

