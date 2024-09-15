import sqlite3

connection = sqlite3.connect('../db.db', check_same_thread=False)
cursor = connection.cursor()


def find(par, val):
    result = []
    index = {'tg_id': 0, 'name': 1, 'year': 2, 'genre': 3, 'desc': 4}

    cursor.execute("""SELECT * from Posts""")
    records = cursor.fetchall()
    for row in records:
        if val.lower() in row[index[par]].lower():
            result.append(row)

    return result


def add_post(tg_id, name, year, genre, desc):
    cursor.execute('INSERT INTO Posts (tg_id, name, year, genre, desc) VALUES (?, ?, ?, ?, ?)',
                   (tg_id, name, year, genre, desc))
    print('Note added')
    connection.commit()


def close_con():
    connection.close()
