from typing import NamedTuple

RAM_saver = set()


class Reminder(NamedTuple):
    name: str
    date: str
    time: str


def add_reminder(message):
    return f'added new reminder {message}'


def get_all_reminders():
    return 'all'


def get_permanent_reminders():
    return 'perm'


def get_temporary_reminders():
    return 'temp'


def delete_done_reminders():
    return 'cleaned'


def delete_reminder(row_id):
    return f'deleted reminder {row_id}'
