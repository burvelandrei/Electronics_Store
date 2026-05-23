from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.views import APIView


class IsEmployee(BasePermission):
    def has_permission(self, request: Request, _: APIView) -> bool:
        """Return True if user is authenticated, active and has a store."""
        return (
            request.user.is_authenticated
            and request.user.is_active
            and request.user.store_id is not None
        )
