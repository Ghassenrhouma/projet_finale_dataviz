import pandas as pd

def validate_dataframe(df: pd.DataFrame) -> None:
    """
    Validate the DataFrame for basic requirements.

    Args:
        df (pd.DataFrame): DataFrame to validate.

    Raises:
        ValueError: If validation fails.
    """
    if df.empty:
        raise ValueError("The uploaded dataset is empty.")
    if len(df.columns) < 2:
        raise ValueError("The dataset must have at least two columns for visualization.")
    # Check for numeric columns for certain plots
    numeric_cols = df.select_dtypes(include=[float, int]).columns
    if len(numeric_cols) == 0:
        raise ValueError("The dataset must contain at least one numeric column.")

def format_llm_response(response: str) -> dict:
    """
    Parse the LLM response into a structured format.
    Assumes response is in a specific format, e.g., JSON-like.

    Args:
        response (str): Raw response from LLM.

    Returns:
        dict: Parsed response with 'viz_type' and 'justification'.
    """
    # Simple parsing; in practice, use JSON or structured output
    try:
        # Assume response is "viz_type: bar\njustification: ..."
        lines = response.strip().split('\n')
        viz_type = lines[0].split(': ')[1] if ':' in lines[0] else 'bar'
        justification = lines[1].split(': ')[1] if len(lines) > 1 and ':' in lines[1] else response
        return {'viz_type': viz_type, 'justification': justification}
    except:
        return {'viz_type': 'bar', 'justification': 'Default visualization due to parsing error.'}