from django.urls import path

from .views import couriers_create, orders_create


urlpatterns = [
    path('couriers', couriers_create),
    path('orders', orders_create),
]
