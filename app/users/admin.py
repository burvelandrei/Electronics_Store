from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import Employee


@admin.register(Employee)
class EmployeeAdmin(UserAdmin):
    list_display = ("username", "email", "first_name", "last_name", "store")
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            "Personal info",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "patronymic",
                    "email",
                    "phone",
                    "store",
                ),
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                    "api_key",
                ),
            },
        ),
    )
