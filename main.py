'''
Для начала импортируем библиотеу pyTelegramBotAPI для работы с Telegram.
'''
import telebot
from telebot import types

'''
Далее импортируем дополнительные файлы, чтобы соединить их с основным файлом "main.py":
Файл "main_menu.py" содержит функцию, возвращающую переменную, содержащую кнопки главного меню;
Файл "bells.py"получает и возврщает данные таблицы "bells" из базы данных "chatbot_database.db"
Файл "teachers.py" получает и возврщает данные таблицы "teachers" из базы данных "chatbot_database.db".
'''
import main_menu
import bells
import teachers

'''
Ниже приведенные файлы работют с базой данных "chatbot_database.db".
Они получают и обрабатывают данные таблиц с расписаниями на соответствующие дни.
'''
import monday_tab
import tuesday_tab
import wednesday_tab
import thursday_tab
import friday_tab
import saturday_tab

'''
Затем зададим переменную "token" равную нашему токену (уникальная строка из символов, которая нужна для того, чтобы 
установить подлинность бота в системе), который мы получили от BotFather для взаимодействия с Telegram Bot Api, 
а также объявим бота.
'''
token = '5075963542:AAFajStxGJilq3e_Tsebr5T4bIvM0naoR48'
bot = telebot.TeleBot(token)

'''
Далее задается декоратор. На данном шаге наш бот будет обрабатывать команду "/start", которая равносильна нажатию
кноки "Вернуться назад".
С помощью метода "ReplyKeyboardRemove()" Бот удаляет встроенную клавиатуру, чтобы начать работу "с чистого листа".
Переменная "markup" возвращается из функции "main_menu()" файла "main_menu.py" и является набором кнопок с главным меню.

'''
@bot.message_handler(commands=['start'])
def start_message(message):
   keyboard = types.ReplyKeyboardRemove()
   bot.send_message(message.chat.id, text="Привет! Чем я могу тебе помочь?",
                    reply_markup=keyboard)
   markup = main_menu.main_menu()
   bot.send_message(message.chat.id, text="Выбери нужное:", reply_markup=markup) #предлагаем пользователю выбрать запрос

'''
Далее задается еще один декоратор. 
В этом блоке мы описываем обработку ботом результатов нажатий кнопок главного меню.

"bot.answer_callback_quer" – это всплывающее окно, которое будет показано пользователю после нажатия кнопки.

Основные параметры при создании кнопки: "text" - текст на кнопке, "callback_data" – данные, которые будут переданы боту
при выборе пользователем определенного варианта ответа. 

В "call.data" будет передано значение, 
которое мы указывали при создании клавиатуры в параметре "callback_data".

С помощью методов ".ReplyKeyboardMarkup(resize_keyboard=True)" и ".add(types.KeyboardButton())" мы 
изменяем кнопки встроенной клавиатуры.

text = название_файла.название_функции()
Переменная text возвращает значение переменной text, являющейся возвращенным значением данной функции из данного файла.
'''
@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
   bot.answer_callback_query(callback_query_id=call.id, text='Результат вашего запроса.')

   if call.data == 'timetable':  # Вложенное меню для кнопки "Расписание уроков"
       keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
       keyboard.add(*[types.KeyboardButton(element) for element in
                      ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Вернуться назад']])
       bot.send_message(call.message.chat.id, 'Выберите нужный день.',
                        reply_markup=keyboard)   #  Предлагаем пользователю выбрать запрос

   elif call.data == 'teachers':
       keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
       keyboard.add(types.KeyboardButton('Вернуться назад'))
       text = teachers.teachers()
       # Переменная "text" содержит данные таблицы "teachers", подробно в "teachers.py"
       bot.send_message(call.message.chat.id, 'Список учителей и их контактные данные по вашему запросу:',
                        reply_markup=keyboard)
       bot.send_message(call.message.chat.id, text)

   elif call.data == 'bells':  # Вывод результатов нажатия кнопки "Расписание звонков"
       keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
       keyboard.add(types.KeyboardButton('Вернуться назад'))
       text = bells.bells()
       # Переменная "text" содержит данные таблицы "bells", подробно в "bells.py"
       bot.send_message(call.message.chat.id, 'Расписание звонков:',
                        reply_markup=keyboard)
       bot.send_message(call.message.chat.id, text)


   elif call.data == 'documents': # Вложенное меню для Образцов заявлений
       keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
       keyboard.add(*[types.KeyboardButton(element) for element in
                      ['Освобождение.', 'Самостоятельный уход из школы/с мероприятия.', 'Вернуться назад']])
       bot.send_message(call.message.chat.id, 'Выберите нужный образец.',
                        reply_markup=keyboard)


'''
Приведенный ниже декоратор реагирует лишь на текстовые сообщения, то есть на нажатия вложенных кнопок.

text = название_файла.название_функции()
Переменная text возвращает значение переменной text, являющейся возвращенным значением данной функции из данного файла.
'''
@bot.message_handler(content_types=['text'])
def answer_on_message(message):
   if message.text == 'Понедельник':
       bot.send_message(message.chat.id, 'Расписание на понедельник.')
       text = monday_tab.timetable_monday()
       # Переменная "text" содержит данные таблицы "monday", подробно в "monday_tab.py"
       bot.send_message(message.chat.id, text)

   elif message.text == 'Вторник':
       bot.send_message(message.chat.id, 'Расписание на вторник.')
       text = tuesday_tab.timetable_tuesday()
       # Переменная "text" содержит данные таблицы "tuesday", подробно в "tuesday_tab.py"
       bot.send_message(message.chat.id, text)

   elif message.text == 'Среда':
       bot.send_message(message.chat.id, 'Расписание на среду.')
       text = wednesday_tab.timetable_wednesday()
       # Переменная "text" содержит данные таблицы "wednesday", подробно в "wednesday_tab.py"
       bot.send_message(message.chat.id, text)

   elif message.text == 'Четверг':
       bot.send_message(message.chat.id, 'Расписание на четверг.')
       text = thursday_tab.timetable_thursday()
       # Переменная "text" содержит данные таблицы "thursday", подробно в "thursday_tab.py"
       bot.send_message(message.chat.id, text)

   elif message.text == 'Пятница':
       bot.send_message(message.chat.id, 'Расписание на пятницу.')
       text = friday_tab.timetable_friday()
       # Переменная "text" содержит данные таблицы "friday", подробно в "friday_tab.py"
       bot.send_message(message.chat.id, text)

   elif message.text == 'Суббота':
       bot.send_message(message.chat.id, 'Расписание на субботу.')
       text = saturday_tab.timetable_saturday()
       # Переменная "text" содержит данные таблицы "saturday", подробно в "saturday_tab.py"
       bot.send_message(message.chat.id, text)

   elif message.text == 'Освобождение.':
       bot.send_message(message.chat.id, "Образец заявления об освобождении.")
       bot.send_document(message.chat.id, open(r"C:\Users\Marina\Desktop\chatbot\release.docx", "rb"))

   elif message.text == 'Самостоятельный уход из школы/с мероприятия.':
       bot.send_message(message.chat.id, "Образец заявления о самостоятельном уходе с мероприятия.")
       bot.send_document(message.chat.id, open(r"C:\Users\Marina\Desktop\chatbot\selfcare.docx", "rb"))

   elif message.text == 'Вернуться назад':
       return start_message(message)

'''
Чтобы бот постоянно ожидал запрос от пользователя в конце пропишем:
'''
bot.polling(none_stop=True)
