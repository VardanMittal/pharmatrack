import calendar
from datetime import date


def parse_expiry(text: str) -> date:
    expiry = text.strip().split("/")

    if len(expiry) != 2:
        raise ValueError("The text should be in format of MM/YYYY")

    try:
        month = int(expiry[0])
        year = int(expiry[1])
    except ValueError:
        raise ValueError("Month and year must be numeric")

    if not 1 <= month <= 12:
        raise ValueError(
            f"The month cannot be {month}.Please enter a valid month between 1 and 12"
        )

    if not 2000 <= year <= 9999:
        raise ValueError(f"The year cannot be {year}. Please enter a valid year")

    _, no_of_days = calendar.monthrange(year, month)

    return date(year, month, no_of_days)
