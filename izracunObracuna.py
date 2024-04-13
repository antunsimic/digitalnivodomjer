import sqlite3
from datetime import datetime as datum

# vjerojatno potrebno zamijenit s mysql.connector u buducnosti
conn = sqlite3.connect('vodomjeri.db')
cursor = conn.cursor()

def upisUTablicu(obracun_id, korisnik_id, mjesec_godina, zbroj_ocitanja, datum_tren):

    # provjera postoji li vec u tablici
    cursor.execute('SELECT COUNT(*) FROM Obracun WHERE ID_korisnik = ? AND Razdoblje_obracun = ? AND Datum_obracun = ?', (korisnik_id, mjesec_godina, datum_tren))
    result = cursor.fetchone()[0]
    #print(result)

    if result == 0:  
        print("Inserting for korisnik_id:", korisnik_id, "rmodul:", rmodul[0], "mjesec_godina:", mjesec_godina, "zbroj_ocitanja:", round(zbroj_ocitanja, 2), "datum_tren:", datum_tren)
        cursor.execute('INSERT INTO Obracun (ID_obracun, ID_korisnik, Razdoblje_obracun, Potrosnja_hv, Datum_obracun) VALUES (?, ?, ?, ?, ?)', (obracun_id, korisnik_id, mjesec_godina, round(zbroj_ocitanja, 2), datum_tren))
        conn.commit()
    else:
        print("Skipping insertion for korisnik_id:", korisnik_id, "mjesec_godina:", mjesec_godina, "zbroj_ocitanja:", round(zbroj_ocitanja, 2), "datum_tren:", datum_tren)



# selectaj sve korisnike 
cursor.execute('SELECT DISTINCT ID_korisnik FROM Korisnik_oprema ORDER BY ID_korisnik')
korisnici = cursor.fetchall()

for korisnik in korisnici:
    korisnik_id = korisnik[0]

    # selectaj najnoviji Datum_preth_mj po rmodulu
    cursor.execute('SELECT DISTINCT Datum_preth_mj FROM Ocitanje ORDER BY Datum_preth_mj DESC LIMIT 1')
    datum_preth_mj = cursor.fetchone()[0]
    #print("dat Preth", datum_preth_mj)


    datum_preth_mj = datum.strptime(datum_preth_mj, "%Y.%m.%d")
    # formatiranje u GGGGMM
    mjesec_godina = datum_preth_mj.strftime('%Y%m')

    # pronađi max id_obracuna
    cursor.execute('''
        SELECT MAX(id_obracun)
        FROM Obracun
    ''')
    max_obracun_id = cursor.fetchone()[0]
    #Sprint(max_obracun_id)
    # ako nema postojeceg id-ja postavi na jedan inace inkrementiraj
    if max_obracun_id is None:
        obracun_id = 1
    else:
        obracun_id = max_obracun_id + 1
    
    # selectaj sve rmodule po korisniku
    cursor.execute('SELECT DISTINCT Broj_rmodul FROM Korisnik_oprema WHERE ID_korisnik = ?', (korisnik_id,))
    rmoduli = cursor.fetchall()

    datum_tren = None
    # Odabir datum_trena tako da se prođe skup rmdoula na datum_preth_mj i nađe najnoviji datum_tren ocitanja
    for rmodul in rmoduli:
        cursor.execute('SELECT DISTINCT Datum_tren FROM Ocitanje WHERE Broj_rmodul = ? AND Datum_preth_mj = ? ORDER BY Datum_tren DESC LIMIT 1', (rmodul[0], datum_preth_mj.strftime('%Y.%m.%d'),))
        latest_datum_tren = cursor.fetchone()
        #print(latest_datum_tren)
        if latest_datum_tren:
            latest_datum_tren = latest_datum_tren[0]
            if datum_tren is None or datum_tren < latest_datum_tren:
                datum_tren = latest_datum_tren


    zbroj_ocitanja = 0
    for rmodul in rmoduli:
        #print("rmodul: ", rmodul[0])
        # dohvati potrosnju vezanu za trenutni rmodul
        cursor.execute('SELECT DISTINCT Potrosnja_preth_mj FROM Ocitanje WHERE Broj_rmodul = ? AND Datum_preth_mj = ?', (rmodul[0], datum_preth_mj.strftime('%Y.%m.%d'),))
        potrosnja_preth_mj = cursor.fetchone()[0]
        #print(potrosnja_preth_mj)

        # ako je ocitanje nadeno zbroji potrosnju u ukupno ocitanje
        if potrosnja_preth_mj is not None:
            zbroj_ocitanja += potrosnja_preth_mj
        #ako nije nađeno ocitanje za neki od rmodul umjesto zbroja uzimaju se vrijednosti potrošnje zadnjih 6 mjeseci iz obračuna 
        else:
            cursor.execute('SELECT DISTINCT Potrosnja_hv FROM Obracun WHERE ID_korisnik = ? ORDER BY Razdoblje_obracun DESC LIMIT 6', (korisnik_id,))
            obracuni = cursor.fetchall()
                
            # ako u 6 mjeseci ima više ili jednako 3 obracuna moguce je maknuti mix i max
            if len(obracuni) >= 3:
                obracuni.sort()
                obracuni = obracuni[1:-1]

            # pretpostavka da se u nemogućnosti micanja min i max svejedno uzima prosjek
            zbroj_ocitanja = sum(obracun[0] for obracun in obracuni) / len(obracuni)
            
            # ako ne postoji - umetni 
            upisUTablicu(obracun_id, korisnik_id, mjesec_godina, zbroj_ocitanja, datum_tren)
            
    # AKO SE REDAK VEĆ POPUNIO u slučaju kad fali ocitanje, provjera bi trebala zaustavit ponovno popunjavanje
    upisUTablicu(obracun_id, korisnik_id, mjesec_godina, zbroj_ocitanja, datum_tren)


conn.close()
