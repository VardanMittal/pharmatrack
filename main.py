from datetime import date

from pharmatrack.inventory import Inventory
from pharmatrack.models import Batch, Medicine

med1 = Medicine("ZerodolP", "500mg")
med2 = Medicine("Dolo", "250mg")
med3 = Medicine("Leavociz", "100mg")

batch1 = Batch(med1, "1234", date(2026, 11, 17), 45)
batch2 = Batch(med1, "2345", date(2027, 2, 28), 67)
batch3 = Batch(med2, "45783", date(2026, 11, 14), 100)
batch4 = Batch(med3, "57689", date(2026, 12, 16), 4)

today = date(2026, 11, 16)

# print(is_expired(batch1, today))
# print(is_expired(batch2, today))
# print(is_expired(batch3, today))
# print(is_expired(batch4, today))


# print(days_to_expiry(batch1, today))
# print(days_to_expiry(batch2, today))
# print(days_to_expiry(batch3, today))
# print(days_to_expiry(batch4, today))


inventory = Inventory()
inventory.add_batch(batch1)
inventory.add_batch(batch2)

batches = inventory.expiring_within(30, date(2026, 12, 18))

print(batches)
