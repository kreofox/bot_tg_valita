import telebot


from currency_converter import CurrencyConverter
from telebot import types

bot = telebot.Telebot = "TOKEN_BOT"
curre = CurrencyConverter()
amount = 0

@bot.message_handler(commands =["start"])
def start(message):
    bot.send_message(message.chat.id, "Привет введи сумму: ")
    bot.register_next_step_handler(message, summa)

def summa(message):
    global amount
    try:
        amount = int(message.text.strip())
    except ValueError: #This is to prevent the bot from breaking 
        bot.send_message(message.chat.id, "You wrote it wrong, write it again. ")
        bot.register_next_step_handler(message,summa)
        return

    if amount > 0:
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn1 = types.InlineKeyboardButton('USD/EUR', callback_data='usd/eur')
        btn2 = types.InlineKeyboardButton('USD/RU', callback_data='usd/ru')
        btn3 = types.InlineKeyboardButton('USD/GBP', callback_data='usd/gbp')
        btn4 = types.InlineKeyboardButton('Other value', callback_data='else')
        markup.add(btn1, btn2, btn3, btn4)
        bot.send_message(message.chat.id, "Select a currency pair", reply_markup = markup)
    else:
        bot.send_message(message.chat.id, 'the amount entered is wrong again')
        bot.register_next_step_handler(message,summa)

@bot.callback_query_hanler(func = lambda call: True)
def callback(call):
    if call.date != 'else':
        values = call.data.upper().split('/')
        res = curre.convert(amount, values[0], values[1])
        bot.send_message(call.message.chat.id, f"It turns out:{round(res, 2)} you can re-pay the amount")
        bot.register_next_step_handler(call.message, summa)
    else:
        bot.send_message(call.message.chat.id, 'The number must be greater than 0 ')
        bot.register_next_step_halder(call.message, mycurrency)

def mycurrency(message):
    try:
        values = message.text.upper().split('/')
        res = curre.convert(amount, values[0], values[1])
        bot.send_message(message.message.chat.id, f"It turns out:{round(res, 2)} you can re-pay the amount")
        bot.register_next_step_handler(message, summa)
    except Exception: #It avoids crashes due to unforeseen and sudden bugs.
        bot.send_message(message.message.chat.id, "Something is wrong. You see the amount")
        bot.register_next_step_handler(message, mycurrency)

bot.polling(none_stope=True)