from flask import Flask, request, render_template
from bazaPodatakaFunct import upload_db, download_db, delete_db, vodomjeri_availability
app = Flask(__name__)

# treba spojit u file gdje su i ostale rute
# ruta za dohvaćanje stranice na kojoj se vrši prikaz i upload er slike
@app.route('/database_page')
def database_page():
    return render_template('db_page.html')

# ruta koja obavlja upload slike er
@app.route('/upload', methods=['POST'])
def upload():
    return upload_db()
    
# ruta za download slike er
@app.route('/download/<filename>', methods=['GET'])
def download(filename):
    return download_db(filename)

# ruta za brisanje datoteke i slike er
@app.route('/delete', methods=['DELETE'])
def delete():
    return delete_db()

# ruta za provjeru dostupnosti baze podataka
@app.route('/database_availability')
def database_availability():
    return vodomjeri_availability()

if __name__ == '__main__':
    app.run(debug=True)
