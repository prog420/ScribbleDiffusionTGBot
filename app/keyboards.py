from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

cmd_regenerate = "Regenerate image"
cmd_retry = "Retry"

button_regenerate = KeyboardButton(cmd_regenerate)
button_retry = KeyboardButton(cmd_retry)

kb_regenerate = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kb_regenerate.add(button_regenerate)

kb_retry = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kb_retry.add(button_retry)
