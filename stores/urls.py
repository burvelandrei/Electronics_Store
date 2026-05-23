from django.urls import path

from stores.views import (
    DealerAboveAverageView,
    StoreByProductView,
    StoreDetailView,
    StoreListCreateView,
)

urlpatterns = [
    path("", StoreListCreateView.as_view(), name="store-list-create"),
    path("<int:pk>/", StoreDetailView.as_view(), name="store-detail"),
    path(
        "dealers/above-average/",
        DealerAboveAverageView.as_view(),
        name="dealer-above-average",
    ),
    path("by-product/", StoreByProductView.as_view(), name="store-by-product"),
]
