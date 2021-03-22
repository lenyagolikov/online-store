from django.urls import path
from .api_views import CouriersPostRequest, OrdersPostRequest


urlpatterns = [
    path('couriers', CouriersPostRequest.as_view()),
    path('orders', OrdersPostRequest.as_view()),
]
