from datetime import date


def parse_date(text):
    """ISO date string -> date. Raises ValueError on anything else."""
    return date.fromisoformat(text.strip())


def normalise_customer(name):
    """Trim and collapse spaces; keep the customer's own capitalisation."""
    return " ".join(name.split())


def due_is_valid(issued, due):
    """A due date may not fall before the issue date."""
    return parse_date(due) >= parse_date(issued)
