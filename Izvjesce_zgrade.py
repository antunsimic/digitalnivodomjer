# -*- coding: utf-8 -*-

import sqlite3
import datetime as dt

class vodomjer:
    def __init__(self, broj_vodomjer, broj_modul, ID, ocitanje, lokacija):
        self.broj_vodomjer = broj_vodomjer
        self.broj_modul = broj_modul
        self.IDKor = ID
        self.ocitanje = ocitanje
        self.lokacija = lokacija

class stanar:
    def __init__(self, ime, prezime, zgrada, ID, vodomjer):
        self.ime = ime
        self.prezime = prezime
        self.zgrada = zgrada
        self.ID = ID
        self.vodomjer = vodomjer

class Zgrada:
    def __init__(self, adresa, mjesto, postanski_broj, dat_poc, dat_kraj, stanari):
        self.Naslov = "Izvještaj o očitanju internih vodomjera"
        self.adresa = adresa 
        self.mjesto = mjesto
        self.postanski_broj = postanski_broj 
        self.Razdoblje = "Razdoblje: " + dat_poc + " - " + dat_kraj
        self.stanari = stanari
        self.kraj = "U slavonskom brodu, " + dt.datetime.now().date().strftime("%d.%m.%y")
        

Korisnici = []
Izvjesca = []

conn = sqlite3.connect('vodomjeri.db')

c = conn.cursor()

# Čitanje podataka za zgrade-------------------------------------------------------------------------------
sql = "SELECT MAX(Datum_preth_mj) FROM Ocitanje"
c.execute(sql)
datumT = c.fetchone()
datum = (datumT[0].split())[0]
datumKraja = dt.datetime.strptime(datum, '%m/%d/%Y')
datumPocetka = datumKraja - dt.timedelta(days = (datumKraja.day-1))

# Čitanje podataka za zgrade-------------------------------------------------------------------------------

sql = "SELECT * FROM 'Zgrada'"
c.execute(sql)
rows = c.fetchall()
for row in rows:
    Izvjesca.append(Zgrada(row[1], row[2], int(row[3]), datumPocetka.strftime("%d.%m.%Y"), datumKraja.strftime("%d.%m.%Y"), []))
    
    
    

# Dohvaćanje broja stanara po ID---------------------------------------------------------------------------------

sql = "SELECT MAX(ID_korisnik) FROM Korisnik"
c.execute(sql)
maximum = c.fetchone()

# Čitanje podataka za stanare----------------------------------------------------
sql = "SELECT * FROM 'Korisnik'"
c.execute(sql)
rows = c.fetchall()
Korisnici = [stanar("null", "null", 0, 0, [])]*(maximum[0]+1)
for row in rows:
    Korisnici[row[0]] = (stanar(row[4], row[3], row[2], row[0], []))




# Čitanje podataka vodomjera--------------------------------------------------------------------------------------
sql = "SELECT * FROM 'Korisnik_oprema'"
c.execute(sql)
rows = c.fetchall()
for row in rows:
    sql = "SELECT Potrosnja_preth_mj FROM Ocitanje WHERE Broj_rmodul = " + str(row[1])
    c.execute(sql)
    pot = c.fetchall()
    sql = "SELECT Lokacija FROM Korisnik_oprema WHERE Broj_rmodul = " + str(row[1])
    c.execute(sql)
    lok = c.fetchone()
    Korisnici[row[2]].vodomjer.append(vodomjer(row[0], row[1], row[2], pot[-1][0], lok[0]))
    
for korisnik in Korisnici:
    for mjera in korisnik.vodomjer:
        Izvjesca[korisnik.zgrada-1].stanari.append(korisnik)

conn.close()
