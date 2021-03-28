from decimal import Decimal
from datetime import time
from re import match


def validate_id(id):
    """Проверяет, чтобы id был положительным"""

    return id > 0


def validate_region(region):
    """Проверяет, чтобы регион был положительным"""

    return region > 0


def validate_regions(regions):
    """Проверяет, чтобы регионы были положительными"""

    return all([region > 0 for region in regions])


def validate_weight(weight):
    """Проверяет, чтобы вес был в указанном промежутке"""

    return Decimal("0.01") <= weight <= 50


def validate_hours(hours):
    """Проверяет, чтобы был введен корректный промежуток времени"""

    pattern = r"^(([0,1][0-9])|(2[0-3])):[0-5][0-9][-](([0,1][0-9])|(2[0-3])):[0-5][0-9]"

    for hour in hours:
        if match(pattern, hour):
            start_time = time(int(hour[:2]), int(hour[3:5]))
            end_time = time(int(hour[6:8]), int(hour[9:]))

            if start_time >= end_time:
                return False
        else:
            return False

    return True
