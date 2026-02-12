import pandas as pd

def load_data(file_path) -> pd.DataFrame:
    """
    Load a CSV or Excel file into a pandas DataFrame.

    Args:
        file_path: Path to the CSV or Excel file, or file-like object.

    Returns:
        pd.DataFrame: Loaded DataFrame.
    """
    try:
        # Check if it's a file-like object (from Streamlit uploader)
        if hasattr(file_path, 'name'):
            filename = file_path.name
        else:
            filename = str(file_path)
        
        # Determine file type and load accordingly
        if filename.endswith('.csv'):
            df = pd.read_csv(file_path)
        elif filename.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(file_path, engine='openpyxl')
        else:
            # Try CSV as default
            df = pd.read_csv(file_path)
        
        return df
    except Exception as e:
        raise ValueError(f"Error loading data: {str(e)}")

def get_data_info(df: pd.DataFrame) -> dict:
    """
    Extract basic information from the DataFrame.

    Args:
        df (pd.DataFrame): Input DataFrame.

    Returns:
        dict: Dictionary containing columns, data types, shape, and summary statistics.
    """
    info = {
        'columns': list(df.columns),
        'dtypes': {col: str(dtype) for col, dtype in df.dtypes.items()},
        'shape': df.shape,
        'summary': df.describe(include='all').to_dict()
    }
    return info