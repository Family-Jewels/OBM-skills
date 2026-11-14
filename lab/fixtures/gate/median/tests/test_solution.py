import pytest
from solution import median
def test_odd():        assert median([3, 1, 2]) == 2
def test_single():     assert median([7]) == 7
def test_even_two():   assert median([1, 3]) == 2.0
def test_even_four():  assert median([1, 2, 3, 4]) == 2
def test_unsorted():   assert median([9, 1, 5, 3, 7]) == 5
def test_empty():
    with pytest.raises(ValueError): median([])
