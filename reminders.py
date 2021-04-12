from typing import NamedTuple
import datetime
import pytz
from dateutil.parser import parse

import exceptions
import db


class Reminder(NamedTuple):
    name: str
    date: str
    category: str


def add_reminder(message) -> Reminder:
    reminder = _parse_message(message)
    temp = db.insert(
        'reminder',
        {
            'name': reminder.name,
            'date_time': reminder.date,
            'category': reminder.category
        }
    )
    return f'Created "{reminder.name}" on {reminder.date}'


def get_all_reminders():
    cursor = db.get_cursor()
    cursor.execute(
        "select * from reminder order by date_time ASC limit 10 ")
    rows = cursor.fetchall()
    if not rows:
        return "No reminders in system"

    answer_message = _data_to_result_string("All", rows)
    return answer_message


def get_permanent_reminders():
    cursor = db.get_cursor()
    cursor.execute(
        "select * from reminder where category = 'perm' order by date_time ASC limit 10 ")
    rows = cursor.fetchall()
    if not rows:
        return "No permanent reminders in system"

    answer_message = _data_to_result_string("Permanent", rows)
    return answer_message

def get_temporary_reminders():
    cursor = db.get_cursor()
    cursor.execute(
        "select * from reminder where category = 'temp' order by date_time ASC limit 10 ")
    rows = cursor.fetchall()
    if not rows:
        return "No temporary reminders in system"
    answer_message = _data_to_result_string("Temporary", rows)
    return answer_message


def delete_done_reminders():
    db.clean_done('reminder')
    return 'done reminders were cleaned'


def delete_reminder(row_id):
    try:
        deleted = db.delete('reminder', row_id)
    except exceptions.NotConsistInDB as e:
        return str(e)
    return f'reminder {deleted[1]} was deleted'


def done_reminder(row_id):
    try:
        done_reminder = db.update('reminder', row_id)
    except exceptions.NotConsistInDB as e:
        return str(e)
    return f'reminder {done_reminder[1]} is done'


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
        category = data[0]
        name = data[1]
        date = parse(data[2], fuzzy=True)
    except IndexError:
        raise exceptions.NotCorrectMessage("can't parse this message")

    if category == 'temp' or category == 'perm':
        return Reminder(name=name, date=date, category=category)
    else:
        raise exceptions.NotCorrectMessage("not correct category")

def _data_to_result_string(kind, rows):
    last_reminders_rows = [
        f"{reminder[1]} ({reminder[3]}) — нажми "
        f"/del{reminder[0]} или "
        f"/done{reminder[0]}  "
        for reminder in rows]
    answer_message = f"{kind} reminders:\n\n* " + "\n\n* "\
            .join(last_reminders_rows)
    return answer_message
