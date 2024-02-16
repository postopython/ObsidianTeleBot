# -*- coding: utf-8 -*-

import telebot
import datetime
from telebot.types import InputFile, InlineKeyboardMarkup, InlineKeyboardButton
import os

bot = telebot.TeleBot(token)
Check_list = set()


@bot.message_handler(commands=['help', 'start'])
def start(message):
    bot.send_message(message.chat.id,
                     'Ты уже забыл зачем этот бот? Офигеть у тебя память, конечно. Короче, пишешь сюда сообщение, а я создаю .md файл с текстом, который ты мне отправишь.')


@bot.message_handler(commands=['download'])
def download(message):
    markup = InlineKeyboardMarkup()
    files = os.listdir(path="files")
    button_all = InlineKeyboardButton('Скачать всё', callback_data='download_all')
    button_unchecked = InlineKeyboardButton('Скачать новые', callback_data='download_unchecked')
    markup.row(button_all, button_unchecked)
    for value in files:
        data = f'download_{value}'
        if value in Check_list:
            text = f'{value}-✓'
        else:
            text = value
        markup.add(InlineKeyboardButton(text, callback_data=data))
    bot.send_message(message.chat.id, 'Выберите файл', reply_markup=markup)


@bot.message_handler(commands=['delete'])
def delete(message):
    markup = InlineKeyboardMarkup()
    button_all = InlineKeyboardButton('Удалить всё', callback_data='delete_all')
    button_unchecked = InlineKeyboardButton('Удалить старые', callback_data='delete_checked')
    markup.row(button_all, button_unchecked)
    files = os.listdir(path="files")
    for value in files:
        data = f'delete_{value}'
        if value in Check_list:
            text = f'{value}-✓'
        else:
            text = value
        markup.add(InlineKeyboardButton(text, callback_data=data))
    bot.send_message(message.chat.id, 'Выберите файл', reply_markup=markup)


@bot.message_handler(commands=['check'])
def check(message):
    bot.send_message(message.chat.id, Check_list)


@bot.message_handler(commands=['files', 'file'])
def files(message):
    files = os.listdir(path='files')
    text = 'Список файлов: \n'
    file_list = map(lambda x: x + '\n', files)
    text += ''.join(file_list)
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['hosting'])
def hosting(message):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('PythonEverywhere',
                                    url=hosting_url))
    bot.send_message(message.chat.id, 'Хостинг: Pythoneverywhere', reply_markup=markup)


@bot.callback_query_handler(func=lambda callback: True)
def callback_func(callback):
    global Check_list
    data_list = callback.data.split('_')
    if data_list[0] == 'download':
        if data_list[1] == 'all':
            send_list = os.listdir(path='files')
            print(send_list)
            for filename in send_list:
                bot.send_document(callback.from_user.id, InputFile(f'files/{filename}'))
                Check_list.add(filename)
        elif data_list[1] == 'unchecked':
            send_list = os.listdir(path='files')
            for filename in send_list:
                if filename not in Check_list:
                    bot.send_document(callback.from_user.id, InputFile(f'files/{filename}'))
                    Check_list.add(filename)
        else:
            bot.send_document(callback.from_user.id, InputFile(f'files/{data_list[1]}'))
            Check_list.add(data_list[1])
    elif data_list[0] == 'delete':
        if data_list[1] == 'all':
            file_list = os.listdir('files')
            for filename in file_list:
                os.remove(f'files/{filename}')
            Check_list.clear()
            bot.send_message(callback.from_user.id, f'Все файлы успешно удалены!')
        elif data_list[1] == 'checked':
            file_list = os.listdir('files')
            for filename in file_list:
                if filename in Check_list:
                    os.remove(f'files/{filename}')
                    Check_list.remove(filename)
            bot.send_message(callback.from_user.id, f'Файлы успешно удалены!')
        else:
            os.remove(f'files/{data_list[1]}')
            bot.send_message(callback.from_user.id, f'Файл {data_list[1]} успешно удалён!')
            Check_list.remove(data_list[1])


@bot.message_handler()
def write(message):
    date_time = datetime.datetime.now()
    date = str(date_time.date()) + 'T' + str(date_time.time()).replace(':', '-')[:8]
    file = open(f'files/{date_time.date()}.md', 'a+', encoding='utf-8')
    text = date + '\n' + str(message.text) + '\n\n'
    file.write(text)
    file.close()
    bot.send_message(message.chat.id, 'Текст записан')


bot.polling(non_stop=True)
