from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import types


# --- utils buttons ---
btnBack = KeyboardButton('Back')
btnCancel = KeyboardButton('Cancel')
btnCleanDone = KeyboardButton('Clean')

cancelMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(btnCancel)

# --- Main Menu buttons ---
btnCreate = KeyboardButton('Create')
btnWatchList = KeyboardButton('Show reminders')
mainMenu = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1, one_time_keyboard=True).add(btnCreate,
                                                                      btnWatchList,
                                                                      btnCleanDone)

# --- Show Reminders Menu buttons ---
btnShowAll = KeyboardButton('All')
btnShowPermanent = KeyboardButton('Permanent')
btnShowTemporary = KeyboardButton('Temporary')
remindersMenu = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1).add(btnShowAll,
                                                                           btnShowPermanent,
                                                                           btnShowTemporary,
                                                                           btnBack)

# --- Reminders Menu buttons ---
anyRemindersMenu = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1).add(btnCleanDone, btnBack)

# --- Inline Create Reminder buttons ---
inline_btn_temp = InlineKeyboardButton('Temporary', callback_data='btn_temp')
inline_btn_perm = InlineKeyboardButton('Permanent', callback_data='btn_perm')
inline_btn_cancel = InlineKeyboardButton('Cancel', callback_data='btn_cancel')
inline_btn_cancel_adding = InlineKeyboardButton('Cancel', callback_data='cancel_adding')

inline_kb1 = InlineKeyboardMarkup(row_width=2).add(inline_btn_temp, inline_btn_perm, inline_btn_cancel)
inline_kb2 = InlineKeyboardMarkup().add(inline_btn_cancel_adding)

# --- Inline Editing Reminder status buttons ---
inline_btn_done = InlineKeyboardButton('Done', callback_data='btn_done')
inline_btn_delete = InlineKeyboardButton('Delete', callback_data='btn_delete')
inline_btn_edit = InlineKeyboardButton('Edit', callback_data='btn_edit')

inline_kb_edit1 = InlineKeyboardMarkup(row_width=2).add(inline_btn_done, inline_btn_delete, inline_btn_edit)

# --- Inline Editing Reminder buttons ---
inline_btn_back = InlineKeyboardButton('<<< Back', callback_data='btn_back')
inline_btn_edit_text = InlineKeyboardButton('Text', callback_data='btn_edit_text')
inline_btn_edit_date = InlineKeyboardButton('Date', callback_data='btn_edit_date')
inline_btn_edit_type = InlineKeyboardButton('Type', callback_data='btn_edit_type')
inline_btn_edit_frequency = InlineKeyboardButton('Frequency', callback_data='btn_edit_frq')

inline_kb_edit2 = InlineKeyboardMarkup(row_width=2).add(inline_btn_edit_text,
                                                        inline_btn_edit_date,
                                                        inline_btn_edit_type,
                                                        inline_btn_edit_frequency,
                                                        inline_btn_back)
