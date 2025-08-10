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


class DBQ:
    @staticmethod
    def select_one(sql, params=()):
        with Database('financial_tracker.db') as cur:
            cur.execute(sql, params)
            return cur.fetchone()  # tuple или None

    @staticmethod
    def select_all(sql, params=()):
        with Database('financial_tracker.db') as cur:
            cur.execute(sql, params)
            return cur.fetchall()  # list[tuple]

    @staticmethod
    def insert(sql, params=()):
        with Database('financial_tracker.db') as cur:
            cur.execute(sql, params)
            return cur.lastrowid

    @staticmethod
    def execute(sql, params=()):
        with Database('financial_tracker.db') as cur:
            cur.execute(sql, params)

class UserRepo:
    @staticmethod
    def get_by_email_password(email, password):
        return DBQ.select_one(
            'SELECT id, name, surname, email FROM user WHERE email=? AND password=?',
            (email, password)
        )

    @staticmethod
    def create(name, surname, email, password):
        return DBQ.insert(
            'INSERT INTO user (name, surname, email, password) VALUES (?, ?, ?, ?)',
            (name, surname, email, password)
        )

class IncomeRepo:
    @staticmethod
    def list_by_user(user_id):
        return DBQ.select_all(
            'SELECT id, amount, description FROM income WHERE user_id=? ORDER BY id DESC',
            (user_id,)
        )

    @staticmethod
    def add(user_id, amount, description=''):
        return DBQ.insert(
            'INSERT INTO income (user_id, amount, description) VALUES (?, ?, ?)',
            (user_id, amount, description)
        )

class SpendRepo:
    @staticmethod
    def list_by_user(user_id):
        return DBQ.select_all(
            'SELECT id, amount, description FROM spend WHERE user_id=? ORDER BY id DESC',
            (user_id,)
        )

    @staticmethod
    def add(user_id, amount, description=''):
        return DBQ.insert(
            'INSERT INTO spend (user_id, amount, description) VALUES (?, ?, ?)',
            (user_id, amount, description)
        )

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

    result = UserRepo.get_by_email_password(email, password)

    if result:
        session.clear()
        session['user_id'] = result[0]  # id
        session['user_email'] = result[3]  # email
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

    UserRepo.create(username, surname, email, password)

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
            amount_f = float(amount)
        except ValueError:
            return redirect(url_for('income_handler'))

        IncomeRepo.add(user_id, amount_f, description)
        return redirect(url_for('income_handler'))

    rows = IncomeRepo.list_by_user(user_id)
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
            amount_f = float(amount)
        except ValueError:
            return redirect(url_for('spend_handler'))

        SpendRepo.add(user_id, amount_f, description)
        return redirect(url_for('spend_handler'))

    rows = SpendRepo.list_by_user(user_id)
    return render_template('spend.html', items=rows, user_email=session['user_email'])


if __name__ == '__main__':
    app.run(debug=True)

@app.route('/category', methods=['GET', 'POST'])
def category_handler():
    if request.method == 'GET':
        return "HELLO GET"
    else:
        return "HELLO POST"

@app.route('/category/<category_id>', methods=['GET', 'POST'])
def category_id_handler(category_id):
    if request.method == 'GET':
        return render_template('category_id.html')
    else:
        method_from_form=request.form['request_method']
        if method_from_form =='DELETE':
            ...
        elif method_from_form== 'PATCH':
            ...
        else:
            "error"

if __name__ == '__main__':
    app.run()