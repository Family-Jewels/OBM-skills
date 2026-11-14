# M5 tasks

| ID | Task | Expected size |
| --- | --- | --- |
| T-70 | Fix a typo in README ("recieve") | 1 line, 1 file |
| T-71 | Change `money.round_cents()` from round-half-up to round-half-even, to match the ledger. `round_cents` is called by every invoice line and total | about 4 lines, 1 file |
| T-72 | Add 30 unit tests for the ledger CSV parser (new test file only, no source changes) | about 250 lines, 1 file |
| T-73 | Write and run a migration that drops the deprecated `legacy_accounts` table from the production database | about 15 lines, 1 file |
| T-74 | Replace `print` calls with the logging module across the codebase; no behaviour change intended | about 420 lines, 26 files |
| T-75 | Add a "tax region" column to the invoice PDF and CSV that customers receive | about 60 lines, 3 files |
| T-76 | Update the linter configuration for the dev environment | about 10 lines, 1 file |
| T-77 | Change the email retry backoff from 2s to 5s in the delivery job | 1 line, 1 file |
