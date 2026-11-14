import json
from pathlib import Path
from pricing.discount import subtotal_after_discounts, order_total

def o(date, total, coupon=None):
    return {"id": 1, "date": date, "coupon": coupon, "items": [{"sku": "X", "price": total, "qty": 1}]}

def test_cap_binds():            assert subtotal_after_discounts(700.0, "SAVE15") == 580.0
def test_cap_save10_large():     assert subtotal_after_discounts(1000.0, "SAVE10") == 850.0
def test_cap_not_binding():      assert subtotal_after_discounts(300.0, "SAVE15") == 255.0
def test_tier_only():            assert subtotal_after_discounts(600.0) == 540.0
def test_ticket_8841():          assert order_total(json.load(open("fixtures/order_8841.json"))) == 614.80
def test_tax_first_half():       assert order_total(o("2026-05-01", 100.0)) == 106.50
def test_tax_second_half():      assert order_total(o("2026-08-01", 100.0)) == 106.00
def test_tax_boundary():         assert order_total(o("2026-07-01", 100.0)) == 106.00
