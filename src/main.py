from pharmatrack.models import Medicine, Batch
from datetime import date

med1 = Medicine("ZerodolP", "500mg")
med2 = Medicine("Dolo", "250mg")
med3 = Medicine("Leavociz", "100mg")

batch1 = Batch(med1, "1234", date(2026, 12, 31), 45)
batch2 = Batch(med1, "2345", date(2027, 2, 28), 67)
batch3 = Batch(med2, "45783", date(2026, 11, 14), 100)
batch4 = Batch(med3, "57689", date(2026, 12, 15), 4)

print(batch1)
print(batch2)
print(batch3)
print(batch4)
