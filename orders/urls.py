from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet, OrderItemViewSet

router = DefaultRouter()
router.register(r'orders', OrderViewSet)
router.register(r'orders/(?P<order_pk>\d+)/order-items', OrderItemViewSet, basename='order-items')  # Nested route for order items

urlpatterns = router.urls 