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
    """
    Adding reminder to db including getting parameters.
    Returns modernized NamedTuple class which include all needful information about reminder.
    It can be temporary or permanent reminders and even bookmarks classes.
    """
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


def get_all_reminders() -> list:
    """
    Returns list of all reminders from db.
    """
    cursor = db.get_cursor()
    cursor.execute(
        "select * from reminder order by date_time ASC limit 20 ")
    rows = cursor.fetchall()
    if not rows:
        return "No reminders in system"
    return rows


def get_permanent_reminders() -> list:
    """
    Returns list of permanent reminders from db.
    """
    cursor = db.get_cursor()
    cursor.execute(
        "select * from reminder where category = 'perm' order by date_time ASC limit 20 ")
    rows = cursor.fetchall()
    if not rows:
        return "No permanent reminders in system"
    return rows


def get_temporary_reminders() -> list:
    """
    Returns list of temporary reminders from db.
    """
    cursor = db.get_cursor()
    cursor.execute(
        "select * from reminder where category = 'temp' order by date_time ASC limit 20 ")
    rows = cursor.fetchall()
    if not rows:
        return "No temporary reminders in system"
    return rows


def get_bookmarks() -> list:
    """
    Returns list of bookmarks from db.
    """
    cursor = db.get_cursor()
    cursor.execute(
        "select * from reminder where category = 'book' order by date_time ASC limit 20 ")
    rows = cursor.fetchall()
    if not rows:
        return "No bookmarks in system"
    return rows


def delete_done_reminders() -> str:
    """
    Returns message with successful cleaning db by 'is_done' parameter.
    """
    db.clean_done('reminder')
    return 'done reminders were cleaned'


def delete_reminder(row_id) -> object:
    """
    Returns reminder which was deleted by user.
    """
    try:
        deleted = db.delete('reminder', row_id)
    except exceptions.NotConsistInDB as e:
        return str(e)
    return deleted


def done_reminder(row_id) -> object:
    """
    Returns reminder which 'is_done' parameter was marked as True by user.
    """
    try:
        done_reminder = db.update('reminder', row_id)
    except exceptions.NotConsistInDB as e:
        return str(e)
    return done_reminder


def _get_now_formatted() -> str:
    """
    Returns data on str type
    """
    return _get_now_datetime().strftime("%Y-%m-%d %H:%M:%S")


def _get_now_datetime() -> datetime.datetime:
    """
    Returns datetime with Moscow timezone.
    """
    tz = pytz.timezone("Europe/Moscow")
    now = datetime.datetime.now(tz)
    return now


def _parse_message(message) -> TemporaryReminder:
    # deprecated
    data = message.split('.')
    frequency = 1
    try:
        type = data[0]
        title = data[1]
        date = parse(data[2], fuzzy=True)
        if type == 'perm':
            frequency = data[3]
    except IndexError:
        raise exceptions.NotCorrectMessage("can't parse this message")

    if type == 'temp':
        return TemporaryReminder(title=title, date=date, type=type, is_done=False)
    elif type == 'perm':
        return PermanentReminder(title=title, date=date, type=type, frequency=frequency, is_done=False)
    elif type == 'book':
        return Bookmark(title=title, type=type, is_done=False)
    else:
        raise exceptions.NotCorrectMessage("not correct category")
