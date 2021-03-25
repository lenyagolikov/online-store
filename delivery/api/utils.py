from datetime import time


def is_available_order_time(delivery_hours, working_hours):
    """
    Принимает часы доставки заказа и график работы курьера
    Если курьеру удобно принять заказ, то возвращает True, иначе False

    begin_time - начало промежутка
    end_time - конец промежутка
    check_time - проверка, входит ли это время в промежуток
    """

    for delivery_time in delivery_hours:
        for working_time in working_hours:

            check_time = time(int(delivery_time[:2]), int(delivery_time[3:5]))
            begin_time = time(int(working_time[:2]), int(working_time[3:5]))
            end_time = time(int(working_time[6:8]), int(working_time[9:]))

            if begin_time <= check_time <= end_time:
                return True

            check_time = time(int(working_time[:2]), int(working_time[3:5]))
            begin_time = time(int(delivery_time[:2]), int(delivery_time[3:5]))
            end_time = time(int(delivery_time[6:8]), int(delivery_time[9:]))

            if begin_time <= check_time <= end_time:
                return True

    return False