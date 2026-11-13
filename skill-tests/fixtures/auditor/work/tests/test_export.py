import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from fees import late_fee
from export import COLUMNS


def test_columns():
    assert COLUMNS == ["invoice_id", "customer", "issued", "due", "amount_cents", "late_fee_cents", "total_cents"]


def test_not_late():
    assert late_fee(25000, date(2026, 10, 20), date(2026, 10, 15)) == 0


def test_one_period():
    assert late_fee(40000, date(2026, 10, 5), date(2026, 10, 12)) == 600
