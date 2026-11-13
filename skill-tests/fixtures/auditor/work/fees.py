from datetime import date


def late_fee(amount_cents, due, paid, month_end=date(2026, 10, 31)):
    """Late fee per spec appendix B."""
    end = paid or month_end
    days = (end - due).days
    if days <= 0:
        return 0
    periods = (days + 29) // 30
    fee = amount_cents
    for _ in range(periods):
        fee = fee * 1.015
    return int(round(fee - amount_cents))
