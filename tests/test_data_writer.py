from src.data_writer import save_records
import pandas as pd
import pytest


def test_save_records_creates_csv(tmp_path, monkeypatch):
    df = pd.DataFrame({
        "booking_id": [101, 102],
        "no_guests": [4, 6]
    })

    monkeypatch.setattr(
        "src.data_writer.Path.resolve",
        lambda self: tmp_path / "src" / "data_writer.py"
    )

    save_records(df, "processed/test_bookings.csv")

    output_file = tmp_path/ "data" / "processed" / "test_bookings.csv"

    assert output_file.exists()

    saved_df = pd.read_csv(output_file)

    assert len(saved_df) == 2
    assert list(saved_df.columns) == ["booking_id", "no_guests"]


def test_save_records_does_not_write_index(tmp_path, monkeypatch):
    df = pd.DataFrame({
        "booking_id": [101, 102],
        "no_guests": [2, 3]
    })

    monkeypatch.setattr(
        "src.data_writer.Path.resolve",
        lambda self: tmp_path / "src" / "data_writer.py"
    )

    save_records(df, "processed/test_bookings.csv")

    output_file = tmp_path / "data" / "processed" / "test_bookings.csv"
    saved_df = pd.read_csv(output_file)

    assert "Unnamed: 0" not in saved_df.columns
    assert list(saved_df.columns) == ["booking_id", "no_guests"]


def test_save_records_propagates_write_error(tmp_path, monkeypatch):
    df = pd.DataFrame({"booking_id": [101]})

    def raise_os_error(*args, **kwargs):
        raise OSError("Simulated file write failure")

    monkeypatch.setattr(pd.DataFrame, "to_csv", raise_os_error)

    monkeypatch.setattr(
        "src.data_writer.Path.resolve",
        lambda self: tmp_path / "src" / "data_writer.py"
    )

    with pytest.raises(OSError, match="Simulated file write failure"):
        save_records(df, "processed/test_bookings.csv")

