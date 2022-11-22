import math # округление
import time
import sqlite3
import re # импортируем регулярные выражения
from flask import url_for

class FDataBase:
    def __init__(self, db): # db ссылка на связь с базой данных
        self.__db = db
        self.__cur = db.cursor() # через класс cursor мы работаем с таблицей базы данных

    def getMenu(self):
        sql = '''SELECT * FROM mainmenu'''
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            if res: return res
        except:
            print("Ошибка чтения из БД")
        return []

    def addPost(self, title, text, url):
        try:
            self.__cur.execute(f"SELECT COUNT() as 'count' FROM posts WHERE url LIKE '{url}'")
            res = self.__cur.fetchone()
            if res['count'] > 0:
                print('Статья с таким url уже существует')
                return False
            tm = math.floor(time.time())
            self.__cur.execute('INSERT INTO posts VALUES(NULL, ?, ?, ?, ?)', (title, text, url, tm))
            self.__db.commit() #commit сохраняет физически данные в базу данных
        except sqlite3.Error as e:
            print('Ошибка добавления статьи в БД'+str(e))
            return False

    def getPost(self, alias):
        try:
            self.__cur.execute(f"SELECT title, text FROM posts WHERE url LIKE '{alias}' LIMIT 1")
            res = self.__cur.fetchone()
            if res:
                base = url_for('static', filename='images_html')
                # base путь к каталогу с картинками
                text = re.sub(r"(?P<tag><img\s+[^>]*src=)(?P<quote>[\"'])(?P<url>.+?)(?P=quote)>","\\g<tag>" + base + "/\\g<url>>",res['text'])
                # регулярное выражение, чтобы составить полный путь к картинкам сайта
                return (res['title'], text)
        except sqlite3.Error as e:
            print('Ошибка получения статьи из БД' + str(e))

        return (False, False)

    def getPostAnonce(self): # возвращает список статей
        try:
            self.__cur.execute(f'SELECT id, title, text, url FROM posts ORDER BY time DESC')
            res = self.__cur.fetchall()
            if res: return res
        except sqlite3.Error as e:
            print('Ошибка получения статьи из БД' + str(e))

        return []

    def addUser(self, name, email, hpsw):
        try:
            self.__cur.execute(f"SELECT COUNT() as 'count' FROM users WHERE email LIKE '{email}'")
            res = self.__cur.fetchone()
            if res['count'] > 0:
                print('Пользователь с таким emqil уже существует')
                return False
            tm = math.floor(time.time()) # формируем время когда происходит регистрация пользователя
            self.__cur.execute('INSERT INTO users VALUES(NULL, ?, ?, ?, NULL, ?)', (name, email, hpsw, tm)) #добавляем в базу данных все поля
            self.__db.commit() #вызываем функцию commit, чтобы сохранить данные непосредственно в базу данных
        except sqlite3.Error as e:
            print('Ошибка добавления пользователя в БД'+str(e))
            return False

        return True

    def getUser(self, user_id):
        try:
            self.__cur.execute(f"SELECT * FROM users WHERE id = '{user_id}' LIMIT 1")
            res = self.__cur.fetchone()
            print('res =', res)
            if not res:
                print('Пользователь не найден')
                return False

            return res
        except sqlite3.Error as e:
            print('Ошибка получения данных из БД'+str(e))

        return False

    def getUserByEmail(self, email):
        try:

            self.__cur.execute(f"SELECT * FROM users WHERE email = '{email}' LIMIT 1")
            print(email)

            res = self.__cur.fetchone()

            print('res =', res)
            if not res:
                print('Пользователь не найден')
                return False

            return res
        except sqlite3.Error as e:
            print('Ошибка получения данных из БД'+str(e))

        return False

    def updateUserAvatar(self, avatar, user_id):
        if not avatar: #если аватра ничего не содержит то функция завершается
            return False

        try:
            binary = sqlite3.Binary(avatar) #превращаем объект в бинарный объект через специальный метод sqlite3
            self.__cur.execute(f'UPDATE users SET avatar = ? WHERE id = ?', (binary, user_id))
            #затем этот бинарный объект помещаем в БД
            self.__db.commit() #сохраняем изменения в БД
        except sqlite3.Error as e:
            print('Ошибка обновления аватара в БД', + str(e))
            return False
        return True