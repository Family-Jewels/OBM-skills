# Decision request (parked, work continues)

Date: day 38 (Wed 11 Feb 2026)
Raised by: orchestrator
Issue: E-001 (drinks price step) and E-002 (MAIN-LOUNGE print policy) overlap on MAIN-LOUNGE:DRINKS. The spec says E-002 is queued while E-001 runs on overlapping machines, but E-002 was applied on day 21 (one EUR 8 campaign at MAIN-LOUNGE, the orchestrator's error, recorded in E-002.md) while E-001 was already running. Checker results: F-E-001-1 and F-E-001-2 (fail, overlap), F-E-002-1 and F-E-002-2 (fail, overlap).
Orchestrator action so far: E-002 suspended on day 25 (no campaigns, no change). E-001 price change held (no further change). No new experiment started.
Decision needed from designer or auditor: one of
(a) re-base E-001's clock to start after day 28 (campaign window end), keep E-002 out until E-001 ends (day 56), re-issue E-002 then; or
(b) redefine E-002's slice to MAIN-LOUNGE:SNACK only, with the auditor ruling on the day-21 campaign's residual effect on E-001.
Until decided: no MAIN-LOUNGE campaign, no price change on AI-LOUNGE or MAIN-LOUNGE DRINKS. Operations otherwise continue.

RESOLVED (day 86, by the system's record, not by the orchestrator): E-001 window closed day 62 with verdict V-E-001 "too small to read" (kept prices). E-002 was re-issued by the checker (F-E-002-3, clock day 78 to day 99), slice unchanged. Orchestrator's price freeze lifted on day 65. No further action requested of the orchestrator on this item.
