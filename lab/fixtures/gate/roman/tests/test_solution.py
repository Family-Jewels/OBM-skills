import pytest
from solution import to_roman, from_roman
@pytest.mark.parametrize("n,s", [(1,"I"),(4,"IV"),(9,"IX"),(14,"XIV"),(40,"XL"),(90,"XC"),(400,"CD"),(1994,"MCMXCIV"),(2024,"MMXXIV"),(3999,"MMMCMXCIX")])
def test_both(n, s):
    assert to_roman(n) == s and from_roman(s) == n
def test_roundtrip():
    assert all(from_roman(to_roman(n)) == n for n in range(1, 4000))
@pytest.mark.parametrize("bad", ["IIII", "IC", "VX", "", "MMMM", "ABC"])
def test_invalid(bad):
    with pytest.raises(ValueError): from_roman(bad)
def test_range():
    for n in (0, 4000):
        with pytest.raises(ValueError): to_roman(n)
