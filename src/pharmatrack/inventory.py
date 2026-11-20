from pharmatrack.models import Batch
import copy


class Inventory:
    def __init__(self):
        self.batches = list()

    def find_batch(self, batch: Batch) -> int:
        for i in range(len(self.batches)):
            if (
                (batch.batch_number == self.batches[i].batch_number)
                and (batch.medicine.name == self.batches[i].medicine.name)
                and (batch.medicine.strength == self.batches[i].medicine.strength)
            ):
                return i
        return -1

    def add_batch(self, batch: Batch):
        b = self.find_batch(batch)
        if b >= 0:
            if self.batches[b].expiry_date == batch.expiry_date:
                self.batches[b].quantity += batch.quantity
            else:
                raise ValueError(
                    f"For the {batch.medicine}, with batch number {batch.batch_number}, the stored expiry is {self.batches[b].expiry_date}, but added was {batch.expiry_date}"
                )
        else:
            self.batches.append(batch)

    def list_batches(self) -> list[Batch]:
        batches = copy.deepcopy(self.batches)
        return batches

    def search_by_name(self, name: str):
        name = name.strip().lower()
        batches_with_name = []
        for b in self.batches:
            if b.medicine.name.strip().lower().startswith(name):
                batches_with_name.append(b)
        return batches_with_name
