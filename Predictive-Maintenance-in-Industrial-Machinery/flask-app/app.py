from flask import Flask, render_template, request, redirect, url_for, flash, session, send_file
from werkzeug.security import generate_password_hash, check_password_hash
from ml_model import ml_function
import pandas as pd

app = Flask(__name__)
app.secret_key = 'this is my secret key'

users = {
    'user1': {
        'username': 'user1',
        'password_hash': generate_password_hash('password1'),
    },
    'user2': {
        'username': 'user2',
        'password_hash': generate_password_hash('password2'),
    },
}

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/machine', methods=['POST', 'GET'])
def machine():
    if request.method == 'POST' and 'file' in request.files:
        f = request.files['file']
        if f:
            f.save('uploaded/input.csv')
            print(f)

            df = pd.read_csv('uploaded/input.csv')
            failear_df = ml_function(df)
            if len(failear_df) > 5:
                failear_df = failear_df.iloc[:5]
            failear_df.to_csv('uploaded/sample_failear_report.csv', index=False)

            return send_file('uploaded/sample_failear_report.csv', 
                         as_attachment=True, 
                         download_name='sample_failear_report.csv')
        else:
            print('No file uploaded')
    else:
        print('No files or no post method')
    return render_template('machine.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users:
            flash('Username already exists. Please choose another.', 'danger')
        else:
            users[username] = {
                'username': username,
                'password_hash': generate_password_hash(password),
            }
            flash('Registration successful. You can now log in.', 'success')
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = users.get(username)
        if user and check_password_hash(user['password_hash'], password):
            session['user'] = user['username']
            flash('Login successful', 'success')
            return redirect(url_for('profile'))
        else:
            flash('Login failed. Please check your username and password.', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('You have been logged out', 'success')
    return redirect(url_for('login'))

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'user' in session:
        if request.method == 'POST' and 'file' in request.files:
            f = request.files['file']
            if f:
                f.save('uploaded/input.csv')
                print(f)

                df = pd.read_csv('uploaded/input.csv')
                failear_df = ml_function(df)
                failear_df.to_csv('uploaded/failear_report.csv', index=False)

                return send_file('uploaded/failear_report.csv', 
                            as_attachment=True, 
                            download_name='failear_report.csv')
            else:
                print('No file uploaded')
        else:
            print('No files or no post method')
        return render_template('profile.html')
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
