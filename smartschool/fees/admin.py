from django.contrib import admin
from . import models


@admin.register(models.AcademicYear)
class AcademicYearAdmin(admin.ModelAdmin):
    list_display = ("name", "start_date", "end_date", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name",)


@admin.register(models.Term)
class TermAdmin(admin.ModelAdmin):
    list_display = ("name", "academic_year", "start_date", "end_date", "is_active")
    list_filter = ("academic_year", "is_active")
    search_fields = ("name",)


@admin.register(models.ClassRoom)
class ClassRoomAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(models.Guardian)
class GuardianAdmin(admin.ModelAdmin):
    list_display = ("full_name", "phone", "email")
    search_fields = ("full_name", "phone", "email")


@admin.register(models.Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("admission_number", "first_name", "last_name", "class_room", "is_active")
    list_filter = ("class_room", "is_active")
    search_fields = ("admission_number", "first_name", "last_name")
    autocomplete_fields = ("guardians",)


@admin.register(models.FeeType)
class FeeTypeAdmin(admin.ModelAdmin):
    list_display = ("code", "name")
    search_fields = ("code", "name")


@admin.register(models.FeeStructure)
class FeeStructureAdmin(admin.ModelAdmin):
    list_display = ("academic_year", "class_room", "fee_type", "amount")
    list_filter = ("academic_year", "class_room", "fee_type")
    search_fields = ("fee_type__name", "class_room__name", "academic_year__name")


@admin.register(models.Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ("reference", "student", "term", "due_date", "total_amount", "amount_paid", "is_paid")
    list_filter = ("term", "is_paid")
    search_fields = ("reference", "student__admission_number", "student__first_name", "student__last_name")


@admin.register(models.Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("invoice", "amount", "received_on", "received_by", "method")
    list_filter = ("method", "received_on")
    search_fields = ("invoice__reference",)
