import telebot
import tokens
import pars

bot = telebot.TeleBot(tokens.token)

sign = ''
description, year, genre = '', '', ''


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Я бот, пришли мне ссылку на скачивание фильма и я добавлю его на каналы")


@bot.message_handler(func=lambda message: True)
def main(message):
	global sign, description, year, genre
	if 'http' not in message.text:
		bot.reply_to(message, 'Я говорю ссылку, а не то, что ты отправил')
	else:
		print('parsing began')
		bot.send_message(message.chat.id, 'Приступаю к скачиванию')
		film = pars.get_film(message.text)
		name, description, year, genre = film[0], film[1], film[2], film[3]
		print('parsing ended')
		bot.send_message(message.chat.id, 'Готово, начинаю отправку')
		sign = name
		bot.stop_polling()
		print('downloading')


bot.polling()
