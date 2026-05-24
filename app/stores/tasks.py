import logging
import random

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.db.models import F

from stores.models import Stock, Store, StoreType

logger = logging.getLogger(__name__)


@shared_task
def restock_zero_items() -> None:
    """Daily 09:00 — restock items with zero quantity by random 5-25 units."""
    items = Stock.objects.filter(
        store__type=StoreType.DEALER,
        quantity=0,
    )
    count = 0
    for item in items:
        amount = random.randint(5, 25)
        item.quantity = amount
        item.save(update_fields=["quantity"])
        count += 1
    logger.info(f"Restocked {count} zero items")


@shared_task
def process_hourly_sales() -> None:
    """
    Every hour — deduct random stock items, update revenue,
    send email if out of stock.
    """
    dealers = Store.objects.filter(type=StoreType.DEALER).prefetch_related(
        "stock_items__product",
    )
    if not dealers.exists():
        logger.info("No dealers found, skipping hourly sales")
        return
    dealer = random.choice(list(dealers))
    stock_items = list(dealer.stock_items.filter(quantity__gt=0))
    if not stock_items:
        logger.info(f"No stock items in dealer {dealer.name}, skipping")
        return
    count = random.randint(1, min(5, len(stock_items)))
    selected_items = random.sample(stock_items, count)
    total_revenue = 0
    for item in selected_items:
        deduct = random.randint(1, min(10, item.quantity))
        total_revenue += deduct * item.product.price
        item.quantity = F("quantity") - deduct
        item.save(update_fields=["quantity"])
        item.refresh_from_db()
        logger.info(
            f"Deducted {deduct} of {item.product} from {dealer.name}, "
            f"remaining: {item.quantity}",
        )
        if item.quantity == 0:
            logger.info(
                f"Product {item.product} is out of stock at {dealer.name}, "
                f"sending email",
            )
            send_out_of_stock_email.delay(item.pk, dealer.pk)
    Store.objects.filter(pk=dealer.pk).update(
        daily_revenue=F("daily_revenue") + total_revenue,
    )
    logger.info(f"Added {total_revenue} to daily revenue of {dealer.name}")


@shared_task
def send_out_of_stock_email(stock_item_pk: int, dealer_pk: int) -> None:
    """Send email to HO employee when product is out of stock."""
    try:
        stock_item = Stock.objects.select_related(
            "product",
            "store__address",
        ).get(pk=stock_item_pk)
        dealer = Store.objects.select_related("address").get(pk=dealer_pk)
        ho_employee = (
            Store.objects.filter(type=StoreType.HO)
            .prefetch_related("employees")
            .first()
        )
        if not ho_employee:
            logger.error("No HO found, cannot send email")
            return
        employee = ho_employee.employees.first()
        if not employee:
            logger.error("No HO employee found, cannot send email")
            return
        send_mail(
            subject="Out of stock alert",
            message=(
                f"Dealer: {dealer.name}\n"
                f"Address: {dealer.address.country}, {dealer.address.city}, "
                f"{dealer.address.street}, {dealer.address.house}\n"
                f"Product: {stock_item.product.brand} "
                f"{stock_item.product.model}"
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[employee.email],
        )
        logger.info(f"Out of stock email sent to {employee.email}")
    except Exception as e:
        logger.error(f"Failed to send out of stock email: {e}")
        raise


@shared_task
def reset_daily_revenue() -> None:
    """Daily 21:15 — reset daily revenue for all dealers."""
    updated = Store.objects.filter(type=StoreType.DEALER).update(
        daily_revenue=0,
    )
    logger.info(f"Reset daily revenue for {updated} dealers")
