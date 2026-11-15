from dataclasses import dataclass
from datetime import date


@dataclass
class Medicine:
    name: str
    strength: str


@dataclass
class Batch:
    medicine: Medicine
    batch_number: str
    expiry_date: date
    quantity: int
