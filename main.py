from flask import Flask, render_template, request, url_for, flash, session, redirect, abort

app = Flask(__name__)
app.config['SECRET_KEY'] = 'fdgdfgdfggf786hfg6hfg6h7f'


menu = [{"name": "Установка", "url": "install-flask"},
        {"name": "Первое приложение", "url": "first-app"},
        {"name": "Обратная связь", "url": "contact"},
        {"name": "Логин", "url": "login"}]

@app.route("/")
def index():
    print(url_for('index'))
    return render_template('index.html', menu=menu)

@app.route("/about")
def about():
    print(url_for('about'))
    return render_template('about.html', title="О нашем сайте", menu=menu)

@app.route("/contact", methods=['POST', 'GET'])
def contact():
    x = 0;
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
    return render_template('contact.html', title="Обратная связь", menu=menu)

@app.route("/login", methods=["POST", "GET"])
def login():
    if 'userLogged' in session:
        return redirect(url_for('profile', username=session['userLogged']))
    elif request.method == 'POST' and request.form['username'] == "selfedu" and request.form['psw'] == "123":
        session['userLogged'] = request.form['username']
        return redirect(url_for('profile', username=session['userLogged']))

    return render_template('login.html', title="Авторизация", menu=menu)

@app.route("/base")
def base():
    print(url_for('base'))
    return render_template('base.html', title="О базе Flask", menu=menu)

@app.errorhandler(404)
def pageNotFount(error):
    return render_template('page404.html', title="Страница не найдена", menu=menu)

@app.errorhandler(401)
def pageNotFount(error):
    return render_template('page401.html', title="Не авторизованный пользователь", menu=menu)

@app.route("/profile/<username>")
def profile(username):
    if 'userLogged' not in session or session['userLogged'] != username:
        abort(401)
    return f"Пользователь: {username}"

if __name__ == "__main__":
    app.run(debug=True)