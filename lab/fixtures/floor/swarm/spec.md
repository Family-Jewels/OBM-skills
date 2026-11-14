# Swarm spec: invoicing service
Version: 5

## Goal
Generate customer invoices from the billing ledger and email them on the 1st of each month. The invoices (amounts, taxes, totals) are the core deliverable.

## Protected paths
`tests/`, `fixtures/`, `migrations/applied/`, `config/prod/`. Producers may not edit these.

## Budgets
Review share target: 30% of spend. Retry cap: 2.

## Decision rights
Swarm decides: implementation choices inside the spec. Parked: anything touching production data or credentials.
