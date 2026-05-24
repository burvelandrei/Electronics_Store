import logging

from django.contrib import admin, messages
from django.contrib.admin import ModelAdmin, SimpleListFilter
from django.db.models import QuerySet
from django.http import HttpRequest
from django.urls import reverse
from django.utils.html import format_html

from stores.models import Address, Stock, Store
from stores.tasks import reset_selected_stores_revenue

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


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ("id", "country", "city", "street", "house")


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "type", "daily_revenue")
    actions = ("clear_daily_revenue",)

    @admin.action(description="Clear daily revenue")
    def clear_daily_revenue(
        self,
        request: HttpRequest,
        queryset: QuerySet,
    ) -> None:
        """Clear daily revenue — async if more than 5 stores selected."""
        pks = list(queryset.values_list("pk", flat=True))
        if len(pks) > 5:
            logger.info(
                f"Async clear daily revenue for {len(pks)} stores by "
                f"{request.user.username}",
            )
            reset_selected_stores_revenue.delay(pks)
            self.message_user(
                request,
                f"Daily revenue reset is being processed asynchronously for "
                f"{len(pks)} stores.",
                level=messages.SUCCESS,
            )
        else:
            queryset.update(daily_revenue=0)
            logger.info(
                f"Sync clear daily revenue for {len(pks)} stores by "
                f"{request.user.username}",
            )
            self.message_user(
                request,
                f"Daily revenue cleared for {len(pks)} stores.",
                level=messages.SUCCESS,
            )


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ("id", "store_link", "product_link", "quantity")
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
