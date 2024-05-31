from flask import Flask, request, render_template, send_file, jsonify, session
from bazaPodatakaFunct import upload_db, download_db, delete_db, vodomjeri_availability
import atexit
import os
from flask_cors import CORS
from werkzeug.utils import secure_filename
from bankovni_izvodi import ucitavanje_izvoda
from ApatorMaddalena import ocitanja_vodomjera
from godisnjaPotrosnjaFunct import get_consumption, get_godine, get_korisnici, get_zgrade, get_filter_data
from izracunObracuna import izracunObracuna
from python_google_gmail import send_email, send_both_mails
from python_google_gmail import send_reports_for_zgrade

app = Flask(__name__)
CORS(app, supports_credentials=True)  # Allow credentials for cross-origin requests
app.secret_key = 'your_really_secret_key_here'
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SECURE'] = True  # Use if HTTPS is enabled




UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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
@app.route('/database-availability')
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


@app.route('/upload-izvjestaj', methods=['POST'])
def upload_izvjestaj():

    if 'files' not in request.files:
        return 'No file part', 400
    
    files = request.files.getlist('files')
    for file in files:
        filename = secure_filename(file.filename)
        file_ext = filename.split('.')[-1].lower()
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

    ###unosi u bazu podataka
    ucitavanje_izvoda()
    if ocitanja_vodomjera():
        izracunObracuna()
    ###/unosi u bazu podataka

    #brisu se sve datoteke iz 'uploads' foldera
    uploads_dir = os.path.join(os.path.dirname(__file__), 'uploads')
    uploads_dir = os.path.abspath(uploads_dir)

    if os.path.exists(uploads_dir):
        for filename in os.listdir(uploads_dir):
            file_path = os.path.join(uploads_dir, filename)
            os.unlink(file_path)

    return 'Files successfully uploaded', 200


# godisnja-potrosnja
#
# vraćanje zgrada(ulica, mjesto, id) za prikaz na izborniku frontend
@app.route('/get_zgrade', methods=['GET'])
def get_buildings():
    if  session.get("uploaded_file"):
        return get_zgrade()
    else:
        return jsonify({'error': 'Baza nije uploadana ili korisnik nije ulogiran'})
        
# vraćanje korisnika(id, ime, prezime) za prikaz na izborniku frontend   OVISI O BUILDING 
@app.route('/get_korisnici', methods=['GET'])
def get_users():
    if  session.get("uploaded_file"):
        return get_korisnici()
    else:
        return jsonify({'error': 'Baza nije uploadana ili korisnik nije ulogiran'})
        
# vraćanje godina(dubstring prva 4 broja razdoblja) za prikaz na izborniku frontend    OVISI O KORISNIKU
@app.route('/get_godine', methods=['GET'])
def get_years():
    if  session.get("uploaded_file"):
        return get_godine()
    else:
        return jsonify({'error': 'Baza nije uploadana ili korisnik nije ulogiran'})
        
# kombinacija prethodne tri - odabrati koja opcija je bolja za frontend
@app.route('/get_filter', methods=['GET'])
def get_filters():
    if session.get("uploaded_file"):
        # vraca u formatu buildings, users, years
        # buildings ima building[0](id) [1](ulica) [2](mjesto) za svaki building po buildings
        # users ima user[0](id) [1](ime) [2](prezime)
        # years ima samo godine
        # Kao zaasebne rute ali bez ograničenja
        return get_filter_data()
    else:
        return jsonify({'error': 'Baza nije uploadana ili korisnik nije ulogiran'})
        
# vraćanje podataka dobivenih na temelju filtara za umetanje u graf
@app.route('/potrosnja', methods=['GET'])
def get_consumption_data():
    if session.get("uploaded_file"):
        # vraca result sa row po resultu: [0](datum) [1](potrosnja)
        return get_consumption()
    else:
        return jsonify({'error': 'Baza nije uploadana ili korisnik nije ulogiran'})

@app.route('/reports', methods=['GET'])
def get_reports():
    if session.get("uploaded_file"):
        try:
            files_vodovod = os.listdir('izvjestaji/vodovod')
            files_zgrade = os.listdir('izvjestaji/zgrade')
            files = files_vodovod + files_zgrade
            #return jsonify({
            #    'vodovod_reports': files_vodovod,
            #    'zgrade_reports': files_zgrade
            #})
            return jsonify(files)
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': 'Baza podataka nije uploadana'})

@app.route('/send_emails')
def get_slanje():
        return send_reports_for_zgrade()
        #return send_both_mails()
if __name__ == '__main__':
    app.run(debug=True)

