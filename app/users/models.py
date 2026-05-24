import uuid

from core.mixins import TimeStampedModel
from django.contrib.auth.models import AbstractUser
from django.db import models


class Employee(AbstractUser, TimeStampedModel):
    patronymic = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    store = models.ForeignKey(
        "stores.Store",
        on_delete=models.PROTECT,
        related_name="employees",
        null=True,
        blank=True,
    )
    api_key = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False,
    )

    class Meta:
        ordering = ("id",)

    def get_full_name(self) -> str:
        """Return full name."""
        full_name = f"{self.last_name} {self.first_name} {self.patronymic}"
        return full_name.strip()

    def __str__(self):
        return self.get_full_name()
