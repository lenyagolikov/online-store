from datetime import time


def is_completed_order_found(delivery, order_id, courier_id, complete_time, Assign, Order):
    """Поиск заказа, который нужно отметить выполненным"""

    if delivery and order_id in delivery.active_orders:
        if complete_time > previous_order_time(Assign, Order, courier_id):
            order = Order.objects.get(order_id=order_id)
            order.complete_time = complete_time
            order.save()

            delivery.active_orders.remove(order_id)
            delivery.finished_orders.append(order_id)

            if not delivery.active_orders:
                delivery.completed = True

            delivery.save()
            return True

    return False


def search_suitable_orders(available_orders, courier):
    """Поиск подходящих заказов для выдачи курьеру"""

    assigned_orders = []

    for order in available_orders:
        if order.region in courier.regions:
            if is_available_order_time(order.delivery_hours, courier.working_hours):
                max_weight = int(courier.get_courier_type_display())
                current_weight = 0

                if order.weight + current_weight <= max_weight:
                    assigned_orders.append(order.order_id)
                    order.is_available = False
                    current_weight += order.weight
                    order.save()

    return assigned_orders


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
    """Рассчитывает рейтинг курьера"""
    pass


def calculation_of_earnings(Assign, courier):
    """Рассчитывает заработок курьера"""

    earnings = 0
    completed_deliveries = Assign.objects.filter(
        courier_id=courier.courier_id, completed=True).exclude(finished_orders=[])

    for delivery in completed_deliveries:
        earnings += int(delivery.get_courier_type_display()) * 500

    courier.earnings = earnings
    courier.save()
