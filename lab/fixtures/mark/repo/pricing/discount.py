import json
from pathlib import Path

from .money import round_cents

ROOT = Path(__file__).resolve().parent.parent
COUPONS = {"SAVE10": 0.10, "SAVE15": 0.15}


def subtotal_after_discounts(items_total: float, coupon: str | None = None) -> float:
    """Apply the volume tier, then the coupon. Returns the pre-tax subtotal."""
    sub = items_total
    if sub > 500:
        sub = sub * 0.90
    if coupon:
        sub = sub - sub * COUPONS[coupon]
    return round_cents(sub)


def tax_rate(order_date: str) -> float:
    cfg = json.loads((ROOT / "config" / "tax.json").read_text())
    return cfg["rate"]


def order_total(order: dict) -> float:
    items_total = sum(i["price"] * i["qty"] for i in order["items"])
    sub = subtotal_after_discounts(items_total, order.get("coupon"))
    return round_cents(sub * (1 + tax_rate(order["date"])))
