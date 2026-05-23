from rest_framework import serializers

from users.models import Employee


class EmployeeSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = ("id", "full_name", "phone", "email")

    def get_full_name(self, obj: Employee) -> str:
        """Return full name of employee."""
        return obj.get_full_name()
