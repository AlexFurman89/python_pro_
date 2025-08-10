from flask import Flask, request, render_template, session, redirect, url_for
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class Database:
    def __init__(self, db_name):
        self.db_name = db_name

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.commit()
        self.conn.close()


@app.route('/')
def index():
    if 'user_id' in session:
        return render_template('index.html', user_email=session['user_email'])
    return redirect(url_for('user_login_handler'))


@app.route('/login', methods=['GET', 'POST'])
def user_login_handler():
    if request.method == 'GET':
        return render_template('login.html')

    email = request.form.get('email', '')
    password = request.form.get('password', '')

    with Database('financial_tracker.db') as cursor:
        cursor.execute(
            'SELECT id, name, surname, email FROM user WHERE email=? AND password=?',
            (email, password)
        )
        result = cursor.fetchone()

    if result:
        session.clear()
        session['user_id'] = result[0]
        session['user_email'] = result[3]
        return redirect(url_for('index'))
    else:
        return "Invalid credentials", 401


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('user_login_handler'))


@app.route('/register', methods=['GET', 'POST'])
def user_register_handler():
    if request.method == 'GET':
        return render_template('register.html')

    username = request.form.get('username', '')
    surname  = request.form.get('surname', '')
    email    = request.form.get('email', '')
    password = request.form.get('password', '')

    if not username or not surname or not email or not password:
        return "All fields are required", 400

    with Database('financial_tracker.db') as cursor:
        cursor.execute(
            'INSERT INTO user (name, surname, email, password) VALUES (?, ?, ?, ?)',
            (username, surname, email, password)
        )

    return redirect(url_for('user_login_handler'))


@app.route('/income', methods=['GET', 'POST'])
def income_handler():
    if 'user_id' not in session:
        return redirect(url_for('user_login_handler'))

    user_id = session['user_id']

    if request.method == 'POST':
        amount = request.form.get('amount')
        description = request.form.get('description', '')

        if not amount:
            return redirect(url_for('income_handler'))
        try:
            float(amount)
        except ValueError:
            return redirect(url_for('income_handler'))

        with Database('financial_tracker.db') as cursor:
            cursor.execute(
                'INSERT INTO income (user_id, amount, description) VALUES (?, ?, ?)',
                (user_id, amount, description)
            )
        return redirect(url_for('income_handler'))

    with Database('financial_tracker.db') as cursor:
        cursor.execute(
            'SELECT id, amount, description FROM income WHERE user_id=? ORDER BY id DESC',
            (user_id,)
        )
        rows = cursor.fetchall()

    return render_template('income.html', items=rows, user_email=session['user_email'])


@app.route('/spend', methods=['GET', 'POST'])
def spend_handler():
    if 'user_id' not in session:
        return redirect(url_for('user_login_handler'))

    user_id = session['user_id']

    if request.method == 'POST':
        amount = request.form.get('amount')
        description = request.form.get('description', '')

        if not amount:
            return redirect(url_for('spend_handler'))
        try:
            float(amount)
        except ValueError:
            return redirect(url_for('spend_handler'))

        with Database('financial_tracker.db') as cursor:
            cursor.execute(
                'INSERT INTO spend (user_id, amount, description) VALUES (?, ?, ?)',
                (user_id, amount, description)
            )
        return redirect(url_for('spend_handler'))

    with Database('financial_tracker.db') as cursor:
        cursor.execute(
            'SELECT id, amount, description FROM spend WHERE user_id=? ORDER BY id DESC',
            (user_id,)
        )
        rows = cursor.fetchall()

    return render_template('spend.html', items=rows, user_email=session['user_email'])


if __name__ == '__main__':
    app.run()