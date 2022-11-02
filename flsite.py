import os.path
import sqlite3
import os
from flask import Flask, render_template, request, g

# конфигурация
DATABASE = '/tmp/flsite.db'
DEBUG = True
SECRET_KEY ='dwhsej,.<>843h3nfjk8ek34,dlkwkei'

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(DATABASE=os.path.join(app.root_path, 'flsite.db')))

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

@app.route('/')
def index():
    db = get_db()
    return render_template('index.html', menu = [])

@app.teardown_appcontext
def close_db(error):
    # Закрываем соединение с БД, если оно было установлено
    if hasattr(g, 'link_db'):
        g.link_db.close()


if __name__ == "__main__":
    app.run(debug=True)