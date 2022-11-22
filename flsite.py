import os.path
import sqlite3
import os
from flask import Flask, render_template, request, g, flash, make_response, abort, redirect, url_for
from FDataBase import FDataBase
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from UserLogin import UserLogin
from forms import LoginForm

# конфигурация
DATABASE = '/tmp/flsite.db' # путь к базе данных
DEBUG = True # устанавливает режим отладки
SECRET_KEY ='dwhsej,.<>843h3nfjk8ek34,dlkwkei'
MAX_CONTENT_LENGTH = 1024 * 1024 #размер файла аватарки которую можно загружать на сервер 1Мб

app = Flask(__name__) # создаем приложение Flask
app.config.from_object(__name__) # через метод from.object загружаем нашу конфигурацию, name значит кофигурацию берем из этого файла

# переопределяем путь к базе данных через свойство root_path, который ссылается на текущий рабочий каталог
# app.root_path, 'flsite.db' так мы формируем полный путь к нашей базе данных
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'flsite.db')))

login_manager = LoginManager(app) # создаем экземпляр класса LoginManager и связываем его с нашим преложением app

@login_manager.user_loader
def load_user(user_id):
    print('load_user')
    return UserLogin().fromDB(user_id, dbase)

# menu = [{"name": "Установка", "url": "install-flask"},
#         {"name": "Первое приложение", "url": "first-app"},
#         {"name": "Обратная связь", "url": "contact"},
#         {"name": "Логин", "url": "login"}]

# общая функция для соединения с базой данных
def connect_db():
    conn = sqlite3.connect(app.config['DATABASE']) # методом connect, говорим где находится наша база данных, в нашей случае мы её берём из данной конфигурации нашего приложения
    conn.row_factory = sqlite3.Row # это чтобы база данных бала представлена не виде картеджей, а ввиде словаря
    return conn

def create_db():
    # Вспомогательная функция для создания таблицы БД
    db = connect_db()
    with app.open_resource('sq_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()

def get_db():
    # соединение с БД, если оно еще не установлено
    if not hasattr(g,'link_db'):
        g.link_db = connect_db()
    return g.link_db

dbase = None
@app.before_request
def before_request():
    """ Установление соединения с БД перед выполнением запроса"""
    global dbase
    db = get_db()
    dbase = FDataBase(db)

@app.teardown_appcontext
def close_db(error):
    # Закрываем соединение с БД, если оно было установлено
    if hasattr(g, 'link_db'):
        g.link_db.close()

@app.route('/')
def index():
    # db = get_db()
    # dbase = FDataBase(db)

    # content = render_template('index.html', menu=dbase.getMenu(), posts=dbase.getPostAnonce())
    # res = make_response(content)
    # res = make_response('<h1>Ошибка сервера</h1>', 500)
    # res.headers['Content-Type'] = 'text/plain' # теперь страница отображается просто как текст, а не как hrml страница
    # res.headers['Server'] = 'flasksite'
    # return res

    return render_template('index.html', menu=dbase.getMenu(), posts=dbase.getPostAnonce()) # menu ссылка на коллекция get.Menu

@app.route("/contact", methods=['POST', 'GET'])
def contact():
    # db = get_db()
    # dbase = FDataBase(db)
    x = 0
    if request.method == 'POST':
        if (len(request.form['username']) < 2):
            x = x + 1
            flash('Ошибка имени пользователя', category='error')
        if (len(request.form['email']) < 2):
            x = x + 1
            flash('Ошибка почты пользователя', category='error')
        if x == 0:
            flash('Сообщение отправлено', category='success')

        # print(request.form['username'])
    return render_template('contact.html', title="Обратная связь", menu=dbase.getMenu())

@app.route('/add_post', methods=['POST', 'GET'])
def addPost():
    # db = get_db()
    # dbase = FDataBase(db)
    if request.method == 'POST': # если данные от формы пришли
        if len(request.form['name']) > 4 and len(request.form['post']) > 10:
            res = dbase.addPost(request.form['name'], request.form['post'], request.form['url'])
            if not res:
            #     flash('Ошибка добавления статьи', category='error')
            # else:
                flash('Статья добавлена успешно', category='success')
        else:
            flash('Ошибка добавления статьи в конце', category='error')
    return render_template('add_post.html', menu=dbase.getMenu(), title='Добавление статьи')

# @app.route('/post/<int:id_post>')
# def showPost(id_post):
#     db = get_db()
#     dbase = FDataBase(db)
#     title, text, time = dbase.getPost(id_post)
#     if not title:
#         abort(404)
#
#     return render_template('post.html', menu=dbase.getMenu(), title=title, post=text)

@app.route("/post/<alias>")
@login_required #этот декоратор дает доступ к статьям только авторизованным пользователям
def showPost(alias):
    # db = get_db()
    # dbase = FDataBase(db)
    title, text = dbase.getPost(alias)
    if not title:
        abort(404)

    return render_template('post.html', menu=dbase.getMenu(), title=title, post=text)

@app.errorhandler(404)
def pageNot(error):
    return ('Страница не найдена', 404)

@app.route("/login", methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))

    form = LoginForm() #создаем экземпляр класса LoginForm
    if form.validate_on_submit(): #проверяем, а были ли отправлены данные методом POST запроса
        #и еще проверяет правильно ли заполнены поля, которые мы проверяем validatos в forms.py
         user = dbase.getUserByEmail(form.email.data)  # берем данные пользователя из бд по email
         if user and check_password_hash(user['psw'], form.psw.data): # если данные о user были получены и пароли совпадают
             userLogin = UserLogin().create(user) # создаем экземпляр класса UserLogin и передаем ему всю информацию о пользователе user
         rm = form.remember.data #определяем была ли поставлена птичка Запомнить меня
         login_user(userLogin, remember=rm) # и авторизуем пользователя с помощью функции специальной функции login_user (надо её импортировать)
         return redirect(request.args.get('next') or url_for('profile')) # если всё ОК то перенаправляем на profile

    flash('Неверная пара логин/пароль', 'error')

    return  render_template('login.html', menu=dbase.getMenu(), title='Авторизация', form=form) #далее в login.html мы переадем ссылку на экземпляр класса form



    # if request.method == 'POST':
    #     user = dbase.getUserByEmail(request.form['email']) #берем данные пользователя из бд по email
    #     if user and check_password_hash(user['psw'], request.form['psw']): # если данные о user были получены и пароли совпадают
    #         userLogin = UserLogin().create(user) # создаем экземпляр класса UserLogin и передаем ему всю информацию о пользователе user
    #         rm = True if request.form.get('remainme') else False #определяем была ли поставлена птичка Запомнить меня
    #         login_user(userLogin, remember=rm) # и авторизуем пользователя с помощью функции специальной функции login_user (надо её импортировать)
    #         return redirect(url_for('profile')) # если всё ОК то перенаправляем на profile
    #
    #     flash('Неверная пара логин/пароль', 'error')
    #
    # return render_template('login.html', menu=dbase.getMenu(), title="Авторизация")

