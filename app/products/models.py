from django.db import models


class Product(models.Model):
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=25)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date_release = models.DateField()

    def __str__(self):
        return f"{self.brand} {self.model}"
