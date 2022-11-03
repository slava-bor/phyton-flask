import os.path
import sqlite3
import os
from flask import Flask, render_template, request, g, flash, abort
from FDataBase import FDataBase

# конфигурация
DATABASE = '/tmp/flsite.db'
DEBUG = True
SECRET_KEY ='dwhsej,.<>843h3nfjk8ek34,dlkwkei'

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(DATABASE=os.path.join(app.root_path, 'flsite.db')))

# menu = [{"name": "Установка", "url": "install-flask"},
#         {"name": "Первое приложение", "url": "first-app"},
#         {"name": "Обратная связь", "url": "contact"},
#         {"name": "Логин", "url": "login"}]


def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
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

@app.teardown_appcontext
def close_db(error):
    # Закрываем соединение с БД, если оно было установлено
    if hasattr(g, 'link_db'):
        g.link_db.close()

@app.route('/')
def index():
    db = get_db()
    dbase = FDataBase(db)
    return render_template('index.html', menu = dbase.getMenu())

@app.route('/add_post', methods=['POST', 'GET'])
def addPost():
    db = get_db()
    dbase = FDataBase(db)

    if request.method == 'POST':
        if len(request.form['name']) > 4 and len(request.form['post']) > 10:
            res = dbase.addPost(request.form['name'], request.form['post'])
            if not res:
                flash('Ошибка добавления статьи', category='error')
            else:
                flash('Статья добавлена успешно', category='success')
        else:
            flash('Ошибка добавления статьи', category='error')

    return render_template('add_post.html', menu = dbase.getMenu(), title='Добавление статьи')

if __name__ == "__main__":
    app.run(debug=True)