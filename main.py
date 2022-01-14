import sqlite3

import telebot  # Для начала импортируем библиотеку pyTelegramBotAPI
from telebot import types
import menu

conn = sqlite3.connect('chatbot_database.db', check_same_thread=False)
cursor = conn.cursor()

print(cursor.execute('SELECT * FROM bells').fetchall())
print(cursor.execute('SELECT * FROM teachers').fetchall())

bells_table = cursor.execute('SELECT * FROM bells').fetchall()

def db_bells_val(types: str, time: str):
    cursor.execute('INSERT INTO bells (types, time) VALUES (?, ?, ?, ?)', (types, time))
    conn.commit()

def db_teachers_val(id: int, name: str, subject: str, email:str, phone_number:str):
    cursor.execute('INSERT INTO bells (id, name, subject, email, phone_number) VALUES (?, ?, ?, ?)', (id, name, subject, email, phone_number))
    conn.commit()



token = '5075963542:AAFajStxGJilq3e_Tsebr5T4bIvM0naoR48'  #  Затем зададим переменную token равную нашему токену, который мы получили от BotFather для взаимодействия с Telegram Bot Api
bot = telebot.TeleBot(token)  # Объявим бота


@bot.message_handler(commands=['start'])  # бот обрабатывает команду /start
def start_message(message):
    markup = menu.main_menu()
    bot.send_message(message.chat.id, text="Привет, чем я могу тебе помочь?", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)  # в этом блоке описываем обработку результатов нажатий кнопок
def query_handler(call):
    bot.answer_callback_query(callback_query_id=call.id,
                              text='Результат вашего запроса.')  # bot.answer_callback_quer – это всплывающее окно, которое будет показано пользователю после нажатия кнопки
    # answer = ''

    if call.data == 'timetable':  # в call.data будет передано значение, которое мы указывали при создании клавиатуры в параметре callback_data
        # answer = 'Выберите нужный день'
        #  keyboard = menu.timetable()
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[types.KeyboardButton(advert) for advert in
                       ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота']])
        keyboard.add(*[types.KeyboardButton(advert) for advert in ['/start']])
        return keyboard
        bot.send_message(call.message.chat.id, 'Выберите нужный день.',
                         reply_markup=keyboard)

    elif call.data == 'teachers':
        answer = 'придумать как вывести таблицу с фио + предмет + почта+номер телефона'
        bot.send_message(call.message.chat.id, answer)
        li = cursor.execute('SELECT * FROM teachers').fetchall()
        text = ''
        for id, name, subject, email, phone_number in li:
            text += f"{str(id) str(name)} {str(subject)} {str(email)}  {str(phone_number)}\n"
        bot.send_message(call.message.chat.id, text)

    elif call.data == 'bells':
        #  bells_table = cursor.execute('SELECT * FROM bells').fetchall()
        answer = 'придумать как вывести таблицу с расписанием звонков'
        bot.send_message(call.message.chat.id, answer)
        bot.send_message(call.message.chat.id, bells_table)


    elif call.data == 'documents':
        # answer = 'Выберите нужный образец.'
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[types.KeyboardButton(advert) for advert in
                       ['Освобождение.', 'Самостоятельный ход из школы/ с мероприятия.']])
        keyboard.add(*[types.KeyboardButton(advert) for advert in ['/start']])
        bot.send_message(call.message.chat.id, 'Выберите нужный образец.',
                         reply_markup=keyboard)

    ''' bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)'''


bot.polling(none_stop=True)
