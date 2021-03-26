from django.urls import path

from .views import *


urlpatterns = [
    path('couriers', couriers_create),
    path('couriers/<str:id>', courier_detail),
    path('orders', orders_create),
    path('orders/assign', orders_assign),
    path('orders/complete', orders_complete),
]
