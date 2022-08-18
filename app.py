import telebot
from config import keys, TOKEN
from extensions import ConvertionException, CryptoConverter




bot = telebot.TeleBot(TOKEN)





@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу введите комманду боту в следующем формате: \n<имя валюты>\
    <в какую валюту перевести>\
    <количество переводимой валюты>\nУвидеть список доступных валют: /values'
    bot.reply_to(message, text)
#def echo_test(message: telebot.types.Message):
#    bot.send_message(message.chat.id, 'Hello')

@bot.message_handler(commands=['values'])
def values(message:telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text ='\n'.join((text,key,))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def get_price(message:telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) !=3 :
            raise ConvertionException('Слишком много параметров')

        quote, base, amount = values
        total_base = CryptoConverter.get_price(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя \n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработвать комманду \n{e}')
    else:
        text = f'Цена за {amount} {quote} в {base} - {float(total_base)*float(amount)}'
        bot.send_message(message.chat.id, text)

#Здесь нужно сделать замечание, что данная программа (данный бот) не может вернуть точное значение покупки N-го количества одной валюты за другую.
#Данный бот просто сверяет цены одной валюты по сравнению с другой и перемножает на желаемое количество
#Бот не способен оценить стоимость покупки валюты в некоторых количествах вообще, т.к. исходный API не предоставляет данную информацию

bot.polling()