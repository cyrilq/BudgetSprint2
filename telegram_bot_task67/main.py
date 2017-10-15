import telebot
from telebot import types
import re
import requests
import time
from const import API
from get_info import GetInfoAboutOrganisation
bot = telebot.TeleBot(API)

@bot.message_handler(commands=['inn'])
def send_welcome(message):
    inn = message.text[5:]
    pattern = re.compile('[0-9]{10}|[0-9]{10}')
    if pattern.match(inn):
        newOrg = GetInfoAboutOrganisation(inn, 'inn').return_info()
        bot.send_message(message.chat.id, text='ИНН: {0}'.format(inn))
        bot.send_message(message.chat.id, text=newOrg)

    else:
        bot.send_message(message.chat.id, text='Указан неверный ИНН')



@bot.message_handler(commands=['ogrn'])
def send_welcome(message):
    inn = message.text[6:]

    newOrg = GetInfoAboutOrganisation(inn, 'orgn').return_info()

    bot.send_message(message.chat.id, text='ОГРН: {0}'.format(inn))

    bot.send_message(message.chat.id, text=newOrg)


@bot.message_handler(commands=['name'])
def send_welcome(message):
    inn = message.text[6:]

    newOrg = GetInfoAboutOrganisation(inn, 'name').return_info()

    bot.send_message(message.chat.id, text='Название: {0}'.format(inn))

    bot.send_message(message.chat.id, text=newOrg)

# polling cycle
if __name__ == '__main__':
    while True:
        print('?/?')
        try:
            bot.polling(none_stop=True)
        except requests.exceptions.ConnectionError as e:
            print('There was requests.exceptions.ConnectionError')
            time.sleep(15)
