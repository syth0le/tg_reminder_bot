from typing import NamedTuple

STICKER_DONE = '✅'
STICKER_NOT_DONE = '❌'


class TemporaryReminder(NamedTuple):
    title: str
    type: str
    is_done: str
    date: str


class PermanentReminder(NamedTuple):
    title: str
    type: str
    is_done: str
    frequency: int  #hours
    date: str


class Bookmark(NamedTuple):
    title: str
    type: str
    is_done: str
