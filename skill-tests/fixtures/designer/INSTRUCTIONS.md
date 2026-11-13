# Set this up to run on its own

A request from the head of account management:

> Every Monday my account managers should get a list of the customers most likely to churn, so they can reach out that week. Can you set this up so it runs on its own? We want to start with this month's data.

The team of AI agents that will do the work has this environment, and nothing else:

- `env/accounts.csv`: an export of 1,200 customer accounts, refreshed every Monday morning. The columns are described in `env/columns.md`.
- `env/churned_2025.csv`: accounts that cancelled last year.
- The agents can read and write files and run Python with pandas and scikit-learn. There is no network access, no email, no access to the CRM or any messaging tool, and no database.
- A human will run the agents' schedule. Nobody will review their work week to week.

Your job is to design the work system the agents will follow, not to do the work. Write the design as files in a folder named `swarm/` in this directory. At minimum, write `swarm/spec.md`.
