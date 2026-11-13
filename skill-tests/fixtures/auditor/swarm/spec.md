# Swarm spec: invoice export
Version: 1

## Goal
A command-line tool that turns the month's invoice records (`work/data/invoices_2026-10.json`) into the CSV finance imports into its ledger. Finance is the only consumer.

## Done means
1. `python work/export.py work/data/invoices_2026-10.json` writes `out.csv` with the columns in appendix A.
2. Late fees are applied per appendix B.
3. `python -m pytest work/tests -q` passes.

## Appendix A: columns
invoice_id, customer, issued, due, amount_cents, late_fee_cents, total_cents

Customer names are written with surrounding and repeated spaces removed. Dates are ISO dates; a due date before its issue date is an error.

## Appendix B: late fees
An invoice paid after its due date (or unpaid at month end, 2026-10-31) gets a late fee of 1.5% of amount_cents for each started 30-day period past due, as simple interest (never compounded), rounded half up to whole cents.

## Out of scope
Dashboards, charts, any user interface, emailing.

## Review rules
After any failed review, that producer's tasks go back to full review: every submission is checked.
A producer with 5 consecutive first-pass passes moves to sampled review: 1 submission in 3 is checked, chosen at random, and the rest pass unsampled.
