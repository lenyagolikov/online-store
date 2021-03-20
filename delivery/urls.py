from django.urls import path
from .views import courier_list


urlpatterns = [
    path('couriers', courier_list),
]
