import telebot
from config import keys, TOKEN
from extensions import APIException, Converter

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start','help'])
def help(message: telebot.types.Message):
    text = '**** ИНСТРУКЦИЯ**** \n1) Чтобы узнать цену на определенное количество валюты, отправьте сообщение Боту в следующем виде:\n \n<имя валюты цену которой вы хотите узнать> <имя валюты в которой надо узнать цену первой валюты> <количество первой валюты>\n \nНАПРИМЕР:   доллар рубль 2 \n \n2) Чтобы получить информацию о всех доступных валютах, введите команду /values.'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'ДОСТУПНЫЕ ВАЛЮТЫ:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])
def get_price(message: telebot.types.Message):
    try:
        values = message.text.lower().split(' ')
        if len(values) != 3:
            raise APIException('Неправильное количество параметров!')
        base, quote, amount = values
        total_quote = Converter.get_price(base, quote, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду.\n{e}')
    else:
        text = f'Цена {amount} {base} в {quote} - {total_quote}'
        bot.send_message(message.chat.id, text)

bot.polling()