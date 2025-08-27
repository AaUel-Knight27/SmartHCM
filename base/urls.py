from django.urls import path
from . import views

urlpatterns = [
    # Front page default: Permanent employees
    path("", views.employee_list_permanent, name="employee_list_permanent"),

    # Explicit navigation
    path("permanent/", views.employee_list_permanent, name="employee_list_permanent"),
    path("contract/", views.employee_list_contract, name="employee_list_contract"),
    path("temporary/", views.employee_list_temporary, name="employee_list_temporary"),
    path("temporary/<int:emp_id>/logs/", views.temporary_logs, name="temporary_logs"),
]
