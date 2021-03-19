from django.shortcuts import render
from rest_framework import generics
from .serializers import CourierSerializer
from delivery import serializers


class CourierCreateView(generics.CreateAPIView):
    serializer_class = CourierSerializer
