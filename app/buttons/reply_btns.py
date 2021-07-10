from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

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
btnShowBookmarks = KeyboardButton('Bookmarks')
remindersMenu = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1).add(btnShowAll,
                                                                           btnShowPermanent,
                                                                           btnShowTemporary,
                                                                           btnShowBookmarks,
                                                                           btnBack)

# --- Reminders Menu buttons ---
anyRemindersMenu = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1).add(btnCleanDone, btnBack)
