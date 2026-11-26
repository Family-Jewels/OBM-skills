# Use spare worker time on the depot before buying
Revises: G-004
Applies when: O3
What good looks like: On a day with cash to spare and worker time left over, a strong period looks at the depot and the empty slots first. Loading stock that is already waiting there earns sooner than a purchase, which earns only after delivery and loading, and both use the same worker minutes. A purchase placed on such a day is easiest to judge against the loading minutes the coming days will have. A small price test on a slot that is already stocked is a reasonable use of minutes left over after loading.
Why: Ground truth for days 84 to 113 shows worker time at 0% on 12 of 30 days (about 26% on average), while units waited in the depot on many of those days (133 on day 93, 171 on day 111). Four deliveries of 130 to 160 units landed on days 92 to 110 (PO-1023 to PO-1026). Revenue held near EUR 50 a day from day 64, and the cash gain fell from about EUR 24 a day (days 60 to 90) to about EUR 15 a day (days 90 to 113). See swarm/ground_truth/, swarm/metrics_system.md and swarm/audits/A-003.md.
Source: audit A-003
Revisit: day 143

Fact check: C-010 refuted at day 157 (Claims four deliveries of 130 to 160 units; PO-1023 delivered 120 units on day 92 (its lines sum to 120), so the range is false.)
