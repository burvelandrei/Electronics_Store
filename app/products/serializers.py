from datetime import date

from django.utils import timezone
from rest_framework import serializers

from products.models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ("id", "brand", "model", "price", "date_release")

    def validate_brand(self, value: str) -> str:
        """Validate brand length."""
        if len(value) > 50:
            raise serializers.ValidationError(
                "Brand must be 50 characters or less.",
            )
        return value

    def validate_model(self, value: str) -> str:
        """Validate model length."""
        if len(value) > 25:
            raise serializers.ValidationError(
                "Model must be 25 characters or less.",
            )
        return value

    def validate_date_release(self, value: date) -> date:
        """Validate release date is not in the future."""
        if value > timezone.now().date():
            raise serializers.ValidationError(
                "Release date cannot be in the future.",
            )
        return value
