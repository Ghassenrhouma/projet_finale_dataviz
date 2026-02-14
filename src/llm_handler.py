import os
import google.generativeai as genai
from typing import Dict, Any, List
import json
import re


def _get_model():
    """Initialize and return Gemini model."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not set. Please check your .env file.")
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-2.5-flash')


def step1_identify_relevant_columns(question: str, data_info: Dict[str, Any]) -> Dict[str, Any]:
    """
    STEP 1: Analyze the CSV schema and question to identify relevant columns.
    This is the first step in the multi-step scaffolding approach.
    
    Args:
        question (str): User's question about the data.
        data_info (dict): Information about the dataset.
    
    Returns:
        dict: Contains 'relevant_columns' and 'analysis_reasoning'.
    """
    model = _get_model()
    
    prompt = f"""You are a data analysis expert. Analyze the dataset schema and user question to identify which columns are relevant for visualization.

Dataset Schema:
- Columns: {', '.join(data_info['columns'])}
- Data Types: {json.dumps(data_info['dtypes'], indent=2)}
- Shape: {data_info['shape']} (rows, columns)
- Sample Statistics: {json.dumps({k: v for k, v in list(data_info['summary'].items())[:3]}, indent=2)}

User Question: "{question}"

Task: Identify which columns from the dataset are most relevant to answer this question.

Respond in this EXACT JSON format:
{{
    "relevant_columns": ["column1", "column2"],
    "analysis_reasoning": "Brief explanation of why these columns are relevant"
}}"""

    try:
        response = model.generate_content(prompt)
        raw_response = response.text.strip()
        
        # Extract JSON from response
        json_match = re.search(r'\{.*\}', raw_response, re.DOTALL)
        if json_match:
            result = json.loads(json_match.group())
            return result
        else:
            # Fallback
            return {
                "relevant_columns": data_info['columns'][:2],
                "analysis_reasoning": "Could not parse LLM response, using first two columns."
            }
    except Exception as e:
        return {
            "relevant_columns": data_info['columns'][:2],
            "analysis_reasoning": f"Error in step 1: {str(e)}"
        }


def step2_select_chart_types(question: str, data_info: Dict[str, Any], relevant_columns: List[str]) -> List[Dict[str, str]]:
    """
    STEP 2: Select 3 appropriate chart types with justifications based on best practices.
    This considers: chart type appropriateness, data-ink ratio, avoiding chartjunk, etc.
    
    Args:
        question (str): User's question.
        data_info (dict): Dataset information.
        relevant_columns (list): Columns identified in step 1.
    
    Returns:
        list: 3 proposals with viz_type and justification.
    """
    model = _get_model()
    
    # Get dtypes for relevant columns
    relevant_dtypes = {col: data_info['dtypes'].get(col, 'unknown') for col in relevant_columns}
    
    prompt = f"""You are a data visualization expert following best practices (Tufte, Cleveland, Few).

User Question: "{question}"

Relevant Columns Identified: {', '.join(relevant_columns)}
Column Data Types: {json.dumps(relevant_dtypes, indent=2)}
Dataset Shape: {data_info['shape']}

Task: Recommend 3 DIFFERENT visualization types that would best answer the question.

Considerations:
1. Choose the RIGHT chart type for the data (categorical vs continuous, relationships vs distributions vs comparisons)
2. Maximize data-ink ratio (avoid unnecessary decoration)
3. Avoid chartjunk (no 3D effects, minimal grid lines)
4. Consider perceptual effectiveness
5. Each recommendation should use a DIFFERENT chart type

Available chart types: bar, line, scatter, histogram, box, violin, heatmap, pie

Respond in this EXACT JSON format:
{{
    "proposals": [
        {{
            "viz_type": "chart_type_1",
            "justification": "Why this chart type is appropriate, referencing best practices",
            "columns_to_use": ["col1", "col2"]
        }},
        {{
            "viz_type": "chart_type_2",
            "justification": "Why this chart type is appropriate, referencing best practices",
            "columns_to_use": ["col1"]
        }},
        {{
            "viz_type": "chart_type_3",
            "justification": "Why this chart type is appropriate, referencing best practices",
            "columns_to_use": ["col1", "col2"]
        }}
    ]
}}"""

    try:
        response = model.generate_content(prompt)
        raw_response = response.text.strip()
        
        # Extract JSON
        json_match = re.search(r'\{.*\}', raw_response, re.DOTALL)
        if json_match:
            result = json.loads(json_match.group())
            return result['proposals']
        else:
            raise ValueError("Could not parse JSON response")
    except Exception as e:
        # Fallback proposals
        return [
            {
                "viz_type": "bar",
                "justification": f"Fallback: Bar chart for comparison. Error: {str(e)}",
                "columns_to_use": relevant_columns[:2]
            },
            {
                "viz_type": "scatter",
                "justification": "Fallback: Scatter plot for relationships.",
                "columns_to_use": relevant_columns[:2]
            },
            {
                "viz_type": "histogram",
                "justification": "Fallback: Histogram for distribution.",
                "columns_to_use": relevant_columns[:1]
            }
        ]


def step3_generate_plotting_code(proposal: Dict[str, Any], data_info: Dict[str, Any]) -> str:
    """
    STEP 3: Generate actual Python plotting code for the selected visualization.
    
    Args:
        proposal (dict): Contains viz_type, columns_to_use, justification.
        data_info (dict): Dataset information.
    
    Returns:
        str: Python code to generate the plot using Plotly.
    """
    model = _get_model()
    
    prompt = f"""You are a Python data visualization expert following Edward Tufte and Stephen Few's best practices.

