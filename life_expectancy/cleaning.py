"""Module for cleaning life expectancy data."""

from typing import Protocol
import pandas as pd
from .my_constants import Country, country_name_from_code

def _split_first_column(df: pd.DataFrame) -> pd.DataFrame:
    """ Split four variables in the first column into their own columns.

    Args:
        df (pd.DataFrame): The data.
    
    Returns:
        df (pd.DataFrame): The modified data.
    """
    df[['unit', 'sex', 'age', 'region']] = df[df.columns[0]].str.split(
                                           ',', expand=True)
    df = df.drop(columns = df.columns[0])
    return df

def _remove_spaces_from_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """ Remove extra space from column names.
    
    Args:
        df (pd.DataFrame): The data.

    Returns:
        df (pd.DataFrame): The modified data.
    """   
    df = df.rename(str.strip, axis = 'columns')
    return df
    
def _melt_df(df: pd.DataFrame) -> pd.DataFrame:
    """ Melt data from wide to long format.
     
    Args:
        df (pd.DataFrame): The data.

    Returns:
        (pd.DataFrame): The melted data.
    """
    years = df.columns[:-4]
    return pd.melt(
        df, 
        id_vars = ['unit', 'sex', 'age', 'region'], 
        value_vars = years, var_name = 'year', 
        value_name = 'value')

def _extract_flag(df: pd.DataFrame) -> pd.DataFrame:
    """Extract flag (b, e, p or their combination) 
       from the value column.
    
    Args:
        df (pd.DataFrame): The data.

    Returns:
        df (pd.DataFrame): The modified data.
    """
    df[['value','flag']] = df['value'].str.split(' ', expand=True)
    return df

def _correct_data_types(df: pd.DataFrame) -> pd.DataFrame:
    """Set correct data types.
    
    Args:
        df (pd.DataFrame): The data.

    Returns:
        df (pd.DataFrame): The modified data.
    """
    for col in [col for col in df.columns if col not in ['year','value']]:
        df[col] = df[col].astype('string')
    df['year'] = df['year'].astype('int')
    df['value'] = pd.to_numeric(
        df['value'], errors = 'coerce')
    return df

def _filter_region_data(df: pd.DataFrame, region: Country) -> pd.DataFrame:
    """Filter data for the given region.

    Args:
        df (pd.DataFrame): The data.
        region (Country): The region to select.

    Returns:
        df_region (pd.DataFrame): The data for the specified region.

    Raises:
        ValueError: If the region is not in the data.
    """
    if region.name not in df.region.unique():
        raise ValueError(f"""
                Region {region.name} ({country_name_from_code(region)}) not in the dataset, 
                choose another region from {df.region.unique().tolist()}
                         """)
    df_region = df[df.region == region.name]
    df_region = df_region[['unit', 'sex', 'age', 'region','year','value']]
    print(f'{df_region.shape[0]} lines were exported for'\
          f' region {region.value} ({country_name_from_code(region)})')
    return df_region

def _rename_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Rename country and life_expectancy columns

    Args:
        df (pd.DataFrame): The data.

    Returns:
        pd.DataFrame: The renamed dataframe. 
    """
    old_names = ['unit','sex','age','country','year','life_expectancy','flag','flag_detail']
    new_names = ['unit','sex','age','region','year','value','flag','flag_detail']
    return df.rename(columns = dict(zip(old_names, new_names)))

def _filter_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Select columns for output

    Args:
        df (pd.DataFrame): The data.

    Returns:
        pd.DataFrame: The renamed dataframe. 
    """
    return df[['unit','sex','age','region','year','value']]

class CleanData(Protocol):
    """ Strategy for cleaning data from different filetypes """
    def clean_data(self, df: pd.DataFrame, region: Country = Country.PT) -> pd.DataFrame:
        """ Strategy for cleaning data from different filetypes
            Clean and export data for the chosen region.
        Args:
            df (pd.DataFrame): The data.
            region (Country): The region to select.
        Returns:
            (pd.DataFrame): The data for the specified region.
        """

class CleanTsv:
    """ Strategy for cleaning tsv files """
    def clean_data(self, df: pd.DataFrame, region: Country = Country.PT) -> pd.DataFrame:
        """ Clean and export data for the chosen region.
        Args:
            df (pd.DataFrame): The data.
            region (Country): The region to select.
        Returns:
            (pd.DataFrame): The data for the specified region. """
        df = _split_first_column(df)
        df = _remove_spaces_from_column_names(df)
        df = _melt_df(df)
        df = _extract_flag(df)
        df = _correct_data_types(df)
        df = _filter_columns(df)
        df = df.dropna()
        return _filter_region_data(df, region)

class CleanJson:
    """ Strategy for cleaning json files """
    def clean_data(self, df: pd.DataFrame, region: Country = Country.PT) -> pd.DataFrame:
        """ Clean and export data for the chosen region.
        Args:
            df (pd.DataFrame): The data.
            region (Country): The region to select.
        Returns:
            (pd.DataFrame): The data for the specified region. """
        df = _rename_columns(df)
        df = _correct_data_types(df)
        df = _filter_columns(df)
        df = df.dropna()
        return _filter_region_data(df, region)

def clean_data(clean_strategy: CleanData, df: pd.DataFrame, 
               region: Country = Country.PT) -> pd.DataFrame:
    """ Clean and export data based on a strategy for different filetypes """
    return clean_strategy.clean_data(df, region)
