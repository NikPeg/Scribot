from settings import *
from messages import *
import telebot
from telebot import types

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text='Загрузить работу', callback_data='download')
    btn2 = types.InlineKeyboardButton(text='Узнать о Scribo', callback_data='info')
    btn3 = types.InlineKeyboardButton(text='Связаться с командой', callback_data='connect')
    btn4 = types.InlineKeyboardButton(text='Отправить донат', callback_data='donate')
    markup.add(btn1, btn2)
    markup.add(btn3, btn4)
    bot.send_message(message.from_user.id, START_MESSAGE, reply_markup=markup)


@bot.callback_query_handler(func=lambda call:True)
def callback_query(call):
    req = call.data.split('_')
    if req[0] == 'info':
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton(text='Канал проекта', url='https://t.me/scribo_project')
        markup.add(btn1)
        bot.send_message(call.from_user.id, ABOUT_MESSAGE, reply_markup=markup)


bot.polling(none_stop=True, interval=0)
