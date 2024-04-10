import sqlite3

conn = sqlite3.connect('vodomjeri.db')
cursor = conn.cursor()

#dohvaćanje svih id-eva zgrada
cursor.execute('SELECT ID_zgrada FROM Zgrada')
building_ids = [row[0] for row in cursor.fetchall()]

#prolazak kroz svaku zgradu i dohvaćanje podataka o korisnicima za trenutnu zgradu
for zgrada_id in building_ids:
    print(f"Izvještaj za zgradu s ID-om {zgrada_id}:")
    print("ID\tŠifra korisnika\tŠifra MM\tIme i prezime\tPotrošnja HV")
    cursor.execute('''
        SELECT Korisnik.ID_korisnik, Korisnik.Vod_sif_kor, Korisnik.Vod_mm, Korisnik.Ime, Korisnik.Prezime, Obracun.Potrosnja_hv
        FROM Korisnik
        INNER JOIN Obracun ON Korisnik.ID_korisnik = Obracun.ID_korisnik
        WHERE Korisnik.ID_zgrada = ?
    ''', (zgrada_id,))
    
    #ispis podataka o korisnicima
    for data in cursor.fetchall():
        print(f"{data[0]}\t{data[1]}\t{data[2]}\t{data[3]} {data[4]}\t{data[5]}")

conn.close()
