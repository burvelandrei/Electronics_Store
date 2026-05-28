import logging

from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.request import Request

from users.models import Employee

logger = logging.getLogger(__name__)


class APIKeyAuthentication(BaseAuthentication):
    """Authenticate user by API key."""

    def authenticate(self, request: Request) -> tuple[Employee, None] | None:
        """Return employee if API key is valid."""
        api_key = request.headers.get("X-API-Key")
        if not api_key:
            return None
        try:
            employee = Employee.objects.get(api_key=api_key)
        except Employee.DoesNotExist as e:
            logger.warning(f"Invalid API key: {api_key}")
            raise AuthenticationFailed("Invalid API key.") from e
        if not employee.is_active:
            logger.warning(
                f"Inactive employee tried to authenticate with API key: "
                f"{api_key}",
            )
            raise AuthenticationFailed("Employee is inactive.")
        logger.debug(f"Authenticated employee {employee.username} via API key")
        return employee, None
