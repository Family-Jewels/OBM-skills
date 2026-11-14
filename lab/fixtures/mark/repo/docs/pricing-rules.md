# Pricing rules (owner: finance, last updated 2026-07-02)

1. Volume tier: orders whose item total is over $500 get 10% off the item total.
2. Coupons apply after the volume tier. A percentage coupon is capped at $50 off per order.
3. Tax is applied last, at the rate in force on the order date. Rate files live in `config/`, one per period, each with `valid_from` and `valid_until`. Use the file whose period contains the order date.
4. Round to cents only at the end of each step, half up.
