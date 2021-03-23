from django.urls import path

from .views import couriers_create, orders_create, courier_update


urlpatterns = [
    path('couriers', couriers_create),
    path('couriers/<str:id>', courier_update),
    path('orders', orders_create),
]
