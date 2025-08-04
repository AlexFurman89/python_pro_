from flask import Flask, request, render_template
import sqlite3

app = Flask(__name__)

class Database:
    def __init__(self, db_name):
        self.db_name = db_name
        print(f"Initializing Database with {db_name}")

    def __enter__(self):
        try:
            print(f"Attempting to connect to {self.db_name}")
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()
            print("Connection established successfully")
            return self.cursor
        except Exception as e:
            print(f"Error connecting to database: {e}")
            raise

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            print("Committing changes and closing connection")
            self.conn.commit()
            self.conn.close()
            print("Connection closed successfully")
        except Exception as e:
            print(f"Error closing database connection: {e}")
            raise


@app.route('/user', methods=['GET', 'DELETE'])
def user_handler():
    connector= sqlite3.connect("financial_tracker.db")
    cursor=connector.cursor()

    if request.method == 'GET':
        connector.commit()
        connector.close()
        return ("HELLO GET")
    else:
        connector.commit()
        connector.close()

        return "HELLO DELETE"

@app.route('/login', methods=['GET', 'POST'])
def user_login_handler():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        email=request.form['email']
        password=request.form['password']
        with Database('financial_tracker.db') as cursor:
            result = cursor.execute('SELECT * FROM user WHERE name=? AND password=?', (email, password))
            result=result.fetchone()
        return f"HELLO POST {email}{password}"


@app.route('/register', methods=['GET', 'POST'])
def user_register_handler():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        try:
            username = request.form['username']
            surname = request.form['surname']
            email = request.form['email']
            password = request.form['password']

            print(f"Attempting to register user: {username}")

            with Database('financial_tracker.db') as cursor:
                cursor.execute('INSERT INTO user (name, surname, email, password) VALUES (?, ?, ?, ?)',
                               (username, surname, email, password))

            print(f"User {username} registered successfully")

            return f"User registered: {username}"
        except Exception as e:
            print(f"Error during registration: {e}")
            return f"Registration failed: {str(e)}", 400

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

@app.route('/income', methods=['GET', 'POST'])
def income_handler():
    if request.method == 'GET':
        return "HELLO GET"
    else:
        return "HELLO POST"

@app.route('/income/<income_id>', methods=['GET', 'PATCH', 'DELETE'])
def income_id_handler(income_id):
    if request.method == 'GET':
        return "HELLO GET"
    elif request.method == 'PATCH':
        return "HELLO PATCH"
    else:
        return "HELLO DELETE"

@app.route('/spend', methods=['GET', 'POST'])
def spend_handler():
    if request.method == 'GET':
        return "HELLO GET"
    else:
        return "HELLO POST"

@app.route('/spend/<spend_id>', methods=['GET', 'PATCH', 'DELETE'])
def spend_id_handler(spend_id):
    if request.method == 'GET':
        return "HELLO GET"
    elif request.method == 'PATCH':
        return "HELLO PATCH"
    else:
        return "HELLO DELETE"

if __name__ == '__main__':
    app.run()