import pytest
from duration import parse_duration

def test_hm(): assert parse_duration("1h30m") == 5400
def test_s(): assert parse_duration("45s") == 45
def test_m(): assert parse_duration("90m") == 5400
def test_days(): assert parse_duration("2d") == 172800
def test_mixed(): assert parse_duration("1d1h1m1s") == 90061
def test_bad():
    with pytest.raises(ValueError):
        parse_duration("soon")
