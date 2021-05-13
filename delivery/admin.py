from django.contrib import admin

from .models import Courier, Order, Assign

admin.site.register(Courier)
admin.site.register(Order)
admin.site.register(Assign)
