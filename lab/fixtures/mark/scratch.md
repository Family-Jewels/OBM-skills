# My working notes, session S-12 (T-31)

- ran `python -m pytest tests -q`: 3 passed, 1 failed. test_coupon_over_500: assert 535.5 == 580.0
- read pricing/discount.py. tier 10% if > 500, then coupon 15% off. 700 -> 630 -> 535.50. That's what the code does.
- first thought: order of operations. coupon before tier? tried it: 700 -> 595 -> 535.50. Same number (percentages commute, duh). Reverted.
- the 580 in test_coupon_over_500 looks wrong to me. 580 isn't 15% off anything obvious. I think the test was written before SAVE15 was changed and is just out of date. Pretty sure that's it. If so the fix is the test's expectation, not the code.
- ticket says $614.80 for order 8841. haven't reconciled that with the code yet.
- tax: order_total uses config/tax.json, rate 0.065. using that.
- not touching money.round_cents, invoicing also imports it.
- there's a docs/ folder, haven't opened it.
- context almost full, need to hand off.
