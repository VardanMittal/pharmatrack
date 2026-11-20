from pharmatrack.inventory import Inventory
from pharmatrack.models import Batch, Medicine
from datetime import date


def batch_generator(batch_num, quantity) -> Batch:
    med = Medicine("ZerodolP", "500mg")
    return Batch(med, batch_num, date(2026, 12, 18), quantity)


inventory = Inventory()

b = batch_generator("123456", 90)
batch = batch_generator("123456", 45)
inventory.add_batch(batch)
inventory.add_batch(b)
print(inventory.list_batches())
