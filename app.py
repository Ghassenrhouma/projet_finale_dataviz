"""
Hugging Face Spaces entry point.
"""
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import and run the main app
from src.app import *
