import logging

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from products.models import Product
from products.serializers import ProductSerializer

logger = logging.getLogger(__name__)


class ProductListCreateView(APIView):
    """List all products or create a new one."""

    def get(self, _: Request) -> Response:
        """Return list of all products."""
        serializer = ProductSerializer(Product.objects.all(), many=True)
        logger.debug(f"Returning {len(serializer.data)} products")
        return Response(serializer.data)

    def post(self, request: Request) -> Response:
        """Create a new product."""
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = serializer.save()
        logger.info(f"Product created: {product.brand} {product.model}")
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProductDetailView(APIView):
    """Retrieve, update or delete a product."""

    def get_object(self, pk: int) -> Product:
        """Return product by pk or 404."""
        return get_object_or_404(Product, pk=pk)

    def get(self, _: Request, pk: int) -> Response:
        """Return product by pk."""
        serializer = ProductSerializer(self.get_object(pk))
        return Response(serializer.data)

    def patch(self, request: Request, pk: int) -> Response:
        """Partial update product."""
        product = self.get_object(pk)
        serializer = ProductSerializer(
            product,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        logger.info(
            f"Product updated: {product.brand} {product.model} "
            f"(id={product.pk})",
        )
        return Response(serializer.data)

    def delete(self, _: Request, pk: int) -> Response:
        """Delete product."""
        product = self.get_object(pk)
        logger.info(
            f"Product deleted: {product.brand} {product.model} "
            f"(id={product.pk})",
        )
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
