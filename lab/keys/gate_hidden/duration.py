import pytest
from solution import parse_duration
def test_minutes_spec(): assert parse_duration("90m") == 5400
def test_more(): assert parse_duration("3m") == 180 and parse_duration("1h") == 3600 and parse_duration("10m5s") == 605
