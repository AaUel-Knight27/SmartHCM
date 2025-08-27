from django.contrib import admin
from .models import (
    PermanentEmployee,
    ContractEmployee,
    TemporaryEmployee,
    TemporaryWorkLog,
)


# ---- Inlines for Temporary logs ----
class TemporaryWorkLogInline(admin.TabularInline):
    model = TemporaryWorkLog
    extra = 1
    fields = ("date", "log_type", "recorded_value", "notes")
    show_change_link = True


# ---- Shared Admin mixin for list columns ----
class _BaseEmployeeAdmin(admin.ModelAdmin):
    readonly_fields = ("employee_code",)
    search_fields = ("employee_code", "name", "job_position", "department", "telephone")
    list_display = (
        "employee_code",
        "name",
        "job_position",
        "department",
        "salary_birr",
        "telephone",
        "hire_date",
    )
    list_per_page = 25


@admin.register(PermanentEmployee)
class PermanentEmployeeAdmin(_BaseEmployeeAdmin):
    list_display = _BaseEmployeeAdmin.list_display + ("fired_date", "terminated")
    list_filter = ("department", "terminated", "branch")
    fieldsets = (
        ("Identity", {
            "fields": ("employee_code", "name", "age", "telephone")
        }),
        ("Job", {
            "fields": ("department", "job_position", "salary_birr", "working_hour", "branch")
        }),
        ("Dates & Status", {
            "fields": ("hire_date", "fired_date", "terminated")
        }),
        ("Extra", {
            "fields": ("nationality", "marital_status", "address", "sub_city", "wereda", "tin_no")
        }),
    )


@admin.register(ContractEmployee)
class ContractEmployeeAdmin(_BaseEmployeeAdmin):
    list_display = _BaseEmployeeAdmin.list_display + ("contract_date", "end_date")
    list_filter = ("department", "branch")
    fieldsets = (
        ("Identity", {
            "fields": ("employee_code", "name", "age", "telephone")
        }),
        ("Job", {
            "fields": ("department", "job_position", "salary_birr", "working_hour", "branch")
        }),
        ("Contract", {
            "fields": ("contract_date", "end_date", "hire_date")
        }),
        ("Extra", {
            "fields": ("nationality", "marital_status", "address", "sub_city", "wereda", "tin_no")
        }),
    )


@admin.register(TemporaryEmployee)
class TemporaryEmployeeAdmin(_BaseEmployeeAdmin):
    inlines = [TemporaryWorkLogInline]
    list_filter = ("department", "branch")
    fieldsets = (
        ("Identity", {
            "fields": ("employee_code", "name", "age", "telephone")
        }),
        ("Job", {
            "fields": ("department", "job_position", "salary_birr", "working_hour", "branch")
        }),
        ("Dates", {
            "fields": ("hire_date",)
        }),
        ("Extra", {
            "fields": ("nationality", "marital_status", "address", "sub_city", "wereda", "tin_no")
        }),
    )


@admin.register(TemporaryWorkLog)
class TemporaryWorkLogAdmin(admin.ModelAdmin):
    list_display = ("employee", "log_type", "date", "recorded_value")
    list_filter = ("log_type", "date")
    search_fields = ("employee__employee_code", "employee__name")
    autocomplete_fields = ("employee",)
