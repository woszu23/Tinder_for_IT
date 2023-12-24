from flask import Flask, render_template, request, redirect, url_for, session
import random

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Klucz sesji, ważne dla bezpieczeństwa sesji

# Symulacja bazy danych
users_db = []

# Strona główna
@app.route('/')
def home():
    return render_template('home.html')

# Rejestracja użytkownika
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Tutaj można dodać walidację danych

        # Tworzenie nowego użytkownika
        user = {
            'email': email,
            'password': password,
            'profile': {
                'interests': [],
                'portfolio': '',
                'bio': '',
                'skills': '',
                'age': '',
                'gender': '',
                'avatar': ''
            }
        }

        users_db.append(user)
        session['user'] = user  # Ustawienie sesji po udanej rejestracji
        return redirect(url_for('profile'))

    return render_template('register.html')

# Logowanie użytkownika
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Tutaj można dodać logikę autentykacji

        user = next((u for u in users_db if u['email'] == email and u['password'] == password), None)

        if user:
            session['user'] = user  # Ustawienie sesji po udanym logowaniu
            return redirect(url_for('profile'))
        else:
            return render_template('login.html', error='Nieprawidłowe dane logowania')

    return render_template('login.html')

# Profil użytkownika
@app.route('/profile')
def profile():
    user = session.get('user')

    if user:
        return render_template('profile.html', user=user)
    else:
        return redirect(url_for('home'))

# Przeglądanie profili
@app.route('/browse')
def browse():
    random_user = random.choice(users_db)
    return render_template('browse.html', user=random_user)

# Wylogowanie
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
