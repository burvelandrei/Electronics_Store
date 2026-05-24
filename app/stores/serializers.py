from rest_framework import serializers
from users.serializers import EmployeeSerializer

from stores.models import Address, Stock, Store, StoreType


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ("country", "city", "street", "house")


class StockSerializer(serializers.ModelSerializer):
    product = serializers.StringRelatedField()

    class Meta:
        model = Stock
        fields = ("product", "quantity")


class StoreSerializer(serializers.ModelSerializer):
    address = AddressSerializer()
    employees = EmployeeSerializer(many=True, read_only=True)
    stock_items = StockSerializer(many=True, read_only=True)

    class Meta:
        model = Store
        fields = (
            "id",
            "type",
            "name",
            "address",
            "daily_revenue",
            "employees",
            "stock_items",
        )
        read_only_fields = ("daily_revenue",)

    def validate(self, attrs: dict) -> dict:
        """Ensure only one HO can exist."""
        if attrs.get("type") == StoreType.HO:
            qs = Store.objects.filter(type=StoreType.HO)
            if self.instance:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise serializers.ValidationError("HO already exists.")
        return attrs

    def validate_name(self, value: str) -> str:
        """Validate store name length."""
        if len(value) > 50:
            raise serializers.ValidationError(
                "Name must be 50 characters or less.",
            )
        return value

    def create(self, validated_data: dict) -> Store:
        """Create store with nested address."""
        address_data = validated_data.pop("address")
        address = Address.objects.create(**address_data)
        return Store.objects.create(address=address, **validated_data)

    def update(self, instance: Store, validated_data: dict) -> Store:
        """Update store with nested address."""
        address_data = validated_data.pop("address", None)
        if address_data:
            for attr, value in address_data.items():
                setattr(instance.address, attr, value)
            instance.address.save()
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
