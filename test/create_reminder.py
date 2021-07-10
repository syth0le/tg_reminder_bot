from exceptions import NotCorrectMessage

from dateutil.parser import parse


def enter_title(type: str, message: str) -> str:
    if message:
        reply = f"{type}.{message}."
    else:
        raise NotCorrectMessage


def enter_date(data: str, message: str) -> str:
    if message:
        date = parse(data[2], fuzzy=True)
        data += date
    else:
        raise NotCorrectMessage

