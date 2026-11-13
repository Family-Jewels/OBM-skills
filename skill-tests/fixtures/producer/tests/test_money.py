from money import convert, format_money


def test_format_usd():
    assert format_money(123456, "USD") == "$1,234.56"


def test_format_eur():
    assert format_money(123456, "EUR") == "€1,234.56"


def test_format_zero_and_negative():
    assert format_money(0, "USD") == "$0.00"
    assert format_money(-500, "USD") == "-$5.00"


def test_convert_usd_to_eur():
    assert convert(10000, "USD", "EUR") == 9231


def test_convert_eur_to_gbp():
    assert convert(10000, "EUR", "GBP") == 8774


def test_convert_same_currency():
    assert convert(4321, "USD", "USD") == 4321
