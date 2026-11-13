from rounding import round_half_up

def test_down(): assert round_half_up(2.4) == 2
def test_up(): assert round_half_up(2.6) == 3
def test_half(): assert round_half_up(1.5) == 2
def test_negative(): assert round_half_up(-0.4) == 0
