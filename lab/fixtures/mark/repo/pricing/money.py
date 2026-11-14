from decimal import Decimal, ROUND_HALF_UP


def round_cents(x) -> float:
    """Round to cents, half up. Shared with the invoicing module."""
    return float(Decimal(str(x)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))
