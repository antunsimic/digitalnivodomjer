# -*- coding: utf-8 -*-
"""
Created on Mon May 13 01:17:41 2024

@author: antun_81f2caf
"""

from flask import Flask, request, render_template, send_file, jsonify, session
from bazaPodatakaFunct import upload_db, download_db, delete_db, vodomjeri_availability
from godisnjaPotrosnjaFunct import get_consumption, get_godine, get_korisnici, get_zgrade, get_filter_data
import atexit
import os
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = 'your_really_secret_key_here'
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SECURE'] = True  # Use if HTTPS is enabled
# treba spojit u file gdje su i ostale rute

# ruta koja obavlja upload slike er
@app.route('/upload', methods=['POST'])
def upload():
    return upload_db()
    
# ruta za download slike er
@app.route('/download', methods=['GET'])    
def download():
    return download_db()

# ruta za brisanje datoteke i slike er
@app.route('/delete', methods=['DELETE'])
def delete():
    return delete_db()

# ruta za provjeru dostupnosti baze podataka
@app.route('/database_availability')
def database_availability():
    return vodomjeri_availability()

# brisanje baze po isključivanju flask backenda
#atexit.register(delete_db)

@app.route('/check-login-status')
def check_login_status():
    # Assume `logged_in` is a key in the session that is True when the user is logged in
    return jsonify(logged_in=session.get('logged_in', False))



@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()  # Ensure you're correctly parsing JSON data
    print("Received data:", data)
    if session.get("logged_in"):
        return jsonify({'error': 'Already logged in'}), 400
    email = data.get('email')
    password = data.get('password')
    if not email or not password:
        return jsonify({'error': 'Email or password not entered'}), 400
    
    # For now, assume validation passes:
    session["email"] = email
    session["password"] = password
    session["logged_in"] = True
    return jsonify({'success': True, 'message': 'Login successful'})


    
@app.route('/logout')
def logout():
    if session.get("logged_in"):
        session.pop('logged_in', None)
        session.pop('email', None)  # Consider also cleaning up other session data.
        session.pop('password', None)
        return jsonify({'success': True, 'message': 'Logout successful'})
    else:
        return "Već ste odjavljeni"
    
# godisnja-potrosnja
#
# vraćanje zgrada(ulica, mjesto, id) za prikaz na izborniku frontend
@app.route('/get_zgrade', methods=['GET'])
def get_buildings():
    if session.get("logged_in") and session.get("uploaded_file"):
        return get_zgrade()
    else:
        print("Baza nije uploadana ili korisnik nije ulogiran")
# vraćanje korisnika(id, ime, prezime) za prikaz na izborniku frontend    
@app.route('/get_korisnici', methods=['GET'])
def get_users():
    if session.get("logged_in") and session.get("uploaded_file"):
        return get_korisnici()
    else:
        print("Baza nije uploadana ili korisnik nije ulogiran")
# vraćanje godina(dubstring prva 4 broja razdoblja) za prikaz na izborniku frontend
@app.route('/get_godine', methods=['GET'])
def get_years():
    if session.get("logged_in") and session.get("uploaded_file"):
        return get_godine()
    else:
        print("Baza nije uploadana ili korisnik nije ulogiran")
# kombinacija prethodne tri - odabrati koja opcija je bolja za frontend
@app.route('/get_filter', methods=['GET'])
def get_filters():
    if session.get("logged_in") and session.get("uploaded_file"):
        return get_filter_data()
    else:
        print("Baza nije uploadana ili korisnik nije ulogiran")
# vraćanje podataka dobivenih na         
@app.route('/potrosnja', methods=['GET'])
def get_consumption_data():
    if session.get("logged_in") and session.get("uploaded_file"):
        return get_consumption()
    else:
        print("Baza nije uploadana ili korisnik nije ulogiran")

if __name__ == '__main__':
    app.run(debug=True)
