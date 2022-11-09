import os.path
import sqlite3
import os
from flask import Flask, render_template, request, g, flash, make_response, abort
from FDataBase import FDataBase

# конфигурация
DATABASE = '/tmp/flsite.db' # путь к базе данных
DEBUG = True # устанавливает режим отладки
SECRET_KEY ='dwhsej,.<>843h3nfjk8ek34,dlkwkei'

app = Flask(__name__) # создаем приложение Flask
app.config.from_object(__name__) # через метод from.object загружаем нашу конфигурацию, name значит кофигурацию берем из этого файла

# переопределяем путь к базе данных через свойство root_path, который ссылается на текущий рабочий каталог
# app.root_path, 'flsite.db' так мы формируем полный путь к нашей базе данных
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'flsite.db')))

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

@app.route("/login")
def login():
    return render_template('login.html', menu=dbase.getMenu(), title="Авторизация")

@app.route("/register")
def register():
    return render_template('register.html', menu=dbase.getMenu(), title="Регистрация")


if __name__ == "__main__":
    app.run(debug=True)