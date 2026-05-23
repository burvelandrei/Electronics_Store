from rest_framework.permissions import BasePermission
from rest_framework.request import Request


class IsEmployee(BasePermission):
    def has_permission(self, request: Request, _: object) -> bool:
        """Return True if user is authenticated, active and has a store."""
        return (
            request.user.is_authenticated
            and request.user.is_active
            and request.user.store_id is not None
        )
