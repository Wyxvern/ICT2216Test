from flask import Flask, render_template, request, redirect, url_for
import re

app = Flask(__name__)

COMMON_PASSWORDS_FILE = '10-million-password-list-top-1000.txt'

def load_common_passwords(file_path):
    with open(file_path) as file:
        return set(line.strip() for line in file)

COMMON_PASSWORDS = load_common_passwords(COMMON_PASSWORDS_FILE)

def is_password_strong(password):
    if password in COMMON_PASSWORDS:
        return False
    if len(password) < 8:
        return False
    if not re.search(r'[A-Z]', password):
        return False
    if not re.search(r'[a-z]', password):
        return False
    if not re.search(r'[0-9]', password):
        return False
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False
    return True

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        password = request.form['password']
        if is_password_strong(password):
            return redirect(url_for('welcome', password=password))
    return render_template('home.html')

@app.route('/welcome')
def welcome():
    password = request.args.get('password', '')
    return render_template('welcome.html', password=password)

@app.route('/logout')
def logout():
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