Visualization Type: {proposal['viz_type']}
Columns to Use: {proposal.get('columns_to_use', [])}
Dataset Info:
- All Columns: {data_info['columns']}
- Data Types: {json.dumps(data_info['dtypes'], indent=2)}

Task: Generate clean, READABLE Plotly code for a general audience.

CRITICAL Requirements:
1. Use plotly.express (already imported as px)
2. The DataFrame is already loaded as 'df'
3. Create CLEAR, DESCRIPTIVE titles (not just column names)
4. Use MEANINGFUL axis labels (capitalize properly, add units if applicable)
5. Limit data points for readability (sample if > 1000 rows, show top 15 categories max)
6. Use PROFESSIONAL COLOR SCHEMES - ALWAYS specify colors:
   - For single category: color_discrete_sequence=['#3498db'] (blue)
   - For continuous: color_continuous_scale='Viridis' or 'Blues'
   - For categorical with color param: use a color column if available
7. Ensure text doesn't overlap (rotate labels if needed)
8. Add proper formatting for numbers (round to 2 decimals)
9. Assign the figure to variable 'fig'
10. Do NOT use 'return' statement
11. Do NOT include imports (px and df available)
12. Do NOT include markdown or code fences

Example with colors:
fig = px.bar(df, x='category', y='value', 
            title='Clear Title',
            color_discrete_sequence=['#3498db'])
fig.update_layout(
    title=dict(text='Clear Descriptive Title', font=dict(size=18)),
    font=dict(family='Arial, sans-serif', size=12),
    xaxis_title='Clear X Label',
    yaxis_title='Clear Y Label',
    template='plotly_white',
    showlegend=True,
    height=500
)

Generate ONLY executable Python code:"""

    try:
        response = model.generate_content(prompt)
        code = response.text.strip()
        
        # Clean up code fences if present
        code = re.sub(r'^```python\s*', '', code)
        code = re.sub(r'^```\s*', '', code)
        code = re.sub(r'\s*```$', '', code)
        
        # Remove any return statements that might cause issues
        code = re.sub(r'\breturn\s+fig\b', 'pass  # fig already assigned', code)
        
        return code
    except Exception as e:
        # Return fallback code
        cols = proposal.get('columns_to_use', data_info['columns'][:2])
        return f"""# Fallback code due to error: {str(e)}
fig = px.{proposal['viz_type']}(df, x='{cols[0] if cols else data_info['columns'][0]}', 
                                title='{proposal['viz_type'].capitalize()} Chart')
"""


def generate_visualization_proposals(question: str, data_info: Dict[str, Any], num_proposals: int = 3) -> List[Dict[str, Any]]:
    """
    Multi-step scaffolding approach to generate visualization proposals.
    
    This implements a chain-of-thought approach:
    1. First call: Analyze schema and identify relevant columns
    2. Second call: Select 3 appropriate chart types with justifications
    3. Third call: Generate actual plotting code (done later, per proposal)
    
    Args:
        question (str): User's question about the data.
        data_info (dict): Information about the dataset.
        num_proposals (int): Number of proposals (default 3).
    
    Returns:
        list: Proposals with viz_type, justification, columns_to_use, and plotting_code.
    """
    try:
        # STEP 1: Identify relevant columns
        step1_result = step1_identify_relevant_columns(question, data_info)
        relevant_columns = step1_result['relevant_columns']
        
        # STEP 2: Select chart types
        proposals = step2_select_chart_types(question, data_info, relevant_columns)
        
        # Ensure we have exactly num_proposals
        while len(proposals) < num_proposals:
            proposals.append({
                "viz_type": "bar",
                "justification": "Additional fallback proposal",
                "columns_to_use": relevant_columns[:2]
            })
        
        # Add step 1 reasoning to each proposal for transparency
        for proposal in proposals[:num_proposals]:
            proposal['step1_analysis'] = step1_result['analysis_reasoning']
        
        return proposals[:num_proposals]
        
    except Exception as e:
        # Complete fallback
        return [
            {
                "viz_type": "bar",
                "justification": f"Error in LLM pipeline: {str(e)}. Using fallback.",
                "columns_to_use": data_info['columns'][:2],
                "step1_analysis": "Error occurred"
            }
        ] * num_proposals