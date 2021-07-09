from typing import NamedTuple

STICKER_DONE = '✅'
STICKER_NOT_DONE = '❌'
STICKER_BELL = '🔔'
STICKER_NOTIFY = '📢'
STICKER_PERMANENT = '🔁'
STICKER_TEMPORARY = '🔂'
STICKER_BOOKMARK = '📝'
STICKER_REPEAT = '♻️'
STICKER_BOOKMARK_2 = '📒'


def stickers_recognize(data_done: bool, data_type: str):
    stick_done = STICKER_DONE if data_done else STICKER_NOT_DONE
    print(data_done, type(data_done))
    if data_type == 'perm':
        stick_type = STICKER_PERMANENT
    elif data_type == 'temp':
        stick_type = STICKER_TEMPORARY
    else:
        stick_type = STICKER_BOOKMARK
    return stick_done, stick_type


class TemporaryReminder(NamedTuple):
    id: int
    title: str
    type: str
    is_done: bool
    date: str


class PermanentReminder(NamedTuple):
    id: int
    title: str
    type: str
    is_done: bool
    frequency: int  #hours
    date: str


class Bookmark(NamedTuple):
    id: int
    title: str
    type: str
    is_done: bool
