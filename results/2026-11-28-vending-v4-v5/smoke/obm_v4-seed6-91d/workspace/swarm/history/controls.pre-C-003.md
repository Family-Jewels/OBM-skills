# Controls (risk branch; owned by the controls owner)

Each control is one line: `- <control> | guards: <risk> | review at point <N> | from <D-NNN or REQ-NNN>`.

- Before calling wait_for_next_day, while worker minutes remain before 17:00: call get_machine_inventory; if any slot is empty and the depot holds stock, restock those slots (restock_machine) until the minutes run out or no empty slot with depot stock is left. Do not wait with minutes unused while both hold. | guards: idle worker minutes while slots are empty and stock sits in the depot (the fill throughput that drives slots_selling; D-002 found about 420 minutes unused on day 19 with 63 of 72 slots empty) | review at point 5 | from D-002 (REQ-010)

Last reviewed: day 27 of 91 (C-002, from D-002). Earlier: day 16 (C-001, no worker control; D-001 was an instrumentation fault). The previous version is in swarm/history/controls.pre-C-002.md.
