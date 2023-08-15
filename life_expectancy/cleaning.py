import pandas as pd
import argparse
from pathlib import Path

def import_data(path: str) -> pd.DataFrame:
    """ reads life expectancy data into a DataFrame"""
    return pd.read_csv(path, sep = '\t')

def split_first_column(df: pd.DataFrame) -> pd.DataFrame:
    """ Splits four variables in the first column into their own columns """
    df[['unit', 'sex', 'age', 'region']] = df[df.columns[0]].str.split(
                                           ',', expand=True)
    df = df.drop(columns = df.columns[0])
    return df

def remove_spaces_from_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """ Removes extra space from column names."""   
    df = df.rename(str.strip, axis = 'columns')
    return df
    
def melt_df(df: pd.DataFrame) -> pd.DataFrame:
    """ Melts DataFrame. """
    years = df.columns[:-4]
    return pd.melt(
        df, 
        id_vars = ['unit', 'sex', 'age', 'region'], 
        value_vars = years, var_name = 'year', 
        value_name = 'value')

def extract_flag(df: pd.DataFrame) -> pd.DataFrame:
    """Extract flag (b, e, p or their combination)
    from the value column."""
    df[['value','flag']] = df['value'].str.split(' ', expand=True)
    return df

def correct_data_types(df: pd.DataFrame) -> pd.DataFrame:
    for col in ['unit', 'sex', 'age', 'region','flag']:
        df[col] = df[col].astype('string')
    df['year'] = df['year'].astype('int')
    df['value'] = pd.to_numeric(
        df['value'], errors = 'coerce')
    return df

def remove_flagged_columns(df: pd.DataFrame) -> pd.DataFrame:
    return df[df.flag=='']

def export_region_data(df: pd.DataFrame, region: str) -> None:
    df_region = df[df == region]
    df_region = remove_flagged_columns(df_region)
    file_name = region.lower() + '_life_expectancy.csv'
    path = path = Path().cwd() / 'life_expectancy' / 'data' / file_name
    df_region = df_region[['unit', 'sex', 'age', 'year','value']]
    df_region.to_csv(path, index = False)    

def clean_data(region: str = 'PT') -> None:
    """ 
    imports and cleans life expectancy data
    exports data for the chosen region         
    """
    path = Path().cwd() / 'life_expectancy' / 'data' / 'eu_life_expectancy_raw.tsv'
    eu_life_expectancy_df = import_data(path)
    eu_life_expectancy_df = split_first_column(eu_life_expectancy_df)
    eu_life_expectancy_df = remove_spaces_from_column_names(eu_life_expectancy_df)
    eu_life_expectancy_df = melt_df(eu_life_expectancy_df)
    eu_life_expectancy_df = extract_flag(eu_life_expectancy_df)
    eu_life_expectancy_df = correct_data_types(eu_life_expectancy_df)
    export_region_data(eu_life_expectancy_df, region)

if __name__ == "__main__":  # pragma: no cover
    parser = argparse.ArgumentParser()
    parser.add_argument("region", help = 'Input region argument.', type = str)
    args = parser.parse_args()
    clean_data(region = args.region)
    