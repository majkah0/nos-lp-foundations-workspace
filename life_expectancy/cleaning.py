# line length 79                                                              | 

import pandas as pd

@click.command()
@click.option('--region', default = 'PT', required=True)
def clean_data(**kwargs) -> None:
    """ cleans life expectancy data"""
    file_path = '/home/maria/projects/nos-lp-foundations-workspace/assignments/life_expectancy/data/eu_life_expectancy_raw.tsv'
    eu_life_expectancy_df = pd.read_csv(file_path, sep = '\t')
    
    eu_life_expectancy_df[['unit', 'sex', 'age', 'region']] = eu_life_expectancy_df[
        eu_life_expectancy_df.columns[0]].str.split(',', expand=True)
    eu_life_expectancy_df = eu_life_expectancy_df.drop(
        columns = eu_life_expectancy_df.columns[0])
    
    eu_life_expectancy_df = eu_life_expectancy_df.rename(str.strip, axis = 'columns')
    
    years = eu_life_expectancy_df.columns[:-4]
    eu_life_expectancy_df_long = pd.melt(
        eu_life_expectancy_df, id_vars = ['unit', 'sex', 'age', 'region'], 
        value_vars = years, var_name = 'year', value_name = 'value')
    
    for col in eu_life_expectancy_df_long.columns[:4]:
        eu_life_expectancy_df_long[col] = eu_life_expectancy_df_long[col].astype('string')
    eu_life_expectancy_df_long['year'] = eu_life_expectancy_df_long['year'].astype('int')
    eu_life_expectancy_df_long['value'] = pd.to_numeric(
        eu_life_expectancy_df_long['value'], errors = 'coerce')
    
    pt_life_expectancy = eu_life_expectancy_df_long[
        eu_life_expectancy_df_long.region == region].copy()
    file_path = '/home/maria/projects/nos-lp-foundations-workspace/assignments/life_expectancy/data/pt_life_expectancy.csv'
    pt_life_expectancy.to_csv(file_path, index = False)

if __name__ == "__main__":  # pragma: no cover
    clean_data(region = 'PT')    
    

