from telebot import types


'''def timetable():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*[types.KeyboardButton(advert) for advert in
                   ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота']])
    keyboard.add(*[types.KeyboardButton(advert) for advert in ['/start']])
    return keyboard'''

def main_menu():
    markup = types.InlineKeyboardMarkup()  # создаем кнопки
    markup.add(types.InlineKeyboardButton(text='Расписание на неделю',
                                                  callback_data='timetable'))  # markup - объявляет новую переменную с inline keyboard, а markup.add – создает отдельную кнопку
    markup.add(types.InlineKeyboardButton(text='Список учителей',
                                                  callback_data='teachers'))  # text - отвечает за текст на кнопке
    markup.add(types.InlineKeyboardButton(text='Расписание звонков',
                                                  callback_data='bells'))    # callback_data - отвечает за данные, переданные боту после выборе пользователя
    markup.add(types.InlineKeyboardButton(text='Образцы заявлений', callback_data='documents'))
    return markup
