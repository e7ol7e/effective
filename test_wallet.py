import pytest
import json
from wallet import Record, Wallet, validate_date  


# Fixture to setup a wallet with a predefined file path
@pytest.fixture
def wallet(tmp_path):
    # Define the path to the temporary wallet file
    test_wallet_file = tmp_path / "wallet.txt"
    # Initialize the file with an empty list to ensure valid JSON structure
    with open(test_wallet_file, 'w') as f:
        json.dump([], f)
    # Create a Wallet instance with the path to the temporary file
    return Wallet(filename=str(test_wallet_file))

def test_wallet_add_and_find_record(wallet):
    record = Record("2023-01-01", "Income", 1000.0, "Salary")
    wallet.add_record(record)
    found_records = wallet.find_records("2023-01-01")
    assert len(found_records) == 1
    assert found_records[0].to_dict() == record.to_dict()

def test_validate_date():
    assert validate_date("2023-01-01") is True
    assert validate_date("01-01-2023") is False

def test_removing_a_record(wallet):
    record1 = Record("2023-01-01", "Income", 1000.0, "Salary")
    record2 = Record("2023-02-01", "Expense", 500.0, "Groceries")
    wallet.add_record(record1)
    wallet.add_record(record2)
    assert len(wallet.records) == 2
    wallet.remove_record(0)
    assert len(wallet.records) == 1
    assert wallet.records[0].to_dict() == record2.to_dict()

def test_editing_a_record(wallet):
    original_record = Record("2023-01-01", "Income", 1000.0, "Salary")
    updated_record = Record("2023-01-01", "Income", 2000.0, "Updated Salary")
    wallet.add_record(original_record)
    wallet.edit_record(0, updated_record)
    assert wallet.records[0].amount == 2000.0
    assert wallet.records[0].description == "Updated Salary"

def test_record_string_representation():
    record = Record("2023-01-01", "Income", 1000.0, "Salary")
    expected_string = "2023-01-01 - Income - 1000.0 - Salary"
    assert str(record) == expected_string

def test_load_records_from_empty_file(tmp_path):
    empty_wallet_file = tmp_path / "empty_wallet.txt"
    # Ensure the file exists but is empty
    empty_wallet_file.touch()
    # Attempt to create a Wallet instance with the empty file
    try:
        Wallet(filename=str(empty_wallet_file))
        assert True  # Pass the test if no exception is raised
    except json.JSONDecodeError:
        pytest.fail("JSONDecodeError raised while loading records from an empty file")

def test_adding_multiple_records():
    wallet = Wallet(filename="test_wallet.txt")
    record1 = Record("2023-01-01", "Income", 100.0, "Salary")
    record2 = Record("2023-01-02", "Expense", 50.0, "Coffee")
    wallet.add_record(record1)
    wallet.add_record(record2)
    assert len(wallet.records) == 2
    with open("test_wallet.txt", 'w') as file:
        pass

def test_negative_amount():
    record = Record("2023-01-01", "Expense", -50.0, "Coffee")
    assert record.amount == -50.0

def test_record_string_representation():
    record = Record("2023-01-01", "Income", 100.0, "Salary")
    expected_str = "2023-01-01 - Income - 100.0 - Salary"
    assert str(record) == expected_str

def test_empty_wallet():
    wallet = Wallet(filename="test_wallet.txt")
    assert len(wallet.records) == 0
    with open("test_wallet.txt", 'w') as file:
        pass

def test_record_initialization():
    record = Record("2023-01-01", "Income", 100.0, "Salary")
    assert record.date == "2023-01-01"
    assert record.category == "Income"
    assert record.amount == 100.0
    assert record.description == "Salary"

@pytest.mark.parametrize("date_text,expected", [
    ("2023-01-05", True),
    ("2023-02-29", False),  # 2023 is not a leap year
    ("01-01-2023", False),
    ("2023/01/01", False),
])
def test_validate_date(date_text, expected):
    assert validate_date(date_text) == expected, f"validate_date failed for {date_text}"

def test_wallet_edit_record():
    wallet = Wallet(filename="test_wallet.txt")
    record = Record("2023-01-04", "Expense", 100.0, "Books")
    wallet.add_record(record)
    new_record = Record("2023-01-04", "Expense", 150.0, "Books and Supplies")
    wallet.edit_record(0, new_record)
    assert wallet.records[0].amount == 150.0 and wallet.records[0].description == "Books and Supplies", \
           "Wallet edit_record method failed"
    with open("test_wallet.txt", 'w') as file:
        pass