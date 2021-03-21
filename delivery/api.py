from rest_framework import status
from rest_framework.response import Response


def data_is_valid(request, ModelSerializer, model):
    """Проверка валидности входных данных

    request - принимаемый запрос
    ModelSerializer - модель класса из БД
    model - название модели

    """
    data_list = request.data['data']

    correct_data_list = []
    id_errors_list = []

    for data in data_list:
        serializer = ModelSerializer(data=data)

        if serializer.is_valid():
            correct_data_list.append(serializer)
        else:
            id_errors_list.append(serializer[next(iter(serializer.fields))])

    if id_errors_list == []:
        for data in correct_data_list:
            data.save()
        return Response({model: [{"id": data[next(iter(data.fields))].value} for data in correct_data_list]}, status=status.HTTP_201_CREATED)

    return Response({"validation_error": {model: [{"id": id.value} for id in id_errors_list]}}, status=status.HTTP_400_BAD_REQUEST)
