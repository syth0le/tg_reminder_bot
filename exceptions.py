"""Кастомные исключения, генерируемые приложением"""


class NotCorrectMessage(Exception):
    """Некорректное сообщение в бот, которое не удалось распарсить"""
    pass

class NotConsistInDB(Exception):
    "incorrect message to bot when remind doesn't find in db"
    pass