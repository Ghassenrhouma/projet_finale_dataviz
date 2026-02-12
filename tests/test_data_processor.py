"""
Tests for data processor module.
Tests data loading and information extraction.
"""

import pytest
import pandas as pd
from io import StringIO
from src.data_processor import load_data, get_data_info


@pytest.fixture
def sample_csv():
    """Create a sample CSV file for testing."""
    csv_data = """name,age,city,salary
John,30,New York,75000
Jane,25,Los Angeles,65000
Bob,35,Chicago,80000
Alice,28,Houston,70000
"""
    return StringIO(csv_data)


def test_load_data(sample_csv):
    """Test that CSV data is loaded correctly."""
    df = load_data(sample_csv)
    
    assert isinstance(df, pd.DataFrame)
    assert df.shape == (4, 4)
    assert list(df.columns) == ['name', 'age', 'city', 'salary']


def test_get_data_info(sample_csv):
    """Test that data info is extracted correctly."""
    df = load_data(sample_csv)
    info = get_data_info(df)
    
    assert 'columns' in info
    assert 'dtypes' in info
    assert 'shape' in info
    assert 'summary' in info
    
    assert info['columns'] == ['name', 'age', 'city', 'salary']
    assert info['shape'] == (4, 4)
    assert len(info['dtypes']) == 4
    assert isinstance(info['summary'], dict)


def test_load_data_invalid_file():
    """Test error handling for invalid CSV files."""
    invalid_csv = StringIO("invalid,csv,data\n1,2")
    
    # Should still load but may have issues
    df = load_data(invalid_csv)
    assert isinstance(df, pd.DataFrame)


def test_data_types_detection(sample_csv):
    """Test that data types are correctly identified."""
    df = load_data(sample_csv)
    info = get_data_info(df)
    
    # Check that numeric columns are detected
    assert 'int' in info['dtypes']['age']
    assert 'int' in info['dtypes']['salary']
    
    # Check that object columns are detected
    assert 'object' in info['dtypes']['name']
    assert 'object' in info['dtypes']['city']


def test_empty_dataframe():
    """Test handling of empty dataframes."""
    empty_csv = StringIO("col1,col2\n")
    df = load_data(empty_csv)
    info = get_data_info(df)
    
    assert info['shape'][0] == 0  # No rows
    assert len(info['columns']) == 2  # But columns exist
