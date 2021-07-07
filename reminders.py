from typing import NamedTuple
import datetime
import pytz
from dateutil.parser import parse
from typing import Union

import exceptions
import db
from utility import TemporaryReminder, PermanentReminder, Bookmark


def add_reminder(title: str,
                 date: str,
                 category: str,
                 frequency: int = 0) -> Union[TemporaryReminder, PermanentReminder, Bookmark]:
    date = parse(date, fuzzy=True)
    print(date)
    db.insert(
        'reminder',
        {
            'name': title,
            'date_time': date,
            'category': category,
            'for_each': frequency
        }
    )
    if category == 'temp':
        return TemporaryReminder(title=title, type=category, date=date, is_done=False)
    elif category == 'perm':
        return PermanentReminder(title=title, type=category, date=date, frequency=frequency, is_done=False)
    else:
        return Bookmark(title=title, type=category, is_done=False)


def get_all_reminders():
    cursor = db.get_cursor()
    cursor.execute(
        "select * from reminder order by date_time ASC limit 10 ")
    rows = cursor.fetchall()
    if not rows:
        return "No reminders in system"
    return rows

    # answer_message = _data_to_result_string("All", rows)
    # return answer_message


def get_permanent_reminders():
    cursor = db.get_cursor()
    cursor.execute(
        "select * from reminder where category = 'perm' order by date_time ASC limit 10 ")
    rows = cursor.fetchall()
    if not rows:
        return "No permanent reminders in system"
    return rows

    # answer_message = _data_to_result_string("Permanent", rows)
    # return answer_message


def get_temporary_reminders():
    cursor = db.get_cursor()
    cursor.execute(
        "select * from reminder where category = 'temp' order by date_time ASC limit 10 ")
    rows = cursor.fetchall()
    if not rows:
        return "No temporary reminders in system"
    return rows
    # answer_message = _data_to_result_string("Temporary", rows)
    # return answer_message


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
    return done_reminder


def _get_now_formatted() -> str:
    """returns data on str type"""
    return _get_now_datetime().strftime("%Y-%m-%d %H:%M:%S")


def _get_now_datetime() -> datetime.datetime:
    """returns datetime with Moscow timezone"""
    tz = pytz.timezone("Europe/Moscow")
    now = datetime.datetime.now(tz)
    return now


def _parse_message(message) -> TemporaryReminder:
    data = message.split('.')
    try:
        type = data[0]
        title = data[1]
        date = parse(data[2], fuzzy=True)
    except IndexError:
        raise exceptions.NotCorrectMessage("can't parse this message")

    if type == 'temp' or type == 'perm':
        return TemporaryReminder(title=title, date=date, type=type, is_done=False)
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
