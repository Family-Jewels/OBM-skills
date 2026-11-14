from solution import median
def test_even_spec(): assert median([1, 2, 3, 4]) == 2.5
def test_more(): assert median([4, 1, 3, 2, 6, 5]) == 3.5 and median([2, 8]) == 5
