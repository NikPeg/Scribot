from settings import *
from messages import *
import telebot
from telebot import types

bot = telebot.TeleBot(TOKEN)
all_users = set()


@bot.message_handler(commands=['start', 'help'])
def start(message):
    if message.from_user.id not in all_users:
        all_users.add(message.from_user.id)
        bot.send_message(ADMIN, f"User @{message.from_user.username} started a bot.")
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text='Загрузить работу', callback_data='download')
    btn2 = types.InlineKeyboardButton(text='Узнать о Scribo', callback_data='info')
    btn3 = types.InlineKeyboardButton(text='Связаться с командой', callback_data='connect')
    btn4 = types.InlineKeyboardButton(text='Отправить донат', callback_data='donate')
    markup.add(btn1, btn2)
    markup.add(btn3, btn4)
    bot.send_message(message.from_user.id, START_MESSAGE, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    req = call.data.split('_')
    markup = types.InlineKeyboardMarkup()
    if req[0] == 'info':
        btn1 = types.InlineKeyboardButton(text='Канал проекта', url='https://t.me/scribo_project')
        btn2 = types.InlineKeyboardButton(text='Главное меню', callback_data='menu')
        markup.add(btn1)
        markup.add(btn2)
        bot.edit_message_text(
            ABOUT_MESSAGE,
            reply_markup=markup,
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
        )
    elif req[0] == 'download':
        bot.edit_message_text(
            DOWNLOAD_MESSAGE,
            reply_markup=markup,
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
        )
    elif req[0] == 'menu':
        btn1 = types.InlineKeyboardButton(text='Загрузить работу', callback_data='download')
        btn2 = types.InlineKeyboardButton(text='Узнать о Scribo', callback_data='info')
        btn3 = types.InlineKeyboardButton(text='Связаться с командой', callback_data='connect')
        btn4 = types.InlineKeyboardButton(text='Отправить донат', url='https://vtb.paymo.ru/collect-money/?transaction'
                                                                      '=73419948-d0f9-4381-bfa6-93d4bbe35954')
        markup.add(btn1, btn2)
        markup.add(btn3, btn4)
        bot.edit_message_text(
            MENU_MESSAGE,
            reply_markup=markup,
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
        )
    elif req[0] == 'connect':
        btn1 = types.InlineKeyboardButton(text='Представитель Scribo', url='https://t.me/nikpeg')
        btn2 = types.InlineKeyboardButton(text='Канал проекта', url='https://t.me/scribo_project')
        btn3 = types.InlineKeyboardButton(text='Главное меню', callback_data='menu')
        markup.add(btn1, btn2)
        markup.add(btn3)
        bot.edit_message_text(
            CONNECT_MESSAGE,
            reply_markup=markup,
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
        )


@bot.message_handler(content_types=['document'])
def get_message(message):
    bot.send_message(message.from_user.id, WORK_DOWNLOADED_MESSAGE, parse_mode='Markdown')


@bot.message_handler(content_types=['photo'])
def get_message(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text='Главное меню', callback_data='menu')
    markup.add(btn1)
    bot.send_message(message.from_user.id, PAID_MESSAGE, reply_markup=markup)
    bot.send_message(ADMIN, f"User @{message.from_user.username} paid!")


bot.infinity_polling()
