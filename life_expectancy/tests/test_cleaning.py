"""Tests for all modules"""

import pandas as pd
from ..load_save import load_data, save_data
from ..cleaning import clean_data
from ..main import main
from unittest.mock import MagicMock, patch
from . import OUTPUT_DIR, FIXTURES_DIR

def _correct_data_types(df: pd.DataFrame) -> pd.DataFrame:
    """Set correct data types.
    
    Args:
        df (pd.DataFrame): The data.

    Returns:
        df (pd.DataFrame): The modified data.
    """
    for col in ['unit', 'sex', 'age', 'region']:
        df[col] = df[col].astype('string')
    df['year'] = df['year'].astype('int')
    df['value'] = pd.to_numeric(
        df['value'])
    return df

def test_clean_data(pt_life_expectancy_input, pt_life_expectancy_cleaned_expected) -> pd.DataFrame:
    pt_life_expectancy_cleaned_actual = clean_data(pt_life_expectancy_input, 'PT')
    pd.testing.assert_frame_equal(pt_life_expectancy_cleaned_actual,
                                  _correct_data_types(pt_life_expectancy_cleaned_expected))

def test_save_data(pt_life_expectancy_cleaned_expected):
    to_csv_mock = MagicMock()
    with patch("./load_save.save_data.pd.DataFrame.to_csv", to_csv_mock):
         to_csv_mock(side_effect=print('Saved data'))
         save_data(pt_life_expectancy_cleaned_expected, 'PT')
         to_csv_mock.assert_called_once()

def test_main():
    """Run the `clean_data` function and compare the output to the expected output"""
    region = 'PT'
    df_actual = main(region = region)
    df_expected = pd.read_csv(
        FIXTURES_DIR / 'pt_life_expectancy_total_expected.csv',index_col=[0])
    df_expected = _correct_data_types(df_expected)
    pd.testing.assert_frame_equal(
        df_actual, df_expected)
