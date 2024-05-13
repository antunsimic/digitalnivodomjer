# -*- coding: utf-8 -*-
"""
Created on Mon May 13 01:17:41 2024

@author: antun_81f2caf
"""

from flask import Flask, request, render_template, send_file, jsonify
from bazaPodatakaFunct import upload_db, download_db, delete_db, vodomjeri_availability
import atexit
import os

app = Flask(__name__)

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
atexit.register(delete_db)


def create_file(email, password):
    file_path = 'podaci.txt'
    with open(file_path, 'w') as f:
        f.write(f"{email}\n{password}")

def delete_file():
    file_path = 'podaci.txt'
    if os.path.exists(file_path):
        os.remove(file_path)


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    create_file(email, password)
    return jsonify({'success': True, 'message': 'Login successful'})
    
@app.route('/logout')
def logout():
    delete_file()
    return jsonify({'success': True, 'message': 'Logout successful'})

if __name__ == '__main__':
    app.run(debug=True)
