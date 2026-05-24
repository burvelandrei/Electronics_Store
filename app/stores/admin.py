import logging

from django.contrib import admin
from django.contrib.admin import ModelAdmin, SimpleListFilter
from django.db.models import QuerySet
from django.http import HttpRequest
from django.urls import reverse
from django.utils.html import format_html

from stores.models import Stock, Store

logger = logging.getLogger(__name__)


class StockAvailabilityFilter(SimpleListFilter):
    title = "Availability"
    parameter_name = "availability"

    def lookups(self, _: HttpRequest, __: ModelAdmin) -> list:
        """Return filter options."""
        return [
            ("in_stock", "In stock"),
            ("out_of_stock", "Out of stock"),
        ]

    def queryset(self, _: HttpRequest, queryset: QuerySet) -> QuerySet:
        """Filter queryset by availability."""
        if self.value() == "in_stock":
            return queryset.filter(quantity__gt=0)
        if self.value() == "out_of_stock":
            return queryset.filter(quantity=0)
        return queryset


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ("name", "type", "daily_revenue")
    actions = ("clear_daily_revenue",)

    def clear_daily_revenue(
        self,
        request: HttpRequest,
        queryset: QuerySet,
    ) -> None:
        """Clear daily revenue for selected stores."""
        count = queryset.count()
        queryset.update(daily_revenue=0)
        logger.info(
            f"Daily revenue cleared for {count} stores by "
            f"{request.user.username}",
        )


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ("store_link", "product_link", "quantity")
    list_filter = (StockAvailabilityFilter, "store")

    @admin.display(description="Dealer")
    def store_link(self, obj: Stock) -> str:
        """Return link to dealer admin page."""
        url = reverse("admin:stores_store_change", args=[obj.store.pk])
        return format_html('<a href="{}">{}</a>', url, obj.store)

    @admin.display(description="Product")
    def product_link(self, obj: Stock) -> str:
        """Return link to product admin page."""
        url = reverse("admin:products_product_change", args=[obj.product.pk])
        return format_html('<a href="{}">{}</a>', url, obj.product)
