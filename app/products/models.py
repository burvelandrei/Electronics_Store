from core.mixins import TimeStampedModel
from django.db import models


class Product(TimeStampedModel):
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=25)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    release_date = models.DateField()

    class Meta:
        ordering = ("id",)

    def __str__(self):
        return f"{self.brand} {self.model}"
