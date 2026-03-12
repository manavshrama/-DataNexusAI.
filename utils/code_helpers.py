import re

def extract_python_code(text: str) -> str | None:
    """
    Extracts python code block from a markdown string.
    
    Args:
        text (str): The markdown text containing a python code block.
        
    Returns:
        str | None: The extracted code or None if no block is found.
    """
    pattern = r"```python\s*\n(.*?)```"
    match = re.search(pattern, text, re.DOTALL)
    return match.group(1).strip() if match else None
