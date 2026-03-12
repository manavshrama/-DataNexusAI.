import pytest
import sys
import os

# Add the project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.code_helpers import extract_python_code

def test_extract_python_code_valid():
    text = "Here is some code:\n```python\nprint('hello')\n```\nHope it helps!"
    expected = "print('hello')"
    assert extract_python_code(text) == expected

def test_extract_python_code_no_code():
    text = "No code here."
    assert extract_python_code(text) is None

def test_extract_python_code_multiline():
    text = "```python\ndef foo():\n    return 42\n```"
    expected = "def foo():\n    return 42"
    assert extract_python_code(text) == expected
