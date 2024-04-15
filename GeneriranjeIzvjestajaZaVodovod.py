import sqlite3
import sys

#provjera jesu li navedeni argumenti
if len(sys.argv) != 3:
    print("Koristite: python program.py <razdoblje_obracun> <id_zgrada>")
    sys.exit(1)

razdoblje_obracun = sys.argv[1]
id_zgrada = sys.argv[2]

conn = sqlite3.connect('vodomjeri.db')
cursor = conn.cursor()

#provjera postoje li potrebni podaci u bazi obracun
cursor.execute('''
    SELECT O.*
    FROM Obracun O
    JOIN Korisnik K ON O.ID_korisnik = K.ID_korisnik
    WHERE O.Razdoblje_obracun = ?
    AND K.ID_zgrada = ?;
''', (razdoblje_obracun, id_zgrada))

if not cursor.fetchall():
    print("Nema dostupnih podataka za navedeno razdoblje obračuna i ID zgrade.")
    conn.close()
    sys.exit(0)

print(f"Izvještaj za zgradu s ID-om {id_zgrada}:")
print("ID\tŠifra korisnika\tŠifra MM\tIme i prezime\tPotrošnja HV\tPotrošnja SV\tRazlika")

#dohvaćanje podataka o korisnicima za odabrano razdoblje obračuna i zgradu
cursor.execute('''
    SELECT Korisnik.ID_korisnik, Korisnik.Vod_sif_kor, Korisnik.Vod_mm, Korisnik.Ime, Korisnik.Prezime, Obracun.Potrosnja_hv
    FROM Korisnik
    JOIN Obracun ON Korisnik.ID_korisnik = Obracun.ID_korisnik
    WHERE Korisnik.ID_zgrada = ?
    AND Obracun.Razdoblje_obracun = ?;
''', (id_zgrada, razdoblje_obracun))

#ispis podataka o korisnicima
for data in cursor.fetchall():
    print(f"{data[0]}\t{data[1]}\t{data[2]}\t{data[3]} {data[4]}\t{data[5]}\t0\t0")

conn.close()
