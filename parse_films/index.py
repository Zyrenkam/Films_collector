import chat_bot
import send_video
import os

while True:
    print('# -', chat_bot.sign)
    if len(chat_bot.sign) > 1:
        name = chat_bot.sign

        send_video.send_film(name, chat_bot.description, chat_bot.year, chat_bot.genre)
        chat_bot.sign = ''

        os.remove(str(name.replace(' ', '_') + '.mp4'))
        chat_bot.bot.polling()
