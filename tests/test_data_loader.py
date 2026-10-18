import pytest
from data_loader import load_csv


def test_load_csv_missing_file():
    with pytest.raises(FileNotFoundError):
        load_csv("fact_booking.csv")
