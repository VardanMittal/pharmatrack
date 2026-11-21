from datetime import date

import pytest

from pharmatrack.parsing import parse_expiry


def test_for_31_days():
    assert parse_expiry("12/2026") == date(2026, 12, 31)


def test_for_leap_year():
    assert parse_expiry("02/2028") == date(2028, 2, 29)


def test_for_30_days():
    assert parse_expiry("04/2027") == date(2027, 4, 30)


def test_strip_testing():
    assert parse_expiry("  12/2026 ") == date(2026, 12, 31)


def test_for_month_13():
    with pytest.raises(ValueError) as execinfo:
        parse_expiry("13/2025")

    assert "13" in str(execinfo.value)


def test_for_month_0():
    with pytest.raises(ValueError) as execinfo:
        parse_expiry("0/2025")

    assert "The month cannot be 0" in str(execinfo.value)


def test_for_format():
    with pytest.raises(ValueError) as execinfo:
        parse_expiry("13-2025")
    assert "MM/YYYY" in str(execinfo.value)


def test_for_non_leap_year():
    assert parse_expiry("02/2027") == date(2027, 2, 28)


def test_for_wrong_formatting_YY():
    with pytest.raises(ValueError) as execinfo:
        parse_expiry("12/26")
    assert "The year cannot be 26" in str(execinfo.value)


def test_empty_text():
    with pytest.raises(ValueError, match="The text should be in format of MM/YYYY"):
        parse_expiry("")


def test_for_letters():
    with pytest.raises(ValueError, match="Month and year must be numeric"):
        parse_expiry("ab/2026")


def test_for_unstructured_date():
    with pytest.raises(ValueError, match="The text should be in format of MM/YYYY"):
        parse_expiry("05/2027/05")
