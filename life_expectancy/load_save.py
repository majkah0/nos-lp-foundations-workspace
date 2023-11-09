"""Module for loading and saving life expectancy data."""

from pathlib import Path
from typing import Optional, Protocol
import pandas as pd
from life_expectancy import BASE_DIR, Country, json_filename, tsv_filename

class LoadData(Protocol):
    """ Strategy for strategies to Eurostat data of different file types """
    def read_data(self, path: Optional[Path] = None) -> pd.DataFrame:
        ...

class LoadJson:
    """ Strategy to load zipped json Eurostat data """
    def read_data(self, path: Optional[Path] = None) -> pd.DataFrame:
        if path is None:
            path = BASE_DIR / json_filename
        return pd.read_json(path, compression = 'zip')
    
class LoadTsv:
    """ Strategy to load tsv Eurostat data"""
    def read_data(self, path: Optional[Path] = None) -> pd.DataFrame:
        if path is None:
            path = BASE_DIR / tsv_filename
        return pd.read_csv(path, sep = '\t')

def load_data(load_strategy: LoadData, path: Optional[Path] = None) -> pd.DataFrame:
    """ Read life expectancy data into a DataFrame.
    
    Args:
        load_strategy: How to load the data depending on the file type
        path (Optional[Path]): The path to the directory with the csv file.

    Returns:
        (pd.DataFrame): The data.
    """
    return load_strategy.read_data(path)

def save_data(df: pd.DataFrame, region: Country, path: Optional[Path] = None) -> None:
    """ Save data for the chosen region.
    Args:
        df (pd.DataFrame): The data.
        region (Country): The region to select.
        path (Optional[Path]): The path to the export directory.
    """
    file_name = f'{region.name.lower()}_life_expectancy.csv'
    if path is None:
        path = BASE_DIR / file_name
    else:
        path = path / file_name
    df.to_csv(path, index = False)    
