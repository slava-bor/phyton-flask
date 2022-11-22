from flask_login import UserMixin
from flask import url_for

class UserLogin(UserMixin):
    def fromDB(self, user_id, db):
        self.__user = db.getUser(user_id) # формируем свойство user через которое потом узнаем id
        return self

    def create(self, user):
        self.__user = user
        return self

    def is_authenticated(self):
        # функция проверки авторизации пользователя:
        # (True - если авторизован, False -- если не авторизован)
        return True

    def is_active(self):
        # функция проверки что пользователь активен:
        # (True, False)
        return True

    def is_anonymous(self):
        # функция определяет неавторизованных пользователей:
        # (True - если неавторизован, False -- авторизован)
        return False

    def get_id(self):
        # функция возвращает уникальный идентификатор:
        # (индентификатор должен быть представлен в виде unicode строки)
        return str(self.__user['id'])

    def getName(self):
        return self.__user['name'] if self.__user else 'Без имени'

    def getEmail(self):
        return self.__user['email'] if self.__user else 'Без email'

    def getAvatar(self, app):
        img = None
        if not self.__user['avatar']:
            try:
                with app.open_resourse(app.root_path + url_for('static', filename='images/default.png'), 'rb') as f:
                    # загружаем аватарку в бинарном режиме
                    img = f.read()
                    print(img)
            except FileNotFoundError as e:
                print('Не найден аватар по умолчанию: ', +str(e))
        else:
            img = self.__user['avatar']

        return img

    def verifyExt(self, filename):
        ext = filename.rsplit('.', 1)[1] #получаем данные и делим с конца до точки и смотрим какой получился остаток
        if ext == 'png' or ext =='PNG':
            return True
        return False