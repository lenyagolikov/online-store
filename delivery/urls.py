from django.urls import path
from .views import *

app_name = 'delivery'

urlpatterns = [
    path('', CourierCreateView.as_view())
]
