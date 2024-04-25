# -*- coding: utf-8 -*-

import sqlite3
import datetime as dt
from reportlab.platypus import  Paragraph, Spacer
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors

class vodomjer:
    def __init__(self, broj_vodomjer, broj_modul, ID, ocitanje, lokacija):
        self.broj_vodomjer = broj_vodomjer
        self.broj_modul = broj_modul
        self.IDKor = ID
        self.ocitanje = ocitanje
        self.lokacija = lokacija

class stanar:
    def __init__(self, ime, prezime, zgrada, ID, vodomjer, obracun):
        self.ime = ime
        self.prezime = prezime
        self.zgrada = zgrada
        self.ID = ID
        self.vodomjer = vodomjer
        self.zadOb = obracun

class Zgrada:
    def __init__(self, adresa, mjesto, postanski_broj, dat_poc, dat_kraj, stanari):
        self.Naslov = "Izvještaj o očitanju internih vodomjera"
        self.adresa = adresa 
        self.mjesto = mjesto
        self.postanski_broj = postanski_broj 
        self.Razdoblje = "" + dat_poc + " - " + dat_kraj
        self.stanari = stanari
        
Korisnici = []
Izvjesca = []

conn = sqlite3.connect('vodomjeri.db')

c = conn.cursor()

# Čitanje podataka-------------------------------------------------------------------------------
sql = "SELECT MAX(Datum_preth_mj) FROM Ocitanje"
c.execute(sql)
datumT = c.fetchone()
datum = (datumT[0].split())[0]
datumKraja = dt.datetime.strptime(datum, '%Y.%m.%d')
datumPocetka = datumKraja - dt.timedelta(days = (datumKraja.day-1))

# Čitanje podataka za zgrade-------------------------------------------------------------------------------

sql = "SELECT * FROM 'Zgrada'"
c.execute(sql)
rows = c.fetchall()
for row in rows:
    Izvjesca.append(Zgrada(row[1], row[2], int(row[3]), datumPocetka.strftime("%d.%m.%Y"), datumKraja.strftime("%d.%m.%Y"), []))
    

# Dohvaćanje broja stanara po ID

sql = "SELECT MAX(ID_korisnik) FROM Korisnik"
c.execute(sql)
maximum = c.fetchone()

# Čitanje podataka za stanare----------------------------------------------------
sql = "SELECT * FROM 'Korisnik'"
c.execute(sql)
rows = c.fetchall()
Korisnici = [stanar("null", "null", 0, 0, [], 0)]*(maximum[0]+1)

for row in rows:
    sql = "SELECT Razdoblje_obracun FROM 'Obracun' WHERE ID_korisnik = " + str(row[0])
    c.execute(sql)
    obracun = c.fetchone()
    if (obracun == None):
        obracun = [0,0]
    Korisnici[row[0]] = (stanar(row[4], row[3], row[2], row[0], [], obracun))

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

# Kreiranje .pdf datoteke-------------------------------------------------------------------------------------------

def create_pdf(zgrada):
        
    # Parsiranje pdataka za kreiranje imena datoteke
    maxOb = 0
    for stanar in zgrada.stanari:
        if stanar.zadOb[0] > maxOb:
            maxOb = stanar.zadOb[0]
    doc = SimpleDocTemplate(zgrada.mjesto[:6] + "_" + str(zgrada.adresa).replace("/","_") + "_" + 
                            str(maxOb)[:4] + "_" + str(maxOb)[2:] + ".pdf",rightMargin=60,leftMargin=60)
    
    # Parsiranje podataka za lakše printanje
    elementi = []
    printajMe = []
    tp = ("Rbr", "Stan                     ", "Serijski broj      \nvodomjera", "Serijski broj      \nradio modula", "Lokacija"
          ,"Iznos\n (m3)", "Napomena         ")
    printajMe.append(tp)
    i = 0;
    for stanar in zgrada.stanari:
        for vodomjer in stanar.vodomjer:
            i+=1
            thistuple = (i, (stanar.ime + " " + stanar.prezime), 
            vodomjer.broj_vodomjer, vodomjer.broj_modul, vodomjer.lokacija, vodomjer.ocitanje, "            ")
            printajMe.append(thistuple)
    #for k in printajMe[11]:
    #    print(k)
    t = Table(printajMe)
    t.setStyle(TableStyle([('FONT',(1,1),(-2,-2),'Helvetica'),
                           ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                           ('BOX', (0,0), (-1,-1), 0.25, colors.black)]))
    elementi.append(Paragraph(zgrada.adresa.upper()))
    elementi.append(Paragraph(str(zgrada.postanski_broj) + " " + zgrada.mjesto.upper()))
    elementi.append(Spacer(1,40))
    elementi.append(Paragraph("Izvještaj o očitanju internih vodomjera"))
    elementi.append(Paragraph("Razdoblje: " + zgrada.Razdoblje))
    elementi.append(Spacer(1,20))
    elementi.append(t)
    elementi.append(Spacer(1,40))
    elementi.append(Paragraph("U " + zgrada.mjesto + ", " + zgrada.Razdoblje))
    
    doc.build(elementi)

for izvjesce in Izvjesca:
    create_pdf(izvjesce)
