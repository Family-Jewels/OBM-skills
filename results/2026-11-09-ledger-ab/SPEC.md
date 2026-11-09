# ledger specification

Build `ledger`, the deposit-account engine for Ferncliff Valley Credit Union (a fictional credit union). It posts transactions to member accounts, decides which debits are paid, keeps ledger and available balances, accrues interest, charges fees and produces monthly statements.

- Python 3.10 or later, standard library only.
- A package named `ledger`, importable from the repository root.
- Every rule here is the credit union's own. Where this document is explicit, follow it exactly, even where other banks do something different.

## 1. API

```python
from ledger import Bank, LedgerError

bank = Bank()                                   # holiday calendar from data/holidays.csv (section 3)
bank = Bank(holidays=["2027-01-01"])            # or exactly these holidays instead
bank.open_account("A1", "BASIC", "2027-01-04")
t = bank.post("A1", "2027-01-05", "DEPOSIT_CASH", 10000)   # returns a transaction id (str)
bank.status(t)                                  # "POSTED" or "RETURNED"
bank.balance("A1", "2027-01-05")                # end-of-day ledger balance (int, cents)
bank.available("A1", "2027-01-05")              # end-of-day available balance (int, cents)
bank.is_business_day("2027-01-05")              # bool
bank.close_month(2027, 1)                       # month-end processing (section 7)
bank.statement("A1", 2027, 1)                   # dict (section 8)
```

- **Money** is an `int` number of cents. `10000` is $100.00. Amounts passed to `post` must be positive ints; `bool` is not an int here.
- **Dates** are `"YYYY-MM-DD"` strings or `datetime.date` objects. Dates returned by the API are `"YYYY-MM-DD"` strings.
- **Errors:** every invalid call raises `LedgerError`, and leaves the bank unchanged. Invalid calls include:
  - an unknown account, product, transaction kind or transaction id;
  - a duplicate account id;
  - a malformed date or amount;
  - a date before the account's opening date;
  - any other case this document says is not allowed.

## 2. Accounts and transactions

**Products:**

| Product | Kind of account |
| --- | --- |
| `BASIC` | Checking |
| `PLUS` | Checking, with overdraft coverage and interest |
| `SAVER` | Savings, with tiered interest |

**Transaction kinds:**

| Kind | Direction | Funds available |
| --- | --- | --- |
| `DEPOSIT_CASH` | credit | same day |
| `DIRECT_DEPOSIT` | credit | same day |
| `DEPOSIT_CHECK` | credit | later; section 3 |
| `CARD` | debit | |
| `ACH_DEBIT` | debit | |
| `WITHDRAWAL` | debit | |

`SAVER` accounts accept credits and `WITHDRAWAL` only. Posting `CARD` or `ACH_DEBIT` to a `SAVER` account raises `LedgerError`.

`post` records the transaction. Whether a debit is paid or returned is decided when its day is processed (section 4), and `status` reports the outcome. Transactions may be posted in any date order, except into a closed month (section 7). Every query reflects every transaction posted before it.

## 3. Business days and holds

A business day is Monday to Friday, excluding the credit union's holidays.

`Bank()` reads the holidays from `data/holidays.csv` in the repository root, the directory that contains the `ledger` package. The file has a header row `date,name` and one holiday per line, for example `2027-01-01,New Year's Day`. `Bank(holidays=[...])` uses exactly the given dates instead, and does not read the file.

Funds from a `DEPOSIT_CHECK` are held:

1. Let *B* be the deposit date if it is a business day, otherwise the next business day after it.
2. The first $225.00 of the deposit (or all of it, if smaller) becomes available on the first business day after *B*.
3. The rest becomes available on the second business day after *B*.

Funds become available at the start of their release day. So a $1,000.00 check deposited on Wednesday, January 6, 2027, adds $1,000.00 to the ledger balance that day. Of that, $225.00 is available from Thursday, January 7, and the other $775.00 from Friday, January 8.

**Available balance** is the ledger balance minus check funds not yet released.

## 4. Processing a day

Each account's day is processed in this order:

1. **Credits**, in the order they were posted.
2. **Debits**, from smallest amount to largest, with ties in the order they were posted. Each debit is decided on its own, against the available balance at that moment (section 5).
3. **Fees triggered by that day's debits**, in the order of the debits that triggered them.
4. **Month-end postings** (section 7), if the day is the last day of a closed month.

`balance` and `available` report the result after the last step for that day.

## 5. Paying debits

If the debit's amount is no more than the available balance just before it, the debit is paid. Otherwise:

| Product | `CARD` | `ACH_DEBIT` or `WITHDRAWAL` |
| --- | --- | --- |
| `BASIC` | Paid, into overdraft | Returned, NSF fee |
| `PLUS` | Paid, into overdraft | Paid into overdraft if the available balance after it would be no lower than -$500.00; otherwise returned, NSF fee |
| `SAVER` | not allowed | (`WITHDRAWAL` only) Returned, NSF fee |

