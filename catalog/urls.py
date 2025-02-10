# catalog/urls.py.

from django.urls import path
from catalog.apps import CatalogConfig
from catalog.views import (
    ProductDetailView,
    ProductListView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView,
    CategoryCreateView,
)


app_name = CatalogConfig.name

urlpatterns = [
    path("", ProductListView.as_view(), name="product_list"),
    path("product_detail/<int:pk>", ProductDetailView.as_view(), name="product_detail"),
    path("product_form/", ProductCreateView.as_view(), name="product_create"),
    path("product_form/<int:pk>/", ProductUpdateView.as_view(), name="product_update"),
    path("product_confirm_delete/<int:pk>/", ProductDeleteView.as_view(), name="product_delete"),
    path("category_form/", CategoryCreateView.as_view(), name="category_create"),
]
