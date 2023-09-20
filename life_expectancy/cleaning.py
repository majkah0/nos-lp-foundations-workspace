"""Module for cleaning life expectancy data."""

import pandas as pd

def split_first_column(df: pd.DataFrame) -> pd.DataFrame:
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

def remove_spaces_from_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """ Remove extra space from column names.
    
    Args:
        df (pd.DataFrame): The data.

    Returns:
        df (pd.DataFrame): The modified data.
    """   
    df = df.rename(str.strip, axis = 'columns')
    return df
    
def melt_df(df: pd.DataFrame) -> pd.DataFrame:
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

def extract_flag(df: pd.DataFrame) -> pd.DataFrame:
    """Extract flag (b, e, p or their combination) 
       from the value column.
    
    Args:
        df (pd.DataFrame): The data.

    Returns:
        df (pd.DataFrame): The modified data.
    """
    df[['value','flag']] = df['value'].str.split(' ', expand=True)
    return df

def correct_data_types(df: pd.DataFrame) -> pd.DataFrame:
    """Set correct data types.
    
    Args:
        df (pd.DataFrame): The data.

    Returns:
        df (pd.DataFrame): The modified data.
    """
    for col in ['unit', 'sex', 'age', 'region','flag']:
        df[col] = df[col].astype('string')
    df['year'] = df['year'].astype('int')
    df['value'] = pd.to_numeric(
        df['value'], errors = 'coerce')
    return df

def filter_region_data(df: pd.DataFrame, region: str) -> pd.DataFrame:
    """Filter data for the given region.

    Args:
        df (pd.DataFrame): The data.
        region (str): The region to select.

    Returns:
        df_region (pd.DataFrame): The data for the specified region.

    Raises:
        ValueError: If the region is not in the data.
    """
    if region not in df.region.unique():
        raise ValueError(f"""
                         Region {region} not in the dataset, choose another region from
                         {df.region.unique().tolist()}
                         """)
    df_region = df[df.region == region]
    df_region = df_region[['unit', 'sex', 'age', 'region','year','value']]
    print(f'{df_region.shape[0]} lines were exported for region {region}')
    return df_region

def clean_data(df: pd.DataFrame, region: str = 'PT') -> pd.DataFrame:
    """ Clean data and export data for the chosen region.
    Args:
        df (pd.DataFrame): The data.
        region (str): The region to select.

    Returns:
        (pd.DataFrame): The data for the specified region.
    """
    df = split_first_column(df)
    df = remove_spaces_from_column_names(df)
    df = melt_df(df)
    df = extract_flag(df)
    df = correct_data_types(df)
    df = df.dropna()
    return filter_region_data(df, region)
