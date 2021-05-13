from django.urls import path
from delivery.api import views


urlpatterns = [
    path('couriers', views.couriers_create),
    path('couriers/<str:id>', views.courier_detail),
    path('orders', views.orders_create),
    path('orders/assign', views.orders_assign),
    path('orders/complete', views.orders_complete),
]
