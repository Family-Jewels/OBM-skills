# Controls (risk branch; owned by the controls owner)

No controls are in force. Each control is one line: `- <control> | guards: <risk> | review at point <N> | from <D-NNN or REQ-NNN>`.

Last reviewed: day 16 of 91 (C-001). Diagnosis D-001 (day7-measure-missing) found an instrumentation fault in the system's daily ground-truth read, not an agent action, so it added no worker control. See swarm/audits/C-001.md.
