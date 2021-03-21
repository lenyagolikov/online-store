from django.urls import path
from .views import *


urlpatterns = [
    path('couriers', couriers_list),
    path('orders', orders_list),
]
