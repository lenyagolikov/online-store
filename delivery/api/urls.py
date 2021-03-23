from django.urls import path

from .views import couriers_create, orders_create, courier_update, orders_assign


urlpatterns = [
    path('couriers', couriers_create),
    path('couriers/<str:id>', courier_update),
    path('orders/assign', orders_assign),
    path('orders', orders_create),
]
