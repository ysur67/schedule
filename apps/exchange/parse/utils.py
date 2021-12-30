from datetime import time
from typing import Tuple


def get_time_range_from_string(string: str) -> Tuple[time, time]:
    """Получить временной диапазон из строки.

    Обязательный формат строки, который используется на данный момент
    `hh:mm-hh:mm`.

    Args:
        string (str): Строка с временным промежутком.

    Raises:
        TypeError: Если строка имеет неправильный формат.

    Returns:
        time, time: Диапазон, вида - начало, конец.
    """
    initial = string.split("-")
    if not initial:
        raise TypeError("time range is invalid")
    start_hour, start_minute = get_hours_and_minutes(initial[0])
    end_hour, end_minute = get_hours_and_minutes(initial[1])
    start = time(hour=start_hour, minute=start_minute)
    end = time(hour=end_hour, minute=end_minute)
    return start, end


def get_hours_and_minutes(string: str) -> Tuple[int, int]:
    """Получить часы и минуты из строки.

    Обязательный формат строки - `hh:mm`

    Args:
        string (str): Строка

    Raises:
        TypeError: Если строка имела неправильный формат.

    Returns:
        int, int: Часы, минуты.
    """
    initial = string.split(":")
    if not initial:
        raise TypeError("time format is invalid")
    hour = int(initial[0])
    minute = int(initial[1])
    return hour, minute
