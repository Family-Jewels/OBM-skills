from pricing.discount import subtotal_after_discounts


def test_small_order_no_discount():
    assert subtotal_after_discounts(200.0) == 200.0


def test_tier_only():
    assert subtotal_after_discounts(600.0) == 540.0


def test_coupon_small_order():
    assert subtotal_after_discounts(100.0, "SAVE10") == 90.0


def test_coupon_over_500():
    assert subtotal_after_discounts(700.0, "SAVE15") == 580.0
