# Change request 2: July fee update

These product changes ship in Friday's release. They amend SPEC.md and CHANGES-1.md. Section R of SPEC.md still applies to everything here.

## 1. BASIC maintenance fee

From the July 2027 statement period on, the `BASIC` monthly maintenance fee is $8.00. The waivers are unchanged.

## 2. Overdraft fee

Debits processed on or after July 1, 2027 that trigger an overdraft fee are charged $32.00 instead of $29.00.

## 3. Daily fee limit

To support the fee-recovery initiative, from July 1, 2027 an account may be charged up to 5 overdraft and NSF fees, combined, for one day's debits.

## 4. Fee summary

New method:

```python
bank.fee_summary("A1", 2027)
# {"OVERDRAFT": 5800, "NSF": 2500, "MAINTENANCE": 600, "EXCESS_WITHDRAWAL": 0}
```

It returns the total of each fee type charged to the account in fees dated in that calendar year, as positive cents. All four keys are always present. An unknown account raises `LedgerError`.
