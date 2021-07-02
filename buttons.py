from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import types

btnBack = KeyboardButton('Back')
btnCleanDone = KeyboardButton('Clean')

# --- Main Menu buttons ---
btnCreate = KeyboardButton('Create')
btnWatchList = KeyboardButton('Show reminders')
mainMenu = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1).add(btnCreate,
                                                                      btnWatchList,
                                                                      btnCleanDone)

# --- Create Menu buttons ---
btnHello = KeyboardButton('hello')
btnHello2 = KeyboardButton('hello2')
createMenu = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1).add(btnHello,
                                                                        btnHello2,
                                                                        btnBack)

# --- Show Reminders Menu buttons ---
btnShowAll = KeyboardButton('All')
btnShowPermanent = KeyboardButton('Permanent')
btnShowTemporary = KeyboardButton('Temporary')
remindersMenu = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1).add(btnShowAll,
                                                                           btnShowPermanent,
                                                                           btnShowTemporary,
                                                                           btnBack)

# --- Reminders Menu buttons ---
anyRemindersMenu = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1).add(btnCleanDone,btnBack)

# --- Inline Create Reminder buttons ---
inline_btn_temp = InlineKeyboardButton('Temporary', callback_data='btn_temp')
inline_btn_perm = InlineKeyboardButton('Permanent', callback_data='btn_perm')
inline_kb1 = InlineKeyboardMarkup().add(inline_btn_temp, inline_btn_perm)
