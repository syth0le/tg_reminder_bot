from typing import NamedTuple
import datetime
import pytz

import exceptions
import db

ram_saver = set()


class Reminder(NamedTuple):
    name: str
    date: str
    rem_type: str


def add_reminder(message) -> Reminder:
    reminder = _parse_message(message)
#   ram_saver.add(reminder)
    # category = Categories().get_category(
    #     reminder.category_text)
    temp = db.insert(
        'reminder',
        {
            # 'category': reminder.rem_type,
            'name': reminder.name,
            'date_time': reminder.date
        }
    )
    return reminder


def get_all_reminders():
    """Возвращает последние несколько расходов"""
    cursor = db.get_cursor()
    cursor.execute(
        "select * from reminder limit 10")
    rows = cursor.fetchall()
    # last_expenses = [Reminder(id=row[0], amount=row[1], category_name=row[2]) for row in rows]
    return f'all\n {rows}'


def get_permanent_reminders():
    cursor = db.get_cursor()
    cursor.execute(
        "select * from reminder where category = 'perm' limit 10")
    rows = cursor.fetchall()
    return f'perm\n {rows}'


def get_temporary_reminders():
    cursor = db.get_cursor()
    cursor.execute(
        "select * from reminder where category = 'temp' limit 10")
    rows = cursor.fetchall()
    return f'temp\n {rows}'


def delete_done_reminders():
    db.clean_done('reminder')
    return 'cleaned'


def delete_reminder(row_id):
    try:
        deleted = db.delete('reminder', row_id)
    except exceptions.NotConsistInDB as e:
        return str(e)
    return f'deleted reminder {deleted}'


def done_reminder(row_id):
    # realize method put 
    try:
        updated = db.update('reminder', row_id)
    except exceptions.NotConsistInDB as e:
        return str(e)
    return f'updated reminder {updated}'


def _get_now_formatted() -> str:
    """returns data on str type"""
    return _get_now_datetime().strftime("%Y-%m-%d %H:%M:%S")


def _get_now_datetime() -> datetime.datetime:
    """returns datetime with Moscow timezone"""
    tz = pytz.timezone("Europe/Moscow")
    now = datetime.datetime.now(tz)
    return now


def _parse_message(message) -> Reminder:
    data = message.split('.')
    try:
        rem_type = data[0]
        name = data[1]
        date = data[2]
    except IndexError:
        raise exceptions.NotCorrectMessage("can't parse this message")

    if rem_type == 't' or rem_type == 'p':
        return Reminder(name=name, date=date, rem_type=rem_type)
    else:
        raise exceptions.NotCorrectMessage("not correct category")
