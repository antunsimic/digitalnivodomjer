import sqlite3
from datetime import datetime as datum

# vjerojatno potrebno zamijenit s mysql.connector u buducnosti
conn = sqlite3.connect('vodomjeri.db')
cursor = conn.cursor()

# selectaj sve korisnike 
cursor.execute('SELECT ID_korisnik FROM Korisnik')
korisnici = cursor.fetchall()

for korisnik in korisnici:
    korisnik_id = korisnik[0]

    # selectanje broja_vodomjera vezanog za rmodul nije potebno mislim
    #cursor.execute('SELECT DISTINCT Broj_vodomjer FROM Ocitanje WHERE Broj_rmodul = ?', (rmodul[0],))
    #broj_vodomjer = cursor.fetchone()
    
    # selectaj sve rmodule po korisniku
    cursor.execute('SELECT DISTINCT Broj_rmodul FROM Korisnik_oprema WHERE ID_korisnik = ?', (korisnik_id,))
    rmoduli = cursor.fetchall()

    for rmodul in rmoduli:
        # selectaj najnoviji Datum_preth_mj po rmodulu
        cursor.execute('SELECT DISTINCT Datum_preth_mj FROM Ocitanje WHERE Broj_rmodul = ? ORDER BY Datum_preth_mj DESC LIMIT 1', (rmodul[0],))
        datum_preth_mj = cursor.fetchone()

        cursor.execute('SELECT DISTINCT Datum_tren FROM Ocitanje WHERE Broj_rmodul = ? AND Datum_preth_mj = ?', (rmodul[0], datum_preth_mj[0]))
        datum_tren = cursor.fetchone()

        if datum_preth_mj:
            datum_preth_mj = datum.strptime(datum_preth_mj[0], "%Y.%m.%d")
            # formatiranje u GGGGMM
            mjesec_godina = datum_preth_mj.strftime('%Y%m')
            
            #d ohvati sva ocitanja za taj mjesec
            cursor.execute('SELECT DISTINCT Potrosnja_preth_mj FROM Ocitanje WHERE Broj_rmodul = ? AND Datum_preth_mj = ?', (rmodul[0], datum_preth_mj.strftime('%Y.%m.%d'),))
            ocitanja = cursor.fetchall()

            if ocitanja:
                # zbroj Potrosnja_preth_mj
                zbroj_ocitanja = sum(ocitanje[0] for ocitanje in ocitanja)
                
                # provjera postoji li vec u tablici
                cursor.execute('SELECT COUNT(*) FROM Obracun WHERE ID_korisnik = ? AND Razdoblje_obracun = ? AND Datum_obracun = ?', (korisnik_id, mjesec_godina, datum_tren[0]))
                result = cursor.fetchone()

                # ako ne postoji - umetni 
                if result[0] == 0:  
                    print("Inserting for korisnik_id:", korisnik_id, "rmodul:", rmodul[0], "mjesec_godina:", mjesec_godina, "zbroj_ocitanja:", zbroj_ocitanja, "datum_tren:", datum_tren[0])
                    cursor.execute('INSERT INTO Obracun (ID_korisnik, Razdoblje_obracun, Potrosnja_hv, Datum_obracun) VALUES (?, ?, ?, ?)', (korisnik_id, mjesec_godina, zbroj_ocitanja, datum_tren[0]))
                    conn.commit()
                else:
                    print("Skipping insertion for korisnik_id:", korisnik_id, "rmodul:", rmodul[0], "mjesec_godina:", mjesec_godina, "zbroj_ocitanja:", zbroj_ocitanja, "datum_tren:", datum_tren[0])
            else:
                cursor.execute('SELECT DISTINCT Potrosnja_hv FROM Obracun WHERE ID_korisnik = ? ORDER BY Razdoblje_obracun DESC LIMIT 6', (korisnik_id,))
                obracuni = cursor.fetchall()
                
                if len(obracuni) >= 3:
                    obracuni.sort()
                    obracuni = obracuni[1:-1]

                    avg_ocitanja = sum(obracun[0] for obracun in obracuni) / len(obracuni)

                    # provjera postoji li
                    cursor.execute('SELECT COUNT(*) FROM Obracun WHERE ID_korisnik = ? AND Razdoblje_obracun = ? AND Datum_obracun = ?', (korisnik_id, mjesec_godina, datum_tren[0]))
                    result = cursor.fetchone()

                    if result[0] == 0:  # ako ne postoji - umetni 
                        print("Inserting for korisnik_id:", korisnik_id, "mjesec_godina:", mjesec_godina, "avg_ocitanja:", avg_ocitanja, "datum_tren:", datum_tren[0])
                        cursor.execute('INSERT INTO Obracun (ID_korisnik, Razdoblje_obracun, Potrosnja_hv, Datum_obracun) VALUES (?, ?, ?, ?)', (korisnik_id, mjesec_godina, avg_ocitanja, datum_tren[0]))
                        conn.commit()
                    else:
                        print("Skipping insertion for korisnik_id:", korisnik_id, "mjesec_godina:", mjesec_godina, "avg_ocitanja:", avg_ocitanja, "datum_tren:", datum_tren[0])

conn.close()
