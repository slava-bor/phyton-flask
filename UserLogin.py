class UserLogin():
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