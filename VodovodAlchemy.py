import sys
import sqlalchemy as db

def Vodovod_izvjestaj_func():

    if len(sys.argv) != 1:
        print("Koristite: python program.py")
        sys.exit(1)

    engine = db.create_engine('sqlite:///vodomjeri.db')
    conn = engine.connect()
    metadata = db.MetaData()
    obracun = db.Table('Obracun', metadata, autoload_with=engine)
    korisnik = db.Table('Korisnik', metadata, autoload_with=engine)
    #conn = sqlite3.connect('vodomjeri.db')
    #cursor = conn.cursor()

    #dohvaćanje najnovijeg Razdoblje_obracun
    #cursor.execute('SELECT MAX(Razdoblje_obracun) FROM Obracun')
    #najnovije_razdoblje = cursor.fetchone()[0]
    query = db.Select(db.func.max(obracun.columns.Razdoblje_obracun)).select_from(obracun)
    ResultProxy = conn.execute(query)
    najnovije_razdoblje = ResultProxy.fetchone()[0]

    #dohvaćanje svih ID_zgrada
    #cursor.execute('SELECT DISTINCT ID_zgrada FROM Korisnik')
    #zgrade = cursor.fetchall()
    query = db.Select(korisnik.columns.ID_zgrada.distinct())
    ResultProxy = conn.execute(query)
    zgrade = ResultProxy.fetchall()

    for zgrada_id, in zgrade:
        #print(f"Izvještaj za zgradu s ID-om {zgrada_id}:")
        #print("ID\tŠifra korisnika\tŠifra MM\tIme i prezime\tPotrošnja HV\tPotrošnja SV\tRazlika")

        #dohvaćanje podataka o korisnicima za trenutnu zgradu i najnovije razdoblje obračuna
        #cursor.execute('''
        #    SELECT Korisnik.Vod_ID, Korisnik.Vod_sif_kor, Korisnik.Vod_mm, Korisnik.Ime, Korisnik.Prezime, Obracun.Potrosnja_hv
        #    FROM Korisnik
        #    JOIN Obracun ON Korisnik.ID_korisnik = Obracun.ID_korisnik
        #    WHERE Korisnik.ID_zgrada = ?
        #    AND Obracun.Razdoblje_obracun = ?;
        #''', (zgrada_id, najnovije_razdoblje))
        i = 0
        #query = db.Select(korisnik.columns.Vod_ID, korisnik.columns.Vod_sif_kor, korisnik.columns.Vod_mm, korisnik.columns.Ime, korisnik.columns.Prezime ,obracun.columns.Potrosnja_hv).join(korisnik, korisnik.columns.ID_korisnik == obracun.columns.ID_korisnik).where(db.and_(korisnik.columns.ID_zgrada==zgrada_id, obracun.columns.Razdoblje_obracun==najnovije_razdoblje))
        ResultProxy = conn.execute(query)
        
        for data in ResultProxy.fetchall():
            i += 1
            print(data, i)
        



        #ispis podataka o korisnicima
        #for data in cursor.fetchall():
        #    print(f"{data[0]}\t{data[1]}\t{data[2]}\t{data[3]} {data[4]}\t{data[5]}\t0\t0")
        #print("\n")

        #return cursor.fetchall()

    #conn.close()

Vodovod_izvjestaj_func()
