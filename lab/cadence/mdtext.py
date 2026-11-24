"""Markdown-tolerant reading of role records (engine v4). Task-agnostic.

Agents often bold or code-format the lines the engine parses ('**Fault: yes**', 'Fault key: `cash-low`',
'**Requests**' as a heading). plain() removes that emphasis so every parser reads the same plain lines, and
section() finds a '## Title' section however it is decorated.
"""
import re

_BOLD_HEADING = re.compile(r"^\s*\*\*\s*([A-Za-z][^*:]*?)\s*:?\s*\*\*\s*:?\s*$")

def plain(text):
    out = []
    for line in (text or "").splitlines():
        m = _BOLD_HEADING.match(line)
        if m:  # a line that is only a bold title is a heading
            out.append("## " + m.group(1))
            continue
        s = line.replace("**", "").replace("`", "")
        s = re.sub(r"(?<=\S)\*(?!\S)|(?<!\S)\*(?=\S)", "", s)  # single-star italics; a '* ' bullet stays
        out.append(s)
    return "\n".join(out)

def section(text, title, suffix=True):
    """The body of the section headed `title` (any heading level, an optional '(...)' note and colon), or ''."""
    tail = r"(?:\s*\(.*\))?" if suffix else ""
    m = re.search(rf"^#+\s*{title}{tail}\s*:?\s*$(.*?)(?=^#+\s|\Z)", plain(text), re.M | re.S | re.I)
    return m.group(1) if m else ""
