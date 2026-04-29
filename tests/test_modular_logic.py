import sys
import os
import pandas as pd
import pytest

# Add the project root to sys.path for imports
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from utils.constants import PAGE_TITLE
from services.execution_service import extract_python_code, execute_code

def test_code_extraction():
    print("Testing code extraction...")
    content = "Here is the code:\n```python\nprint('hello')\n```\nDone."
    assert extract_python_code(content) == "print('hello')"
    
    no_code = "Just text."
    assert extract_python_code(no_code) is None
    print("Code extraction OK.")

def test_code_execution():
    df = pd.DataFrame({"A": [1, 2], "B": [3, 4]})
    code = "df['C'] = df['A'] + df['B']"
    stdout, new_df, fig = execute_code(code, df)
    
    assert "C" in new_df.columns
    assert new_df["C"].tolist() == [4, 6]
    # In headless/test mode, fig might be None or a generic fig
    # We just check that it doesn't crash

def test_constants_loading():
    assert PAGE_TITLE == "Data Nexus AI"
