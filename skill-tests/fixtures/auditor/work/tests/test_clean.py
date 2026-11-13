import sys
from datetime import date
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from clean import due_is_valid, normalise_customer, parse_date


def test_parse_date():
    assert parse_date("2026-10-05") == date(2026, 10, 5)


def test_parse_date_rejects_garbage():
    with pytest.raises(ValueError):
        parse_date("05/10/2026")


def test_parse_date_leap_day_and_month_end():
    assert parse_date("2028-02-29") == date(2028, 2, 29)
    assert parse_date(" 2026-10-31 ") == date(2026, 10, 31)


def test_normalise_customer():
    assert normalise_customer("  Acme   Corp ") == "Acme Corp"


def test_due_is_valid():
    assert due_is_valid("2026-10-01", "2026-10-20") is True
    assert due_is_valid("2026-10-20", "2026-10-01") is False
