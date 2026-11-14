import pytest
from solution import parse_duration
def test_h_m():      assert parse_duration("1h30m") == 5400
def test_s():        assert parse_duration("45s") == 45
def test_h():        assert parse_duration("2h") == 7200
def test_all():      assert parse_duration("1h1m1s") == 3661
def test_minutes():  assert parse_duration("90m") == 5000
def test_bad():
    with pytest.raises(ValueError): parse_duration("abc")
