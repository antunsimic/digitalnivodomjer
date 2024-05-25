from flask import request, jsonify, session
import sqlite3

def connect_to_db():
    filepath = session.get("uploaded_file")
    print(filepath)
    #conn = sqlite3.connect('web_stranica/datoteke/vodomjeri.db')
    conn = sqlite3.connect(filepath)    
    cursor = conn.cursor()
    return conn, cursor

#### TREBALO BI NAMJESTIT DA TE PRVO ODABIRE ZGRADA PA SE TADA NA ON CHANGE DOHVACAJU DOSPIPNI KORISNICI,
#### KADA SE ODABRA KORISNIKA NA ON CHANGE SSE DOHVATE GODINE
# Nalazi id, ulice i mjesta zgrada u Zgrada tablici i vraća ih za odabir na frontendu (ulica i mjesto kao tekst, id bi se trebao vratit po odabiru)
def get_zgrade():
    conn, cursor = connect_to_db()
    buildings = cursor.execute('SELECT ID_zgrada, Ulica_kbr, Mjesto FROM Zgrada').fetchall()
    conn.close()
    return jsonify(buildings=[{'id': building[0], 'ulica': building[1], 'mjesto': building[2]} for building in buildings])

# Nalazi id, ime i prezime korisnika i vraća za ofabir na frontendu
def get_korisnici():
    conn, cursor = connect_to_db()
    selected_building = request.args.get('selected_building')
    # odabir korisnika s obzirom koja je zgrada odabrana
    users = cursor.execute('''
        SELECT ID_korisnik, Ime, Prezime 
        FROM Korisnik 
        WHERE ID_zgrada = ?
    ''', (selected_building,)).fetchall()
   
    conn.close()
    return jsonify(users=[{'id': user[0], 'ime': user[1], 'prezime': user[2]} for user in users])

# Nalazi godinu za odabir na frontendu
def get_godine():
    conn, cursor = connect_to_db()
    
    # substring koji iz Razdoblje_obracun uzima iskljucivo godinu, na temelju koji je user prethodno uzet
    years = cursor.execute('''SELECT DISTINCT substr(Razdoblje_obracun, 1, 4) FROM Obracun
    ''').fetchall()
    conn.close()
    return jsonify(years=[year[0] for year in years])

### NE VRIJEDE OGRANIČENJA REDOSLIJEDA ODABIRA
# kombinirana funkcija prethodne tri - ODABRATI koja je bolja za frontend ostalo izbrisat
def get_filter_data():
    conn, cursor = connect_to_db()
    
    # dohvaćanje podataka za odbir na frontendu
    buildings =cursor.execute('SELECT ID_zgrada, Ulica_kbr, Mjesto FROM Zgrada').fetchall()
    users = cursor.execute('SELECT ID_korisnik, Ime, Prezime FROM Korisnik').fetchall() 
    years = cursor.execute('SELECT DISTINCT substr(Razdoblje_obracun, 1, 4) FROM Obracun').fetchall()
    conn.close()

    # Uređivanje podataka za vraćanje na prontend
    buildings_data = [{'id': building[0], 'ulica': building[1], 'mjesto': building[2]} for building in buildings]
    users_data = [{'id': user[0], 'ime': user[1], 'prezime': user[2]} for user in users]
    years_data = [year[0] for year in years]
    
    #print("Buildings:", buildings)
    #print("Users:", users) 
    #print("Years:", years)
    
    return jsonify(buildings=buildings_data, users=users_data, years=years_data)

# Na temelju odabranog(ID_zgrada, ID_korisnik, godina) uzima vrijednosti potrošnje i datume obračuna
def get_consumption():
    conn, cursor = connect_to_db()
    building = request.args.get('building')
    user = request.args.get('user')
    year = request.args.get('year')

    result = cursor.execute(f"SELECT Datum_obracun, Potrosnja_hv FROM Obracun WHERE ID_korisnik={user} AND razdoblje_obracun LIKE '{year}%'").fetchall()
    conn.close()
    # Vrijednosti koje se vracaju za graf 
    consumption = [{'datum': row[0], 'potrosnja': row[1]} for row in result]


    return jsonify({'consumption': consumption})

    
