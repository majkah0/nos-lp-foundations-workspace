"""Pytest configuration file"""
import pandas as pd
import pytest
from . import FIXTURES_DIR, OUTPUT_DIR


@pytest.fixture(autouse=True)
def run_before_and_after_tests() -> None:
    """Fixture to execute commands before and after a test is run"""
    # Setup: fill with any logic you want

    yield # this is where the testing happens

    # Teardown : fill with any logic you want
    file_path = OUTPUT_DIR / "pt_life_expectancy.csv"
    file_path.unlink(missing_ok=True)

@pytest.fixture(scope="session")
def pt_life_expectancy_tsv_input() -> pd.DataFrame:
    """Fixture to load the input file sample"""
    return pd.read_csv(FIXTURES_DIR / "eu_life_expectancy_tsv_input_sample.tsv", sep='\t')

@pytest.fixture(scope="session")
def pt_life_expectancy_json_input() -> pd.DataFrame:
    """Fixture to load the input file sample"""
    return pd.read_csv(FIXTURES_DIR / "eu_life_expectancy_json_input_sample.csv")

@pytest.fixture(scope="session")
def pt_life_expectancy_cleaned_expected_tsv_input() -> pd.DataFrame:
    """Fixture to load the expected output of the cleaning script with the tsv input"""
    df = pd.read_csv(FIXTURES_DIR / "pt_life_expectancy_cleaned_expected_tsv_input.csv", index_col=[0])
    return df 

@pytest.fixture(scope="session")
def pt_life_expectancy_cleaned_expected_json_input() -> pd.DataFrame:
    """Fixture to load the expected output of the cleaning script with the tsv input"""
    df = pd.read_csv(FIXTURES_DIR / "pt_life_expectancy_cleaned_expected_json_input.csv", index_col=[0])
    return df 
