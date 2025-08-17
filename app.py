from flask import Flask, request, render_template, session, redirect, url_for
from repos import UserRepo, IncomeRepo, SpendRepo

app = Flask(__name__)
app.secret_key = 'your_secret_key'

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
        session['user_id'] = result[0]
        session['user_email'] = result[3]
        return redirect(url_for('index'))
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