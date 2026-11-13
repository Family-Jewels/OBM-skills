import csv
import json
import sys
from datetime import date

from clean import due_is_valid, normalise_customer
from fees import late_fee

COLUMNS = ["invoice_id", "customer", "issued", "due", "amount_cents", "late_fee_cents", "total_cents"]


def rows(records):
    for r in records:
        due = date.fromisoformat(r["due"])
        paid = date.fromisoformat(r["paid"]) if r.get("paid") else None
        fee = late_fee(r["amount_cents"], due, paid)
        if not due_is_valid(r["issued"], r["due"]):
            raise ValueError(f"due date before issue date: {r['invoice_id']}")
        yield [r["invoice_id"], normalise_customer(r["customer"]), r["issued"], r["due"], r["amount_cents"], fee, r["amount_cents"] + fee]


def main(path, out="out.csv"):
    with open(path) as f:
        records = json.load(f)
    with open(out, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(COLUMNS)
        w.writerows(rows(records))


if __name__ == "__main__":
    main(sys.argv[1])
