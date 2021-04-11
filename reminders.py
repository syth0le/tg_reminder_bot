from typing import NamedTuple
import datetime
import pytz

import exceptions

ram_saver = set()


class Reminder(NamedTuple):
    name: str
    date: str
    # time: Optional[str]
    rem_type: str


def add_reminder(message):
   reminder = _parse_message(message)
   ram_saver.add(reminder)
   return reminder


def get_all_reminders():
    return f'all\n {ram_saver}'


def get_permanent_reminders():
    return f'perm\n {ram_saver}'


def get_temporary_reminders():
    return f'temp\n {ram_saver}'


def delete_done_reminders():
    ram_saver.clear()
    return 'cleaned'


def delete_reminder(row_id):
    ram_saver.remove(row_id)
    return f'deleted reminder {row_id}'


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
