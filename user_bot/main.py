import telebot
import tokens_us
import sql_find

bot = telebot.TeleBot(tokens_us.token)

group_chat_id = -1002211480154
channel_id = 777000

genres = ['Фантастика', 'Ужасы', 'Комедия', 'Боевик', 'Драма', 'Приключения', 'Мультфильм', 'Назад']
years = ['2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024', 'Назад']
links = ['https://t.me/chanell_one']

page = 0
res = []


def orig_keyboard():
	keyboard = telebot.types.InlineKeyboardMarkup()
	keyboard.add(telebot.types.InlineKeyboardButton(text="Код", callback_data='Код'),
				 telebot.types.InlineKeyboardButton(text="Жанр", callback_data='Жанр'),
				 telebot.types.InlineKeyboardButton(text="Год", callback_data='Год'),
				 telebot.types.InlineKeyboardButton(text="Описание", callback_data='Описание'))
	return keyboard


def position_btn(page, par=None, data=None):
	global res
	print('P ', page, len(res))
	try:
		res = sql_find.find(par, data)
		print(2)
	except:
		pass

	keyboard = telebot.types.InlineKeyboardMarkup()

	for i in range((page-1)*8, page*8):
		if (len(res) <= i) and (i >= 0):
			continue
		keyboard.add(telebot.types.InlineKeyboardButton(text=str(res[i][1] + ' ' + res[i][2]), callback_data='+' + str(res[i][0])))

	if page == 1:
		keyboard.add(telebot.types.InlineKeyboardButton(text='--->', callback_data='--->'))
	else:
		keyboard.add(telebot.types.InlineKeyboardButton(text='<---', callback_data='<---'), telebot.types.InlineKeyboardButton(text='--->', callback_data='--->'))

	keyboard.add(telebot.types.InlineKeyboardButton(text='Домой', callback_data='Назад'))

	return keyboard


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
	button_support = telebot.types.KeyboardButton(text="Запуск бота")
	keyboard.add(button_support)
	bot.send_message(message.chat.id, 'Я начинаю работу!', reply_markup=keyboard)

	try:
		#bot.get_chat_member(group_chat_id, message.from_user.id)
		keyboard = orig_keyboard()
		bot.send_message(message.chat.id, "Привет, тут ты можешь найти фильм на свой вкус", reply_markup=keyboard)
	except:
		keyboard = telebot.types.InlineKeyboardMarkup()

		for i in range(0, len(links)):
			keyboard.add(telebot.types.InlineKeyboardButton(text=links[i], url=links[i]))

		bot.send_message(message.chat.id, 'Подпишись на каналы', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def save_btn(call):
	global page
	message = call.message
	print('CC: ', message)
	print('C: ', call.data)
	if call.data == 'Жанр':
		keyboard = telebot.types.InlineKeyboardMarkup()
		for i in range(1, len(genres), 2):
			keyboard.add(telebot.types.InlineKeyboardButton(text=genres[i-1], callback_data=genres[i-1]),
						 telebot.types.InlineKeyboardButton(text=genres[i], callback_data=genres[i]))

		bot.edit_message_text("Выбери жанр", message.chat.id, message.message_id, reply_markup=keyboard)
	if call.data == 'Год':
		keyboard = telebot.types.InlineKeyboardMarkup()
		for i in range(0, len(years)-1, 3):
			keyboard.add(telebot.types.InlineKeyboardButton(text=str(years[i]), callback_data=str(years[i])),
						 telebot.types.InlineKeyboardButton(text=str(years[i+1]), callback_data=str(years[i+1])),
						 telebot.types.InlineKeyboardButton(text=str(years[i+2]), callback_data=str(years[i+2])))
		bot.edit_message_text("Выбери год, если не нашел, введи вручную только число", message.chat.id, message.message_id, reply_markup=keyboard)

	if call.data == 'Описание':
		bot.send_message(message.chat.id, 'Напиши описание, я что-нибудь найду похожее')

	if call.data in genres:
		page = 1
		keyboard = position_btn(page, 'genre', call.data)
		bot.edit_message_text('Выбери фильм', message.chat.id, message.message_id, reply_markup=keyboard)

	if (call.data in years) and ('Назад' not in call.data):
		bot.send_message(message.chat.id, f'Ты выбрал {years[years.index(call.data)]}')
		page = 1
		keyboard = position_btn(page, 'year', call.data)
		bot.edit_message_text('Выбери фильм', message.chat.id, message.message_id, reply_markup=keyboard)

	if call.data == 'Код':
		bot.send_message(message.chat.id, 'Пришли код в формате "#000"')

	if 'Назад' in call.data:
		keyboard = orig_keyboard()
		bot.edit_message_text("Выбери параметр", message.chat.id, message.message_id, reply_markup=keyboard)

	if call.data[0] == '+':
		print(message.chat.id, group_chat_id, int(call.data[1::]))
		print(message)
		new_msg = 'Код: ' + call.data[1::] + '\n'
		bot.send_message(message.chat.id, new_msg)
		bot.copy_message(message.chat.id, group_chat_id, int(call.data[1::]))

	if call.data == '<---':
		page -= 1
		if page > 0:
			keyboard = position_btn(page)
			bot.edit_message_text("Выбери параметр", message.chat.id, message.message_id, reply_markup=keyboard)
		else:
			page = 1
			bot.send_message(message.chat.id, 'Харе')

	elif call.data == '--->':
		page += 1
		keyboard = position_btn(page)

		try:
			bot.edit_message_text("Выбери параметр", message.chat.id, message.message_id, reply_markup=keyboard)
		except:
			pass


@bot.message_handler(func=lambda message: True)
def work(message):
	flag = True
	print('M: ', message.text)

	if len(message.text) != 0:
		try:
			year = int(message.text)
			bot.send_message(message.chat.id, f'Ты выбрал {str(year)} год')
			page = 1
			keyboard = position_btn(page, 'year', str(year))
			bot.send_message(message.chat.id, 'Выбери фильм', reply_markup=keyboard)
			flag = False
		except:
			pass

		if flag and message.from_user.id != channel_id:
			res = []
			if message.text == 'Запуск бота':
				keyboard = orig_keyboard()
				bot.send_message(message.chat.id, "Выбери параметр", reply_markup=keyboard)
				return 0

			if '#' in message.text:
				print('@', message.text[1::])
				page = 1
				keyboard = position_btn(page, 'tg_id', message.text[1::])
				bot.send_message(message.chat.id, 'Выбери фильм', reply_markup=keyboard)

			if (len(message.text) >= 3) and (message.text != 'Запуск бота'):
				bot.reply_to(message, 'Ищу нечто похожее')
				res = sql_find.find('desc', str(message.text))
			else:
				bot.send_message(message.chat.id, 'Для поиска по описанию введи более трех символов')

			if (len(res) != 0) and (message.text != 'Запуск бота'):
				keyboard = telebot.types.InlineKeyboardMarkup()
				for i in range(0, len(res)):
					keyboard.add(telebot.types.InlineKeyboardButton(text=res[i][1], callback_data='+' + str(res[i][0])))
				bot.send_message(message.chat.id, 'Выбери фильм', reply_markup=keyboard)
				print(res)
			else:
				bot.send_message(message.chat.id, 'Увы, у меня пусто')


@bot.message_handler(content_types=['video'])
def send_text(message):
	print('V: ', message.caption)

	#from chanell
	if message.from_user.id == channel_id:
		# add to db
		print(message.caption)
		msg = message.caption.split('\n')
		print('NEW FILM')
		sql_find.add_post(int(message.id), msg[0], msg[1][5::], msg[2][6::], msg[3])


bot.polling()
