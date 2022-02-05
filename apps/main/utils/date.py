from datetime import date, time, timedelta
from functools import singledispatch
from typing import Any


def get_day_of_week(value: date) -> str:
    num = value.weekday()
    if num == 0:
        return "Понедельник"
    if num == 1:
        return "Вторник"
    if num == 2:
        return "Среда"
    if num == 3:
        return "Четверг"
    if num == 4:
        return "Пятница"
    if num == 5:
        return "Суббота"
    if num == 6:
        return "Воскресенье"
    raise ValueError(f"There is no weekday with index {num}")


def date_range(start_date: date, end_date: date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)

@singledispatch
def to_message_format(data: Any) -> str:
    raise NotImplementedError(f"There is no approach for type {type(data)}")

@to_message_format.register(date)
def _(data: date) -> str:
    return data.strftime('%d.%m.%Y')

@to_message_format.register(time)
def _(data: time) -> str:
    return data.strftime("%H:%M")
