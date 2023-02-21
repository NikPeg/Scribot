from settings import *
from messages import *
import telebot
from telebot import types

bot = telebot.TeleBot(TOKEN)
all_users = set()  # user ids in integer type
current_works = []  # users' works in (chat_id: int, message_id: int) type
making = {}  # link between moderator and work. moderator_id: (chat_id: int, message_id: int)


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
    if message.from_user.id in MODERATORS:
        btn5 = types.InlineKeyboardButton(text='Список доступных работ', callback_data='list')
        markup.add(btn5)
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
        if call.message.chat.id in MODERATORS:
            btn5 = types.InlineKeyboardButton(text='Список доступных работ', callback_data='list')
            markup.add(btn5)
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
    elif req[0] == 'work':
        btn1 = types.InlineKeyboardButton(text='Главное меню', callback_data='menu')
        markup.add(btn1)
        if call.message.chat.id not in making:
            bot.edit_message_text(
                WORK_MESSAGE,
                reply_markup=markup,
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
            )
            chat_id = int(req[1])
            message_id = int(req[2])
            making[call.message.chat.id] = (chat_id, message_id)
            current_works.remove((chat_id, message_id))
        else:
            bot.edit_message_text(
                WRONG_WORK_MESSAGE,
                reply_markup=markup,
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
            )
    elif req[0] == 'list':
        btn1 = types.InlineKeyboardButton(text='Главное меню', callback_data='menu')
        markup.add(btn1)
        if len(current_works):
            bot.edit_message_text(
                LIST_MESSAGE,
                reply_markup=markup,
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
            )
            for work_chat_id, work_message_id in current_works:
                bot.forward_message(call.message.chat.id, work_chat_id, work_message_id)
        else:
            bot.edit_message_text(
                EMPTY_LIST_MESSAGE,
                reply_markup=markup,
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
            )


@bot.message_handler(content_types=['document'])
def get_message(message):
    bot.send_message(message.from_user.id, WORK_DOWNLOADED_MESSAGE, parse_mode='Markdown')
    current_works.append((message.from_user.id, message.id))
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text='Взять в работу', callback_data=f'work_{message.from_user.id}_{message.id}')
    btn2 = types.InlineKeyboardButton(text='Главное меню', callback_data='menu')
    markup.add(btn1)
    markup.add(btn2)
    for moderator_id in MODERATORS:
        try:
            bot.forward_message(moderator_id, message.from_user.id, message.id)
            bot.send_message(moderator_id, NEW_WORK_MESSAGE, reply_markup=markup)
        except telebot.apihelper.ApiTelegramException:
            print(f"Moderator {moderator_id} has not started the bot yet")


@bot.message_handler(content_types=['photo'])
def get_message(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text='Главное меню', callback_data='menu')
    markup.add(btn1)
    bot.send_message(message.from_user.id, PAID_MESSAGE, reply_markup=markup)
    bot.send_message(ADMIN, f"User @{message.from_user.username} paid!")


@bot.message_handler(content_types=['text'])
def get_message(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text='Главное меню', callback_data='menu')
    markup.add(btn1)
    if message.from_user.id in MODERATORS and message.text == "беру":
        bot.send_message(message.from_user.id, "Кайф", reply_markup=markup)
    else:
        bot.send_message(message.from_user.id, IDK_MESSAGE, reply_markup=markup)


bot.infinity_polling()
