from datetime import date, timedelta


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
