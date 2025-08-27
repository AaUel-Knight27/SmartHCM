from django.shortcuts import render, get_object_or_404
from .models import (
    PermanentEmployee,
    ContractEmployee,
    TemporaryEmployee,
    TemporaryWorkLog,
)

# NOTE: You said the front page shows PERMANENT by default.
# These views return context; your templates will render them.


def employee_list_permanent(request):
    employees = PermanentEmployee.objects.all()  # ordered by fired_date by Meta.ordering
    return render(request, "labors/employee_list.html", {
        "active_tab": "PERMANENT",
        "employees": employees,
    })


def employee_list_contract(request):
    employees = ContractEmployee.objects.all()  # ordered by contract_date by Meta.ordering
    return render(request, "labors/employee_list.html", {
        "active_tab": "CONTRACT",
        "employees": employees,
    })


def employee_list_temporary(request):
    employees = TemporaryEmployee.objects.all()  # ordered by name
    return render(request, "labors/employee_list.html", {
        "active_tab": "TEMPORARY",
        "employees": employees,
    })


def temporary_logs(request, emp_id: int):
    employee = get_object_or_404(TemporaryEmployee, id=emp_id)
    logs = employee.logs.all().order_by("-date")
    return render(request, "labors/temporary_logs.html", {
        "employee": employee,
        "logs": logs,
    })
