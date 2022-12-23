from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

button1 = KeyboardButton('Рассчитать совместимость❤️')
button2 = KeyboardButton('Квадрат Пифагора')
button3 = KeyboardButton('Магический шар')

button4 = KeyboardButton('Квадрат Пифагора')
button6 = KeyboardButton('Помощь')

button_s1 = KeyboardButton('По дате рождения')
button_s3 = KeyboardButton('По именам')
button_s2 = KeyboardButton('По росту')

markup5 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).row(
    button1).row(button2, button3).row(button6)

markup_sovm = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).row(
    button_s1, button_s2, button_s3)

button_shar = KeyboardButton('🔮')
markup_shar = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).row(
    button_shar)

