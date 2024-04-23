import sqlite3
import sys

def Vodovod_izvjestaj_func():

    if len(sys.argv) != 1:
        print("Koristite: python program.py")
        sys.exit(1)

    conn = sqlite3.connect('vodomjeri.db')
    cursor = conn.cursor()

    #dohvaćanje najnovijeg Razdoblje_obracun
    cursor.execute('SELECT MAX(Razdoblje_obracun) FROM Obracun')
    najnovije_razdoblje = cursor.fetchone()[0]
    #print(najnovije_razdoblje)

    #dohvaćanje svih ID_zgrada
    cursor.execute('SELECT DISTINCT ID_zgrada FROM Korisnik')
    zgrade = cursor.fetchall()
    print(zgrade)

    for zgrada_id, in zgrade:
        #print(f"Izvještaj za zgradu s ID-om {zgrada_id}:")
        #print("ID\tŠifra korisnika\tŠifra MM\tIme i prezime\tPotrošnja HV\tPotrošnja SV\tRazlika")

        #dohvaćanje podataka o korisnicima za trenutnu zgradu i najnovije razdoblje obračuna
        cursor.execute('''
            SELECT Korisnik.Vod_ID, Korisnik.Vod_sif_kor, Korisnik.Vod_mm, Korisnik.Ime, Korisnik.Prezime, Obracun.Potrosnja_hv
            FROM Korisnik
            JOIN Obracun ON Korisnik.ID_korisnik = Obracun.ID_korisnik
            WHERE Korisnik.ID_zgrada = ?
            AND Obracun.Razdoblje_obracun = ?;
        ''', (zgrada_id, najnovije_razdoblje))
        
        i = 0
        for data in cursor.fetchall():
            i += 1
            print(data, i)

        #ispis podataka o korisnicima
        #for data in cursor.fetchall():
        #    print(f"{data[0]}\t{data[1]}\t{data[2]}\t{data[3]} {data[4]}\t{data[5]}\t0\t0")
        #print("\n")

        return cursor.fetchall()

    conn.close()

Vodovod_izvjestaj_func()
