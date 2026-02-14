"""
Tests for LLM handler module.
Tests the multi-step scaffolding approach for visualization generation.
"""

import pytest
from src.llm_handler import (
    step1_identify_relevant_columns,
    step2_select_chart_types,
    step3_generate_plotting_code,
    generate_visualization_proposals
)


@pytest.fixture
def sample_data_info():
    """Sample dataset information for testing."""
    return {
        'columns': ['age', 'income', 'city', 'purchase_amount'],
        'dtypes': {
            'age': 'int64',
            'income': 'float64',
            'city': 'object',
            'purchase_amount': 'float64'
        },
        'shape': (100, 4),
        'summary': {
            'age': {'mean': 35.5, 'std': 10.2},
            'income': {'mean': 50000, 'std': 15000}
        }
    }


def test_step1_identify_relevant_columns(sample_data_info):
    """Test that step 1 identifies relevant columns."""
    question = "What is the relationship between age and income?"
    
    try:
        result = step1_identify_relevant_columns(question, sample_data_info)
        
        assert 'relevant_columns' in result
        assert 'analysis_reasoning' in result
        assert isinstance(result['relevant_columns'], list)
        assert len(result['relevant_columns']) > 0
    except ValueError as e:
        # If API key is not set, this is expected
        if "GEMINI_API_KEY" in str(e):
            pytest.skip("GEMINI_API_KEY not set")
        else:
            raise


def test_step2_select_chart_types(sample_data_info):
    """Test that step 2 selects appropriate chart types."""
    question = "Show distribution of purchases by city"
    relevant_columns = ['city', 'purchase_amount']
    
    try:
        proposals = step2_select_chart_types(question, sample_data_info, relevant_columns)
        
        assert len(proposals) == 3
        for proposal in proposals:
            assert 'viz_type' in proposal
            assert 'justification' in proposal
            assert 'columns_to_use' in proposal
    except ValueError as e:
        if "GEMINI_API_KEY" in str(e):
            pytest.skip("GEMINI_API_KEY not set")
        else:
            raise


def test_step3_generate_plotting_code(sample_data_info):
    """Test that step 3 generates valid Python code."""
    proposal = {
        'viz_type': 'scatter',
        'columns_to_use': ['age', 'income'],
        'justification': 'Test scatter plot'
    }
    
    try:
        code = step3_generate_plotting_code(proposal, sample_data_info)
        
        assert isinstance(code, str)
        assert len(code) > 0
        # Check that code doesn't have markdown fences
        assert not code.startswith('```')
    except ValueError as e:
        if "GEMINI_API_KEY" in str(e):
            pytest.skip("GEMINI_API_KEY not set")
        else:
            raise


def test_generate_visualization_proposals(sample_data_info):
    """Test the complete multi-step pipeline."""
    question = "What factors influence purchase amounts?"
    
    try:
        proposals = generate_visualization_proposals(question, sample_data_info, 3)
        
        assert len(proposals) == 3
        for proposal in proposals:
            assert 'viz_type' in proposal
            assert 'justification' in proposal
            assert 'step1_analysis' in proposal
    except ValueError as e:
        if "GEMINI_API_KEY" in str(e):
            pytest.skip("GEMINI_API_KEY not set")
        else:
            raise


def test_fallback_on_error(sample_data_info):
    """Test that the system provides fallback proposals on error."""
    # This should work even without API key
    question = "Test question"
    
    # The function should return fallback proposals if API fails
    proposals = generate_visualization_proposals(question, sample_data_info, 3)
    
    assert len(proposals) == 3
    assert all('viz_type' in p for p in proposals)
