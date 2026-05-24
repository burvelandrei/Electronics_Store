import logging

from rest_framework.permissions import BasePermission
from rest_framework.request import Request

logger = logging.getLogger(__name__)


class IsEmployee(BasePermission):
    def has_permission(self, request: Request, _: object) -> bool:
        """Return True if user is authenticated, active and has a store."""
        if not request.user.is_authenticated:
            logger.warning("Unauthenticated request")
            return False
        if not request.user.is_active:
            logger.warning(
                f"Inactive user {request.user.username} tried to access API",
            )
            return False
        if request.user.store_id is None:
            logger.warning(
                f"User {request.user.username} has no store assigned",
            )
            return False
        return True
