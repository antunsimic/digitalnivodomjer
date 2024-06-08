# Datoteka s funkcijama vezanim za upload, download, i deletion baze podatakaS
from flask import request, jsonify, send_file, session
import os

# ime za bazu podataka i folder u koji ce se spremati
DATABASE_NAME = 'vodomjeri.db'
UPLOAD_FOLDER = 'datoteke'

def upload_db():
    # ako ne postoji UPLOAD_FOLDER napravi ga 
    db_filepath = os.path.join(session.get('user_id'), UPLOAD_FOLDER)
    if not os.path.exists(db_filepath):
        os.makedirs(db_filepath)
    
    #ako nije nađena baza - trebalo bi biti spriječeno sa frontend strane ali za svaki slucaj
    if 'database' not in request.files:
        return jsonify({'error': 'No file part'})
    
    file = request.files['database']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'})
    
    # ako je uploadan file s podrzanom ekstenzijom uploadaj
    if file.filename.endswith('.db'):
        filename = DATABASE_NAME
        filepath=os.path.join(db_filepath, filename)
        
        file.save(filepath)
        session["uploaded_file"]=filepath
        return jsonify({'success': 'Upload successful', 'filename': filename})
    else:
        return jsonify({'error': 'Upload failed - Please choose a file ending with .db'})
    
    
def download_db():
    
        filepath = session.get("uploaded_file")
        print(filepath)
        # Provjera ako postoji
        if filepath and os.path.exists(filepath):
            return send_file(filepath, as_attachment=True)
        else:
            return jsonify({'error': 'File not found'}), 404

    
def delete_db():
        filepath = session.get("uploaded_file")
        if (filepath):
            # brisanje datoteke s nazivom vodomjeri.db u datoteke folderu
            os.remove(filepath)
            session.pop("uploaded_file", None)
            return "File deleted"
        else: 
            return "File not found"

    
def vodomjeri_availability():
    # fukcija za provjeru dostupnosti baze podataka
    filename = DATABASE_NAME
    database_available = os.path.exists(session.get("uploaded_file"))
    # vraća true/false
    return jsonify(database_available)