@app.route("/register", methods=['POST', 'GET'])
def register():
    if request.method == 'POST':  # если данные от формы пришли
        if len(request.form['name']) > 4 and len(request.form['email']) > 4 \
            and len(request.form['psw']) > 4 and request.form['psw'] == request.form['psw2']:
            hash = generate_password_hash(request.form['psw'])
            res = dbase.addUser(request.form['name'], request.form['email'], hash)
            if res:
                flash('Вы успешно зарегистрированы', 'success')
                return redirect(url_for('login'))
            else:
                flash('Ошибка при добавление в БД', 'error')
        else:
            if request.form['psw'] != request.form['psw2']:
                flash('Пароли не совпадают', 'error')
            else:
                flash('Неверно зполнены поля', 'error')

    return render_template('register.html', menu=dbase.getMenu(), title="Регистрация")

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли из аккаунта', 'success')
    return redirect(url_for('login'))

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', menu=dbase.getMenu(), title='Профиль')

@app.route('/userava')
@login_required
def userava():
    img = current_user.getAvatar(app)
    if not img:
        return ''

    h = make_response(img)
    h.headers['Content-Type'] = 'image/png'
    return h

@app.route('/upload', methods=['POST', 'GET'])
@login_required #только для зарегистрированных пользователей
def upload():
    if request.method == 'POST': #проверяем что пришли данные по методу POST
        file = request.files['file'] #если данные пришли, то берем поле file из объекта request
        #которое асоцииноравно с загруженным на сервер файлом, т.е. тем файлом который был выбран в profile Пользователя
        if file and current_user.verifyExt(file.filename): #далее идет проверка, что file был успешно загружен
            # и его расширение png. Проверка происходит с помощью написанного метода verifyExt в UserLogin
            try:
                img = file.read() #дале читаем file, если мы его прочитали то затем, вызываем метод updateUser Avatar
                #в котором происходит изменение аватара пользователя в базе данных, это метод мы пропишем сами в FDataBase
                res = dbase.updateUserAvatar(img, current_user.get_id())
                if not res:
                    flash('Ошибка обновления аватара', 'error')
                flash('Аватар обновлен', 'success')
            except FileNotFoundError as e:
                flash('Ошибка чтения файла', 'error')
        else:
            flash('Ошибка обновления аватара', 'error')

    return redirect(url_for('profile'))

if __name__ == "__main__":
    app.run(debug=True)