from django.db import models
from django.utils import timezone


# ---------- Employee Code Generators ----------
def _next_code(prefix: str, qs):
    last = qs.order_by("id").last()
    if not last or not last.employee_code:
        return f"{prefix}001"
    # Extract trailing integer (assumes prefix + 3+ digits)
    num = "".join(ch for ch in last.employee_code if ch.isdigit())
    n = int(num) + 1 if num else 1
    return f"{prefix}{n:03d}"


# ---------- Common / Abstract ----------
class BaseEmployee(models.Model):
    """
    Abstract base for shared fields.
    Each concrete subclass (Permanent/Contract/Temporary) has its own table & admin.
    """
    employee_code = models.CharField(max_length=20, unique=True, editable=False)
    name = models.CharField(max_length=200)
    age = models.PositiveIntegerField(blank=True, null=True)

    # Contact
    telephone = models.CharField(max_length=50, blank=True, null=True)

    # Job
    department = models.CharField(max_length=100, blank=True, null=True)
    job_position = models.CharField(max_length=100, blank=True, null=True)

    # Pay
    salary_birr = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)

    # Optional extra fields (from your form)
    nationality = models.CharField(max_length=100, blank=True, null=True)
    marital_status = models.CharField(
        max_length=20,
        choices=[("SINGLE", "Single"), ("MARRIED", "Married"), ("OTHER", "Other")],
        blank=True, null=True
    )
    address = models.CharField(max_length=255, blank=True, null=True)
    sub_city = models.CharField(max_length=100, blank=True, null=True)
    wereda = models.CharField(max_length=100, blank=True, null=True)
    tin_no = models.CharField(max_length=50, blank=True, null=True)

    working_hour = models.CharField(
        max_length=50,
        choices=[
            ("NORMAL", "Normal Hour"),
            ("PART", "Part Time"),
            ("MORNING", "Morning"),
            ("AFTERNOON", "Afternoon"),
            ("NIGHT", "Night"),
            ("SHIFTING", "Shifting"),
        ],
        blank=True, null=True
    )
    branch = models.CharField(max_length=100, blank=True, null=True)

    hire_date = models.DateField(blank=True, null=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.employee_code} • {self.name}"


# ---------- Permanent ----------
class PermanentEmployee(BaseEmployee):
    fired_date = models.DateField(blank=True, null=True)
    terminated = models.BooleanField(default=False)

    class Meta:
        ordering = ["fired_date", "name"]  # your rule: order by fired date

    def save(self, *args, **kwargs):
        if not self.employee_code:
            self.employee_code = _next_code("PERM", PermanentEmployee.objects)
        super().save(*args, **kwargs)


# ---------- Contract ----------
class ContractEmployee(BaseEmployee):
    contract_date = models.DateField(default=timezone.now)
    end_date = models.DateField(blank=True, null=True)

    class Meta:
        ordering = ["contract_date", "name"]  # your rule: order by contract date

    def save(self, *args, **kwargs):
        if not self.employee_code:
            self.employee_code = _next_code("CONT", ContractEmployee.objects)
        super().save(*args, **kwargs)


# ---------- Temporary ----------
class TemporaryEmployee(BaseEmployee):
    # No special dates; logs capture realtime activity
    class Meta:
        ordering = ["name"]  # your rule: just a clean default ordering

    def save(self, *args, **kwargs):
        if not self.employee_code:
            self.employee_code = _next_code("TEMP", TemporaryEmployee.objects)
        super().save(*args, **kwargs)


class TemporaryWorkLog(models.Model):
    LOG_TYPES = [
        ("DAILY", "Daily"),
        ("WEEKLY", "Weekly"),
        ("MONTHLY", "Monthly"),
    ]
    employee = models.ForeignKey(
        TemporaryEmployee,
        on_delete=models.CASCADE,
        related_name="logs"
    )
    log_type = models.CharField(max_length=10, choices=LOG_TYPES)
    date = models.DateField(default=timezone.now)
    recorded_value = models.DecimalField(
        max_digits=12, decimal_places=2, blank=True, null=True,
        help_text="e.g., hours or pay amount"
    )
    notes = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return f"{self.employee.employee_code} • {self.log_type} • {self.date}"
