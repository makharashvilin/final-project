from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import os
from init_db import init_db
from ppl_db import ppl_db
from datetime import timedelta
app = Flask(__name__)
app.secret_key = 'grisha'
DATABASE = 'database.db'
app.permanent_session_lifetime = timedelta(minutes=20)


class User:
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def register(self):
        try:
            conn = sqlite3.connect(DATABASE)
            cursor = conn.cursor()
            cursor.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)', (self.username, self.email, self.password))
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            return False

    def login(self):
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('SELECT password FROM users WHERE email = ?', (self.email,))
        record = cursor.fetchone()
        conn.close()
        if record and record[0] == self.password:
            return True
        return False


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        user = User(username, email, password)
        if user.register():
            flash('Registration successful! You can now login.')
            return redirect(url_for('login'))
        else:
            flash('Username already exists.')
    return render_template('register.html')


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('SELECT username FROM users WHERE email = ?', (email,))
        username = cursor.fetchone()
        conn.close()
        user = User(username, email, password)
        if user.login():
            session['username'] = username
            return render_template('home.html', user=username)
        else:
            flash('Invalid credentials')
    return render_template('login.html')


@app.route('/home')
def home():
    if 'username' in session:
        username = session['username']
        return render_template('home.html', user=username)
    return redirect(url_for('login'))


def getdata():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM xixia")
    data = cursor.fetchall()
    conn.close()
    return data


@app.route("/add", methods=['POST', 'GET'])
def add():
    if 'username' in session:
        if request.method == 'POST':
            conn = sqlite3.connect(DATABASE)
            cursor = conn.cursor()
            name = request.form['name']
            surname = request.form['surname']
            rating = request.form['rating']
            comment = request.form['comment']
            cursor.execute('SELECT * FROM xixia WHERE name=? AND surname=? AND rating=? AND comment=?',
                           (name, surname, rating, comment))
            rpt = cursor.fetchone()
            if rpt is None:
                cursor.execute('INSERT INTO xixia (name, surname, rating, comment) VALUES (?, ?, ?, ?)',
                               (name, surname, rating, comment))
                conn.commit()
            conn.close()
            return redirect(url_for('shavisia'))
        return render_template('add.html')
    return render_template('login.html')


@app.route("/shavisia")
def shavisia():
    if 'username' in session:
        data = getdata()
        return render_template('shavisia.html', data=data)
    return render_template('login.html')


@app.route("/edit/<int:id>", methods=['POST', 'GET'])
def edit(id):
    if 'username' in session:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        if request.method == 'POST':
            name = request.form['name']
            surname = request.form['surname']
            rating = request.form['rating']
            comment = request.form['comment']
            cursor.execute('UPDATE xixia SET name=?, surname=?, rating=?, comment=? WHERE id=?',
                           (name, surname, rating, comment, id))
            conn.commit()
            conn.close()
            return redirect(url_for('shavisia'))
        else:
            cursor.execute('SELECT * FROM xixia WHERE id=?', (id,))
            data = cursor.fetchone()
            conn.close()
            return render_template('edit.html', data=data)
    return render_template('login.html')


@app.route("/delete/<int:id>")
def delete(id):
    if 'username' in session:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM xixia WHERE id=?', (id,))
        conn.commit()
        conn.close()
        return redirect(url_for('shavisia'))
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))


if __name__ == '__main__':
    if not os.path.exists(DATABASE):
        init_db()
        ppl_db()
    app.run(debug=True)

