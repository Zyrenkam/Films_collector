from telethon import TelegramClient, events, sync
from telethon.tl.types import DocumentAttributeVideo


def send_film(name, desc, year, genre):
    links = {
        'фантастика': 'chanell_one',
        'ужасы': 'chanell_two',
        'комедия': 'chanell_one',
        'боевик': 'chanell_four',
        'драма': 'chanell_one',
        'приключения': 'chanell_six',
        'мультфильм': 'chanell_seven',
    }

    api_id = 0
    api_hash = ''

    client = TelegramClient('session_name', api_id, api_hash)
    client.start()

    print('start sending')
    caption = name + '\nГод: ' + year + '\nЖанр: ' + genre + '\n \n' + desc

    temp_genre = genre.split(', ')
    for i in range(0, len(temp_genre)):
        print('G', temp_genre[i])
        temp_genre[i] = temp_genre[i].replace(' ', '')
        if temp_genre[i] in links.keys():
            print('YES')
            msg_id = client.send_file(links[temp_genre[i]], str(name.replace(' ', '_') + '.mp4'),
                             attributes=(DocumentAttributeVideo(905, 1280, 720),), caption=caption).id
            print(msg_id)

        else:
            print('NO')
    print('finish sending')
    client.disconnect()
