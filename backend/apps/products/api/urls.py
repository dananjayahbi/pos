"""
Category URL routing for the products API.

Uses DRF DefaultRouter to auto-generate RESTful endpoints.

Endpoints:
    GET    /                  → category-list
    POST   /                  → category-list
    GET    /{id}/             → category-detail
    PUT    /{id}/             → category-detail
    PATCH  /{id}/             → category-detail
    DELETE /{id}/             → category-detail
    GET    /tree/             → category-tree
    POST   /{id}/move/        → category-move
"""

from rest_framework.routers import DefaultRouter

from apps.products.api.views import (
    BrandViewSet,
    CategoryViewSet,
    ProductViewSet,
    TaxClassViewSet,
)

app_name = "products"

router = DefaultRouter()
router.register(r"categories", CategoryViewSet, basename="category")
router.register(r"brands", BrandViewSet, basename="brand")
router.register(r"tax-classes", TaxClassViewSet, basename="taxclass")
router.register(r"products", ProductViewSet, basename="product")

urlpatterns = router.urls
