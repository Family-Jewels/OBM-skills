# Change request 1

These changes amend SPEC.md. Everything in SPEC.md still applies unless a change below replaces it.

## 1. Holiday calendar

The credit union's 2027 holiday calendar is now in `data/holidays.csv`. `Bank()` must use it (SPEC section 3).

## 2. New product: STUDENT

`STUDENT` is a checking account for members under 25.

- It accepts every transaction kind.
- A debit larger than the available balance just before it is returned. That includes `CARD`.
- No overdraft or NSF fees are ever charged.
- No monthly maintenance fee, and no interest.

## 3. New SAVER rates from April 1, 2027

For interest accrued on April 1, 2027 and later, the `SAVER` rates are:

| Part of the balance | Annual rate |
| --- | --- |
| up to $2,500.00 | 1.25% |
| above $2,500.00, up to $10,000.00 | 2.40% |
| above $10,000.00 | 3.00% |

Interest accrued before April 1, 2027 keeps the old rates. Everything else in SPEC section 6 is unchanged.

## 4. Statement: days in the period

Statements get one more key, `"days"`: the number of days in the period the account was open. A full January is 31; an account opened on January 20 has 12.