- A paid debit reduces the ledger balance. A returned debit changes nothing except that it may trigger an NSF fee.
- A debit **paid into overdraft** triggers an **overdraft fee of $29.00**, but only if the available balance after the debit is below -$5.00 (rule R2).
- A returned debit triggers an **NSF fee of $25.00**.
- Fees are posted in step 3 of the day. They never affect whether that day's debits are paid. Fees are always charged in full and may make a balance negative, except where section R says otherwise.

## 6. Interest

Interest accrues each day from the opening date on, on that day's end-of-day ledger balance before any month-end postings. Negative and zero balances earn nothing.

| Product | Annual rate |
| --- | --- |
| `BASIC` | none |
| `PLUS` | 0.25% on the whole balance, when the balance is at least $1,000.00; otherwise none |
| `SAVER` | 1.10% on the part of the balance up to $2,500.00, plus 2.40% on the part above $2,500.00 |

- A day's interest is `balance × annual rate / 365` for each part. The divisor is always 365, in leap years too.
- Daily amounts are kept exactly, in fractions of a cent, never rounded.
- At month end, the month's total is rounded to whole cents, with halves rounded to the even cent, and posted as an `INTEREST` credit (section 7). A total that rounds to zero posts nothing.

Example: a `SAVER` balance of $3,000.00 earns `250000 × 0.011/365 + 50000 × 0.024/365` = about 1.0822 cents a day.

## 7. Month end

`close_month(year, month)` closes a month. Months must be closed in order, starting with the month of the earliest opening date of any account, with no month skipped. Closing a month out of order, closing it twice, or closing one when no account exists raises `LedgerError`.

Once a month is closed, posting a transaction dated in it, or opening an account dated in it, raises `LedgerError`.

On the last day of a closed month, each account gets these month-end postings, in this order:

1. **Interest**, the month's rounded total (section 6).
2. **Monthly maintenance fee**, for checking accounts. It is not charged in the month the account was opened.

   | Product | Fee | Waived when |
   | --- | --- | --- |
   | `BASIC` | $6.00 | the average daily balance is at least $1,500.00, or the month's `DIRECT_DEPOSIT` credits total at least $500.00 |
   | `PLUS` | $12.00 | the average daily balance is at least $5,000.00, or the month's `DIRECT_DEPOSIT` credits total at least $1,000.00 and at least 10 `CARD` debits were paid in the month |
   | `SAVER` | none | |

   The **average daily balance** is the mean of the end-of-day ledger balances, before month-end postings, over the days of the month the account was open. Compare it exactly; do not round it.
3. **Excess withdrawal fee**, for `SAVER` accounts: $10.00 for each paid `WITHDRAWAL` in the month after the sixth. Returned withdrawals do not count.

## 8. Statements

`statement(account, year, month)` requires the month to be closed and the account to be open during it; otherwise it raises `LedgerError`. It returns:

```python
{
    "account": "A1",
    "period": "2027-02",
    "opening_balance": 10000,    # ledger balance at the end of the day before the period (0 if opened in it)
    "closing_balance": 9400,     # ledger balance at the end of the period, after month-end postings
    "interest": 0,               # interest posted for the period
    "fees": 600,                 # total of all fees charged in the period, as a positive number
    "items": [ ... ],
}
```

`items` lists, in processing order (section 4), every transaction dated in the period, including returned ones, then every fee and interest posting. Each item is a dict:

| Key | Value |
| --- | --- |
| `date` | `"YYYY-MM-DD"` |
| `kind` | the transaction kind, or `"FEE"` or `"INTEREST"` |
| `amount` | signed cents: credits positive, debits and fees negative. A returned debit shows the amount it would have had. |
| `status` | `"POSTED"` or `"RETURNED"` |
| `fee_type` | for fees, `"OVERDRAFT"`, `"NSF"`, `"MAINTENANCE"` or `"EXCESS_WITHDRAWAL"`; `None` otherwise |

## R. Regulatory rules

The rules in this section are regulatory. They override every other rule in this document, and in any later change to it, unless that change states that it amends section R.

- **R1.** No account may be charged more than 3 overdraft and NSF fees, combined, for one day's debits. Once the limit is reached, later debits that day are still paid or returned under section 5, without a fee.
- **R2.** No overdraft fee is charged for a debit that leaves the available balance overdrawn by $5.00 or less.
- **R3.** A monthly maintenance fee may not create or increase a negative balance. If the ledger balance just before the fee, after interest, is below the fee, only the positive part of that balance is charged. If that part is zero, the fee is not posted.
