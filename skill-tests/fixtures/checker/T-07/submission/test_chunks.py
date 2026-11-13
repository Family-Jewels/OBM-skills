from chunks import chunk

def test_even(): assert chunk([1, 2, 3, 4], 2) == [[1, 2], [3, 4]]
def test_ragged(): assert chunk([1, 2, 3], 2) == [[1, 2], [3]]
def test_empty(): assert chunk([], 3) == []
def test_big_n(): assert chunk([1, 2], 5) == [[1, 2]]
