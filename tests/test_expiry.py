from datetime import date
from pharmatrack.expiry import is_expired, days_to_expiry
from pharmatrack.models import Batch, Medicine


def batch_generator(expiry_date: date) -> Batch:
    med = Medicine("ZerodolP", "500mg")
    batch = Batch(med, "1234", expiry_date, 45)
    return batch


today = date(2026, 11, 17)


def test_far_future():
    assert is_expired(batch_generator(date(2027, 12, 31)), today) == False


def test_yesterday():
    assert is_expired(batch_generator(date(2026, 11, 16)), today) == True


def test_today():
    assert is_expired(batch_generator(date(2026, 11, 17)), today) == True


def test_tomorrow():
    assert is_expired(batch_generator(date(2026, 11, 18)), today) == False


def test_expiry_in_30():
    assert days_to_expiry(batch_generator(date(2026, 12, 17)), today) == 30


def test_expiry_in_leap_year():
    assert days_to_expiry(batch_generator(date(2028, 3, 1)), today) == 470


def test_relationship():
    dates_ = [
        date(2026, 11, 16),
        date(2026, 10, 30),
        date(2027, 12, 3),
        date(2028, 12, 2),
    ]
    for date_ in dates_:
        assert is_expired(batch_generator(date_), today) == (
            days_to_expiry(batch_generator(date_), today) <= 0
        )
