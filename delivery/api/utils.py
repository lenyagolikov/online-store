from datetime import time


def previous_order_time(Assign, Order, courier_id):
    """
    Находит время окончания предыдущего заказа
    Если заказ первый, то возвращает время назначения заказов
    """

    delivery = Assign.objects.get(courier_id=courier_id, completed=False)

    if delivery.finished_orders == []:
        return delivery.assign_time
    else:
        order_id = delivery.finished_orders[-1]
        order = Order.objects.get(order_id=order_id)
        return order.complete_time


def is_available_order_time(delivery_hours, working_hours):
    """
    Принимает часы доставки заказа и график работы курьера
    Если курьеру удобно принять заказ, то возвращает True, иначе False

    delivery_hours - часы доставки заказа
    working_hours - график работы курьера
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


def calculation_of_rating():
    pass


def calculation_of_earnings():
    pass
