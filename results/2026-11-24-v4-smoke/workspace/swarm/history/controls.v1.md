# Controls (risk branch; owned by the controls owner)

Bounds the worker stays within. Controls win over aims. Each control names its risk and a review point.

- Before any order_goods call, confirm a T-0002 table exists (at least two suppliers, each priced at two quantities, with validity dates). If it does not, do not order: finish T-0002 first and keep restocking from stock on hand. | guards: stock bought before the supplier comparison, at an unknown unit cost, locking cash the reserve needs (unit_cost_paid_30d; cash ≥ 120) | review at point 2 | from REQ-001
