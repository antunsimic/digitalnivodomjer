# Datoteka s funkcijama vezanim za upload, download, i deletion baze podatakaS
from flask import request, jsonify, send_file
import os

# ime za bazu podataka i folder u koji ce se spremati
DATABASE_NAME = 'vodomjeri.db'
UPLOAD_FOLDER = 'datoteke'

def upload_db():
    # ako ne postoji UPLOAD_FOLDER napravi ga 
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    
    #ako nije nađena baza - trebalo bi biti spriječeno sa frontend strane ali za svaki slucaj
    if 'database' not in request.files:
        return jsonify({'error': 'No file part'})
    
    file = request.files['database']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    # ako je dobro uploadana baza spremi ju u folder
    if file:
        filename = DATABASE_NAME
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        return jsonify({'success': 'er uploaded successfully', 'filename': filename})
    else:
        return jsonify({'error': 'Upload failed'})
    
    
def download_db():
    # ako je nadena downloadaj
    try:
        return send_file(os.path.join(UPLOAD_FOLDER, DATABASE_NAME), as_attachment=True)
    except FileNotFoundError:
        return jsonify({'error': 'File not found'})
    
def delete_db():
    try:
        # brisanje datoteke s nazivom vodomjeri.db u datoteke folderu
        os.remove(os.path.join(UPLOAD_FOLDER, DATABASE_NAME))
        return jsonify({'success': 'Database deleted successfully'})
    except FileNotFoundError:
        return jsonify({'error': 'File not found'})
    
def vodomjeri_availability():
    filename = DATABASE_NAME
    database_available = os.path.exists(os.path.join(UPLOAD_FOLDER, filename))
    return jsonify(database_available)