from flask import Flask, request, render_template, send_file, jsonify
from bazaPodatakaFunct import upload_db, download_db, delete_db, vodomjeri_availability
import atexit

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

if __name__ == '__main__':
    delete_db() #delete database on app start
    app.run()
