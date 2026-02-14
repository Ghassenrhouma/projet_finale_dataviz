"""
Hugging Face Spaces entry point.
"""
import sys
import os

# Add src to path so imports in src/app.py resolve correctly
src_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src')
if src_path not in sys.path:
    sys.path.insert(0, src_path)

# Use exec so the code re-runs on every Streamlit rerun
# (import would cache the module and skip re-execution)
exec(open(os.path.join(src_path, 'app.py'), encoding='utf-8').read())
