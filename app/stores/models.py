from core.mixins import TimeStampedModel
from django.db import models
from django.db.models import Q, UniqueConstraint


class StoreType(models.TextChoices):
    HO = "HO"
    DEALER = "DEALER"


class Address(TimeStampedModel):
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    house = models.CharField(max_length=20)

    class Meta:
        ordering = ("id",)

    def __str__(self):
        return f"{self.country}, {self.city}, {self.street}, {self.house}"


class Store(TimeStampedModel):
    type = models.CharField(max_length=20, choices=StoreType.choices)
    name = models.CharField(max_length=50)
    address = models.OneToOneField(
        Address,
        on_delete=models.CASCADE,
        related_name="store",
    )
    daily_revenue = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
    )

    class Meta:
        ordering = ("id",)
        constraints = (
            UniqueConstraint(
                fields=["type"],
                condition=Q(type="HO"),
                name="unique_hq",
            ),
        )

    def __str__(self):
        return self.name


class Stock(TimeStampedModel):
    store = models.ForeignKey(
        Store,
        on_delete=models.CASCADE,
        related_name="stock_items",
    )
    product = models.ForeignKey(
        "products.Product",
        on_delete=models.PROTECT,
        related_name="stock_items",
    )
    quantity = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ("id",)
        unique_together = (("store", "product"),)

    def __str__(self):
        return f"{self.store} — {self.product}"
