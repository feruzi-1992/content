from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class AcademicYear(TimeStampedModel):
    name = models.CharField(max_length=32, unique=True)  # e.g., 2024-2025
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:  # pragma: no cover
        return self.name


class Term(TimeStampedModel):
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, related_name='terms')
    name = models.CharField(max_length=32)  # e.g., Term 1
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('academic_year', 'name')

    def __str__(self) -> str:  # pragma: no cover
        return f"{self.academic_year} - {self.name}"


class ClassRoom(TimeStampedModel):
    name = models.CharField(max_length=64, unique=True)  # e.g., Grade 6 Blue

    def __str__(self) -> str:  # pragma: no cover
        return self.name


class Guardian(TimeStampedModel):
    full_name = models.CharField(max_length=128)
    phone = models.CharField(max_length=32, blank=True)
    email = models.EmailField(blank=True)

    def __str__(self) -> str:  # pragma: no cover
        return self.full_name


class Student(TimeStampedModel):
    admission_number = models.CharField(max_length=32, unique=True)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    class_room = models.ForeignKey(ClassRoom, on_delete=models.PROTECT, related_name='students')
    guardians = models.ManyToManyField(Guardian, related_name='students', blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:  # pragma: no cover
        return f"{self.admission_number} - {self.first_name} {self.last_name}"


class FeeType(TimeStampedModel):
    code = models.CharField(max_length=32, unique=True)  # e.g., TUITION, LUNCH, TRANSPORT
    name = models.CharField(max_length=64)

    def __str__(self) -> str:  # pragma: no cover
        return self.name


class FeeStructure(TimeStampedModel):
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, related_name='fee_structures')
    class_room = models.ForeignKey(ClassRoom, on_delete=models.CASCADE, related_name='fee_structures')
    fee_type = models.ForeignKey(FeeType, on_delete=models.CASCADE, related_name='fee_structures')
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ('academic_year', 'class_room', 'fee_type')

    def __str__(self) -> str:  # pragma: no cover
        return f"{self.academic_year} {self.class_room} {self.fee_type}: {self.amount}"


class Invoice(TimeStampedModel):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='invoices')
    term = models.ForeignKey(Term, on_delete=models.PROTECT, related_name='invoices')
    due_date = models.DateField()
    reference = models.CharField(max_length=64, unique=True)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    amount_paid = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    is_paid = models.BooleanField(default=False)

    class Meta:
        unique_together = ('student', 'term', 'reference')
        ordering = ['-created_at']

    def __str__(self) -> str:  # pragma: no cover
        return f"INV-{self.reference}"


class Payment(TimeStampedModel):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    received_on = models.DateField()
    received_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    method = models.CharField(max_length=32, choices=[
        ('CASH', 'Cash'),
        ('CARD', 'Card'),
        ('BANK', 'Bank Transfer'),
        ('MOBILE', 'Mobile Money'),
    ], default='CASH')
    notes = models.TextField(blank=True)

    def __str__(self) -> str:  # pragma: no cover
        return f"PAY-{self.id} {self.amount}"
