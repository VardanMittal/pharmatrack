from datetime import date

import pytest

from pharmatrack.inventory import Inventory
from pharmatrack.models import Batch, Medicine


def batch_generator(name, batch_num, expiry, quantity, strength) -> Batch:
    med = Medicine(name, strength)
    return Batch(med, batch_num, expiry, quantity)


def inventory_generator(batch: Batch):
    inventory = Inventory()
    inventory.add_batch(batch)
    return inventory


def test_batch_addition_in_inventory():
    batch = batch_generator("ZerodolP", "123456", date(2026, 12, 18), 45, "500mg")
    inventory = inventory_generator(batch)
    assert len(inventory.list_batches()) == 1
    assert inventory.list_batches()[0].quantity == 45


def test_finding_the_batch_for_case():
    batch = batch_generator("ZerodolP", "123456", date(2026, 12, 18), 45, "500mg")
    inventory = inventory_generator(batch)
    assert inventory.search_by_name("zerodolp") == inventory.list_batches()


def test_finding_the_batch_for_Null():
    batch = batch_generator("ZerodolP", "123456", date(2026, 12, 18), 45, "500mg")
    inventory = inventory_generator(batch)
    assert inventory.search_by_name("Dolo") == []


def test_for_duplicate_batches():
    b = batch_generator("ZerodolP", "123456", date(2026, 12, 18), 90, "500mg")
    batch = batch_generator("ZerodolP", "123456", date(2026, 12, 18), 45, "500mg")
    inventory = inventory_generator(batch)
    inventory.add_batch(b)
    assert inventory.list_batches()[0].quantity == 135


def test_two_different_batches_correct_quantity():
    A = batch_generator("ZerodolP", "A", date(2026, 12, 18), 45, "500mg")
    B = batch_generator("ZerodolP", "B", date(2026, 12, 18), 56, "500mg")
    inventory = inventory_generator(A)
    inventory.add_batch(B)
    assert len(inventory.list_batches()) == 2

    for i in inventory.list_batches():
        if i.batch_number == "A":
            assert i.quantity == 45
        else:
            assert i.quantity == 56


def test_same_batch_number_different_medicines():
    A = batch_generator("ZerodolP", "A", date(2026, 12, 18), 46, "500mg")
    B = batch_generator("Dolo", "A", date(2026, 12, 18), 5, "500mg")

    inventory = inventory_generator(A)
    inventory.add_batch(B)

    assert len(inventory.list_batches()) == 2


def test_same_batch_different_expiry():
    A = batch_generator("ZerodolP", "A", date(2026, 12, 18), 45, "500mg")
    B = batch_generator("ZerodolP", "A", date(2026, 12, 15), 56, "500mg")
    inventory = inventory_generator(A)
    with pytest.raises(ValueError) as execinfo:
        inventory.add_batch(B)

    assert "2026-12-18" in str(execinfo.value)
    assert "2026-12-15" in str(execinfo.value)
    assert str(B.medicine.name) in str(execinfo.value)
    assert str(B.batch_number) in str(execinfo.value)


def test_search_for_zero():
    A = batch_generator("ZerodolP", "A", date(2026, 12, 18), 45, "500mg")
    inventory = inventory_generator(A)
    assert inventory.search_by_name("zero") == [A]


def test_search_for_Dol():
    A = batch_generator("ZerodolP", "A", date(2026, 12, 18), 45, "500mg")
    inventory = inventory_generator(A)
    assert inventory.search_by_name("dol") == []


def test_different_strengths_same_batch_number():
    A = batch_generator("ZerodolP", "A", date(2026, 12, 18), 45, "500mg")
    B = batch_generator("ZerodolP", "A", date(2026, 12, 18), 56, "250mg")
    inventory = inventory_generator(A)
    inventory.add_batch(B)
    assert len(inventory.list_batches()) == 2


def test_copy_list_batches():
    A = batch_generator("ZerodolP", "A", date(2026, 12, 18), 46, "500mg")
    B = batch_generator("Dolo", "A", date(2026, 12, 18), 5, "500mg")

    inventory = inventory_generator(A)
    inventory.add_batch(B)

    batches = inventory.list_batches()

    batches.clear()

    assert len(inventory.list_batches()) == 2


def test_for_quantity_mutation():
    A = batch_generator("ZerodolP", "A", date(2026, 12, 18), 46, "500mg")
    B = batch_generator("Dolo", "A", date(2026, 12, 18), 5, "500mg")

    inventory = inventory_generator(A)
    inventory.add_batch(B)

    batches = inventory.list_batches()

    batches[0].quantity = 69
    assert inventory.list_batches()[0].quantity == 46


# Testing expiring within


def test_boundary_case_for_expiring_within():
    A = batch_generator("ZerodolP", "A", date(2026, 12, 21), 46, "500mg")
    B = batch_generator("Dolo", "A", date(2026, 12, 13), 5, "500mg")

    inventory = inventory_generator(A)
    inventory.add_batch(B)
    assert inventory.expiring_within(30, date(2026, 11, 21)) == [B, A]


def test_expiring_today():
    B = batch_generator("Dolo", "A", date(2026, 12, 18), 5, "500mg")
    inventory = inventory_generator(B)

    assert inventory.expiring_within(30, date(2026, 12, 18)) == []


def test_negative_days_check():
    B = batch_generator("Dolo", "A", date(2026, 12, 18), 5, "500mg")
    inventory = inventory_generator(B)
    with pytest.raises(ValueError, match="The days can not be negative"):
        inventory.expiring_within(-5, date(2026, 12, 23))


def test_sorted_results_unordered_batches():
    A = batch_generator("ZerodolP", "A", date(2026, 11, 30), 46, "500mg")
    B = batch_generator("Dolo", "B", date(2026, 12, 14), 55, "500mg")
    C = batch_generator("Forxnorm", "C", date(2026, 12, 1), 57, "625mg")
    inventory = inventory_generator(A)
    inventory.add_batch(B)
    inventory.add_batch(C)

    assert inventory.expiring_within(45, date(2026, 11, 21)) == [A, C, B]


def test_quantity_zero_should_be_ignored():
    D = batch_generator("Perinorm", "D", date(2026, 11, 22), 0, "50mg")
    inventory = inventory_generator(D)

    assert inventory.expiring_within(30, date(2026, 11, 18)) == []


def test_two_expiries_two_batches():
    A = batch_generator("ZerodolP", "A", date(2026, 12, 1), 46, "500mg")
    B = batch_generator("Dolo", "B", date(2026, 11, 21), 55, "500mg")
    inventory = inventory_generator(A)
    inventory.add_batch(B)

    assert inventory.expiring_within(30, date(2026, 11, 21)) == [A]


def test_same_expiry_different_names():
    A = batch_generator("ZerodolP", "A", date(2026, 12, 1), 46, "500mg")
    B = batch_generator("Dolo", "B", date(2026, 12, 1), 55, "500mg")
    inventory = inventory_generator(A)
    inventory.add_batch(B)

    assert inventory.expiring_within(30, date(2026, 11, 21)) == [B, A]
