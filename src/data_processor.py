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
            # Reset file position in case it was already read (Streamlit reruns)
            if hasattr(file_path, 'seek'):
                file_path.seek(0)
        else:
            filename = str(file_path)
        
        # Determine file type and load accordingly
        if filename.lower().endswith('.csv'):
            df = pd.read_csv(file_path)
        elif filename.lower().endswith(('.xlsx', '.xls')):
            df = pd.read_excel(file_path, engine='openpyxl')
        else:
            # Try CSV as default
            try:
                df = pd.read_csv(file_path)
            except:
                raise ValueError(f"Unsupported file format: {filename}")
        
        # Basic validation
        if df is None:
            raise ValueError("Failed to load data")
            
        if df.empty:
            raise ValueError("The uploaded file is empty")
        
        if len(df.columns) == 0:
            raise ValueError("The uploaded file has no columns")
        
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