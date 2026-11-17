from pharmatrack.models import Batch
from datetime import date


def is_expired(batch: Batch, today: date) -> bool:
    """A batch is expired on or after its expiry date"""
    return today >= batch.expiry_date


def days_to_expiry(batch: Batch, today: date) -> int:
    """Gives the days left in expiring og the medicine"""

    delta = batch.expiry_date - today
    return delta.days
