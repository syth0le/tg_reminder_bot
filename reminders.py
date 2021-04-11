from typing import NamedTuple

RAM_saver = set()


class Reminder(NamedTuple):
    name: str
    date: str
    time: str


def get_all_reminders():
    pass


def get_permanent_reminders():
    pass


def get_temporary_reminders():
    pass


def delete_done_reminders():
    pass
