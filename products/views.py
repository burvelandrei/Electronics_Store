from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from products.models import Product
from products.serializers import ProductSerializer


class ProductListCreateView(APIView):
    """List all products or create a new one."""

    def get(self, _: Request) -> Response:
        """Return list of all products."""
        serializer = ProductSerializer(Product.objects.all(), many=True)
        return Response(serializer.data)

    def post(self, request: Request) -> Response:
        """Create a new product."""
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
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
        serializer = ProductSerializer(
            self.get_object(pk),
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, _: Request, pk: int) -> Response:
        """Delete product."""
        self.get_object(pk).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
