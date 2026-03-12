import sys
import os
import pandas as pd

# Add the project root to sys.path for imports
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

try:
    from constants.settings import DF_UPDATE_SENTINEL, MODEL_NAME
    from services.gndec_service import gndec_answer
    from services.execution_service import extract_python_code, execute_code
    print("✅ Imports successful.")
except Exception as e:
    print(f"❌ Import failed: {e}")
    sys.exit(1)

def test_gndec():
    res = gndec_answer("When was GNDEC established?")
    if "1956" in res:
        print("✅ GNDEC service: OK")
    else:
        print(f"❌ GNDEC service: Failed (got {res})")

def test_extraction():
    code = extract_python_code("```python\nprint(1)\n```")
    if code == "print(1)":
        print("✅ Code extraction: OK")
    else:
        print(f"❌ Code extraction: Failed (got {code})")

def test_execution():
    df = pd.DataFrame({"A": [1, 2]})
    stdout, new_df, fig = execute_code("df['B'] = df['A'] * 2", df)
    if "B" in new_df.columns and new_df["B"].iloc[1] == 4:
        print("✅ Code execution: OK")
    else:
        print(f"❌ Code execution: Failed")

if __name__ == "__main__":
    print("--- Starting Verification ---")
    test_gndec()
    test_extraction()
    test_execution()
    print("--- Verification Finished ---")
