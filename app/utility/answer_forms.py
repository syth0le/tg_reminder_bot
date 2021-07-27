from typing import Union, Optional

from app.utility.schemas import TemporaryReminder, PermanentReminder, Bookmark
from app.utility.stickers import stickers_recognize


def answer_forms(answer: Optional[Union[TemporaryReminder, PermanentReminder, Bookmark]] = None,
                 adding: Optional[bool] = False,
                 element: Optional[object] = None,
                 position: Optional[int] = None) -> str:
    if adding:
        stick_done, stick_type = stickers_recognize(element[4], element[2])
        answer_message = message_form(reminder_type=element[2],
                                      stick_done=stick_done,
                                      stick_type=stick_type,
                                      element=element,
                                      position=position)
    else:
        stick_done, stick_type = stickers_recognize(answer.is_done, answer.type)
        if not answer.type == 'book':
            answer_message = f'{stick_done} {stick_type} - {answer.title}:\n{answer.date}\n id:{answer.id}'
        else:
            answer_message = f'{stick_done} {stick_type} - {answer.title}:\n id:{answer.id}'
    return answer_message


def message_form(reminder_type: str,
                 stick_done: str,
                 stick_type: str,
                 element: object,
                 position: Optional[int] = None,
                 ) -> str:
    if reminder_type == 'temp':
        answer_message = f'{position}) {stick_done} {stick_type} - {element[1]}:\n{element[3]}\n'
    elif reminder_type == 'perm':
        answer_message = f'{position}) {stick_done} {stick_type} - {element[1]}:\n{element[3]}\n{element[5]}\n'
    elif reminder_type == 'book':
        answer_message = f'{position}) {stick_done} {stick_type} - {element[1]}\n'
    else:
        answer_message = f'{position}) {stick_done} {stick_type} - {element[1]}:\n{element[3]}\n'

    return answer_message
