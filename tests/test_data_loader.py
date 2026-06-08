import io
import pandas as pd
import pytest
from modules.data_loader import DataLoader

class MockUploadedFile(io.BytesIO):
    def __init__(self, content, name):
        super().__init__(content)
        self.name = name

def test_load_file_csv():
    csv_data = b"col1,col2\n1,2\n3,4"
    mock_file = MockUploadedFile(csv_data, "data.csv")
    df, error = DataLoader.load_file(mock_file)
    assert error is None
    assert df is not None
    assert df.shape == (2, 2)
    assert list(df.columns) == ["col1", "col2"]

def test_load_file_csv_uppercase():
    csv_data = b"col1,col2\n1,2\n3,4"
    mock_file = MockUploadedFile(csv_data, "DATA.CSV")
    df, error = DataLoader.load_file(mock_file)
    assert error is None
    assert df is not None
    assert df.shape == (2, 2)

def test_load_file_xlsx():
    # Create small in-memory xlsx file
    output = io.BytesIO()
    df_temp = pd.DataFrame({"A": [10, 20], "B": [30, 40]})
    df_temp.to_excel(output, index=False, engine='openpyxl')
    xlsx_data = output.getvalue()
    
    mock_file = MockUploadedFile(xlsx_data, "test.xlsx")
    df, error = DataLoader.load_file(mock_file)
    assert error is None
    assert df is not None
    assert df.shape == (2, 2)
    assert list(df.columns) == ["A", "B"]

def test_load_file_xlsx_uppercase():
    output = io.BytesIO()
    df_temp = pd.DataFrame({"A": [10, 20], "B": [30, 40]})
    df_temp.to_excel(output, index=False, engine='openpyxl')
    xlsx_data = output.getvalue()
    
    mock_file = MockUploadedFile(xlsx_data, "TEST.XLSX")
    df, error = DataLoader.load_file(mock_file)
    assert error is None
    assert df is not None
    assert df.shape == (2, 2)

def test_load_file_unsupported():
    mock_file = MockUploadedFile(b"some content", "data.txt")
    df, error = DataLoader.load_file(mock_file)
    assert df is None
    assert "Unsupported file format" in error
