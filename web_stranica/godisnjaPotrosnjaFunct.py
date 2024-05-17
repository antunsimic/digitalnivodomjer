from flask import request, jsonify
import sqlite3



# Nalazi id, ulice i mjesta zgrada u Zgrada tablici i vraća ih za odabir na frontendu (ulica i mjesto kao tekst, id bi se trebao vratit po odabiru)
def get_zgrade():
    conn = sqlite3.connect('web_stranica/datoteke/vodomjeri.db')
    cursor = conn.cursor()
    buildings =cursor.execute('SELECT ID_zgrada, Ulica_kbr, Mjesto FROM Zgrada').fetchall()
    conn.close()
    return jsonify(buildings=[{'id': building[0], 'ulica': building[1], 'mjesto': building[2]} for building in buildings])
# Nalazi id, ime i prezime korisnika i vraća za ofabir na frontendu
def get_korisnici():
    conn = sqlite3.connect('web_stranica/datoteke/vodomjeri.db')
    cursor = conn.cursor()
    users = cursor.execute('SELECT ID_korisnik, Ime, Prezime FROM Korisnik').fetchall()    
    conn.close()
    return jsonify(users=[{'id': user[0], 'ime': user[1], 'prezime': user[2]} for user in users])
# Nalazi godinu za odabir na frontendu
def get_godine():
    conn = sqlite3.connect('web_stranica/datoteke/vodomjeri.db')
    cursor = conn.cursor()
    # substring koji iz Razdoblje_obracun uzima iskljucivo godinu
    years = cursor.execute('SELECT DISTINCT substr(Razdoblje_obracun, 1, 4) FROM Obracun').fetchall()
    conn.close()
    return jsonify(years=[year[0] for year in years])
# Na temelju odabranog(ID_zgrada, ID_korisnik, godina) uzima vrijednosti potrošnje i datume obračuna
def get_consumption():
    conn = sqlite3.connect('web_stranica/datoteke/vodomjeri.db')
    cursor = conn.cursor()
    building = request.args.get('building')
    user = request.args.get('user')
    year = request.args.get('year')

    result = cursor.execute(f"SELECT Datum_obracun, Potrosnja_hv FROM Obracun WHERE ¸ID_zgrada='{building}' AND ID_korisnik={user} AND razdoblje_obracun LIKE '{year}%'").fetchall()
    conn.close()
    # Vrijednosti koje se vracaju za graf 
    consumption = [{'datum': row[0], 'potrosnja': row[1]} for row in result]


    return jsonify({'consumption': consumption})

