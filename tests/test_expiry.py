from datetime import date

from pharmatrack.expiry import days_to_expiry, is_expired
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


def test_already_expired_5_days_back():
    assert days_to_expiry(batch_generator(date(2026, 11, 12)), today) == -5


def test_leap_year_testing_for_date_of_expiry():
    assert days_to_expiry(batch_generator(date(2028, 3, 1)), date(2028, 2, 28)) == 2


def test_normal_year_testing_for_date_of_expiry():
    assert days_to_expiry(batch_generator(date(2027, 3, 1)), date(2027, 2, 28)) == 1


def test_expiry_in_leap_year():
    assert days_to_expiry(batch_generator(date(2028, 3, 1)), today) == 470


def test_relationship():
    expiry_dates = [
        date(2026, 11, 16),
        date(2026, 10, 30),
        date(2027, 12, 3),
        date(2028, 12, 2),
        today,
    ]
    for expiry in expiry_dates:
        b = batch_generator(expiry)
        assert is_expired(b, today) == (days_to_expiry(b, today) <= 0)
