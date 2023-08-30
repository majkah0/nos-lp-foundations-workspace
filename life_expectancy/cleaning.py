import pandas as pd
import argparse
from pathlib import Path

BASE_DIR = Path().cwd() / 'life_expectancy' / 'data'

def load_data(path: Optional[Path] = None) -> pd.DataFrame:
    """ Reads life expectancy data into a DataFrame."""
    if path is None:
        path = BASE_DIR / 'eu_life_expectancy_raw.tsv'
    return pd.read_csv(path, sep='\t')

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

def export_region_data(df: pd.DataFrame, region: str) -> None:
    df_region = df[df.region == region]
    df_region = df_region[['unit', 'sex', 'age', 'region','year','value']]
    print(f'{df_region.shape[0]} lines were exported for region {region}')
    return df_region

def clean_data(df: pd.DataFrame, region: str = 'PT') -> None:
    """ 
    imports and cleans life expectancy data
    exports data for the chosen region         
    """
    df = split_first_column(df)
    df = remove_spaces_from_column_names(df)
    df = melt_df(df)
    df = extract_flag(df)
    df = correct_data_types(df)
    df = df.dropna()
    df_region = export_region_data(df, region)
    return df_region

def save_data(df: pd.DataFrame, region: str) -> None:
    file_name = region.lower() + '_life_expectancy.csv'
    path = Path().cwd() / 'life_expectancy' / 'data' / file_name
    df.to_csv(path, index = False)    

def main(region: str)-> None:
    eu_life_expectancy_data = load_data()
    region_life_expectancy_data = clean_data(eu_life_expectancy_data, region = region)
    save_data(region_life_expectancy_data, region)

if __name__ == "__main__":  # pragma: no cover
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--region",
                         default = 'PT', 
                         help = 'Input region argument.',
                         type = str)
    args = parser.parse_args()
    main(region = args.region)