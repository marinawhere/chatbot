import telebot   # Для начала импортируем библиотеку pyTelegramBotAPI
from telebot import types

token = '5075963542:AAFajStxGJilq3e_Tsebr5T4bIvM0naoR48'  # Затем зададим переменную token равную нашему токену, который мы получили от BotFather для взаимодействия с Telegram Bot Api
bot = telebot.TeleBot(token)  # Объявим бота

@bot.message_handler(commands=['start']) #бот обрабатывает команду /start
def start_message(message):
    markup = telebot.types.InlineKeyboardMarkup() #создаем кнопки
    markup.add(telebot.types.InlineKeyboardButton(text='Расписание на неделю', callback_data='timetable')) # markup - объявляет новую переменную с inline keyboard, а markup.add – создает отдельную кнопку
    markup.add(telebot.types.InlineKeyboardButton(text='Список учителей', callback_data='teachers'))   # text - отвечает за текст на кнопке
    markup.add(telebot.types.InlineKeyboardButton(text='Расписание звонков', callback_data='bells'))  # callback_data - отвечает за данные, переданные боту после выборе пользователя
    markup.add(telebot.types.InlineKeyboardButton(text='Образцы заявлений', callback_data='documents'))
    bot.send_message(message.chat.id, text="Привет, чем я могу тебе помочь?", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)  # в этом блоке описываем обработку результатов нажатий кнопок
def query_handler(call):

    bot.answer_callback_query(callback_query_id=call.id, text='Результат вашего запроса.')  # bot.answer_callback_quer – это всплывающее окно, которое будет показано пользователю после нажатия кнопки
    answer = ''
    if call.data == 'timetable':  # в call.data будет передано значение, которое мы указывали при создании клавиатуры в параметре callback_data
        answer = 'придумать как вывести таблицу с расписанием'
    elif call.data == 'teachers':
        answer = 'придумать как вывести таблицу с фио + предмет + почта+номер телефона'
    elif call.data == 'bells':
        answer = 'придумать как вывести таблицу с расписанием звонков'
    elif call.data == 'documents':
        answer = 'придумать как выыести список образцов в виде файлов'

    bot.send_message(call.message.chat.id, answer)

    ''' bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)'''

bot.polling()
