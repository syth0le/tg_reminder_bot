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
    # data_done = bool(data_done)
    # stick_done = STICKER_DONE if bool(data_done) else STICKER_NOT_DONE
    if isinstance(data_done, str):
        if data_done == 'True':
            stick_done = STICKER_DONE
        else:
            stick_done = STICKER_NOT_DONE
    elif isinstance(data_done, bool):
        stick_done = STICKER_DONE if data_done else STICKER_NOT_DONE
    else:
        stick_done = STICKER_DONE if data_done else STICKER_NOT_DONE
    # print(data_done, type(bool(data_done)))
    if data_type == 'perm':
        stick_type = STICKER_PERMANENT
    elif data_type == 'temp':
        stick_type = STICKER_TEMPORARY
    else:
        stick_type = STICKER_BOOKMARK
    return stick_done, stick_type