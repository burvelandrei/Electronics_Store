import logging

from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from stores.models import Store, StoreType
from stores.serializers import StoreSerializer

logger = logging.getLogger(__name__)


class StoreListCreateView(APIView):
    """List all stores or create a new one."""

    def get(self, request: Request) -> Response:
        """Return list of all stores, optionally filtered by city."""
        queryset = Store.objects.select_related("address").prefetch_related(
            "employees",
            "stock_items__product",
        )
        city = request.query_params.get("city")
        if city:
            logger.debug(f"Filtering stores by city: {city}")
            queryset = queryset.filter(address__city__icontains=city)
        serializer = StoreSerializer(queryset, many=True)
        logger.debug(f"Returning {len(serializer.data)} stores")
        return Response(serializer.data)

    def post(self, request: Request) -> Response:
        """Create a new store."""
        serializer = StoreSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        store = serializer.save()
        logger.info(f"Store created: {store.name} (type={store.type})")
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class StoreDetailView(APIView):
    """Retrieve, update or delete a store."""

    def get_object(self, pk: int) -> Store:
        """Return store by pk or 404."""
        return get_object_or_404(
            Store.objects.select_related("address").prefetch_related(
                "employees",
                "stock_items__product",
            ),
            pk=pk,
        )

    def get(self, _: Request, pk: int) -> Response:
        """Return store by pk."""
        serializer = StoreSerializer(self.get_object(pk))
        return Response(serializer.data)

    def patch(self, request: Request, pk: int) -> Response:
        """Partial update store."""
        store = self.get_object(pk)
        serializer = StoreSerializer(store, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        logger.info(f"Store updated: {store.name} (id={store.pk})")
        return Response(serializer.data)

    def delete(self, request: Request, pk: int) -> Response:
        """Delete store."""
        store = self.get_object(pk)
        if store.type == StoreType.HO:
            logger.warning(
                f"Attempt to delete HO (id={store.pk}) by "
                f"{request.user.username}",
            )
            return Response(
                {"detail": "Cannot delete HO."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        logger.info(f"Store deleted: {store.name} (id={store.pk})")
        store.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DealerAboveAverageView(APIView):
    """Return dealers with daily revenue above average."""

    def get(self, _: Request) -> Response:
        """
        Return dealers with revenue strictly above average among all dealers.
        """
        avg = (
            Store.objects.filter(type=StoreType.DEALER).aggregate(
                avg=Avg("daily_revenue"),
            )["avg"]
            or 0
        )
        logger.debug(f"Average daily revenue among dealers: {avg}")
        queryset = (
            Store.objects.filter(
                type=StoreType.DEALER,
                daily_revenue__gt=avg,
            )
            .select_related("address")
            .prefetch_related("employees", "stock_items__product")
        )
        serializer = StoreSerializer(queryset, many=True)
        return Response(serializer.data)


class StoreByProductView(APIView):
    """Return stores that have a specific product in stock."""

    def get(self, request: Request) -> Response:
        """Return stores filtered by product id."""
        product_id = request.query_params.get("product_id")
        if not product_id:
            logger.warning(
                f"product_id not provided by {request.user.username}",
            )
            return Response(
                {"detail": "product_id is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        logger.debug(f"Filtering stores by product_id: {product_id}")
        queryset = (
            Store.objects.filter(
                stock_items__product_id=product_id,
                stock_items__quantity__gt=0,
            )
            .select_related("address")
            .prefetch_related("employees", "stock_items__product")
        )
        serializer = StoreSerializer(queryset, many=True)
        return Response(serializer.data)
