from enum import Enum

class MedicalRecordStatus(Enum):
    NEW_ENTRY = "new_entry"
    PENDING_APPROVAL = "pending_approval"
    DENIED = "denied"
    PENDING_PAYMENT = "pending_payment"
    PENDING_RECORDS = "pending_records"
    COMPLETED = "completed"

    @classmethod
    def choices(cls):
        return [(status.value, status.name.replace("_", " ").title()) for status in cls]