from rest_framework.views import APIView
from .serializers import CourierSerializer, OrderSerializer
from .services import data_is_valid


class CouriersPostRequest(APIView):

    def post(self, request):
        """Принимает POST запрос и валидирует данные"""

        data_list = request.data['data']
        return data_is_valid(data_list, CourierSerializer, "couriers")


class OrdersPostRequest(APIView):

    def post(self, request):
        """Принимает POST запрос и валидирует данные"""

        data_list = request.data['data']
        return data_is_valid(data_list, OrderSerializer, "orders")
