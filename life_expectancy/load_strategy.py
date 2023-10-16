"""Module for strategies for loading of different data files."""

from pathlib import Path
from typing import Optional, Protocol
import pandas as pd

BASE_DIR = Path().cwd() / 'life_expectancy' / 'data'

class LoadData(Protocol):
    """ Protocol for strategies to Eurostat data of different file types """
    def read_data(self, path: Optional[Path] = None) -> pd.DataFrame:
       ...

class LoadJson(LoadData):
    """ Strategy to load zipped json Eurostat data """
    def read_data(self, path: Optional[Path] = None) -> pd.DataFrame:
       if path is None:
           path = BASE_DIR / 'eurostat_life_expect.zip'
       return pd.read_json(path)
    
class LoadTsv(LoadData):
    """ Strategy to load tsv Eurostat data"""
    def read_data(self, path: Optional[Path] = None) -> pd.DataFrame:
       if path is None:
           path = BASE_DIR / 'eu_life_expectancy_raw.tsv'
       return pd.read_csv(path, sep = '\t')
