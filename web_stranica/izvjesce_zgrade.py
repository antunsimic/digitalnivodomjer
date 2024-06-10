import sqlite3
import datetime as dt
from reportlab.platypus import  Paragraph, Spacer
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
import os
from flask import jsonify

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
        self.kraj = dat_kraj
        self.stanari = stanari
        
Korisnici = []
Izvjesca = []

def generacija_izvjestaja_zgrade():
    database_path = os.path.join(os.path.dirname(__file__), 'datoteke', 'vodomjeri.db') #POTENCIJALNI PROBLEM U PUTANJI

    conn = sqlite3.connect(database_path)                                               #POTENCIJALNI PROBLEM U PUTANJI

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
        Izvjesca.append(Zgrada(row[1], row[2], int(row[3]), datumPocetka.strftime("%Y.%m.%d"), datumKraja.strftime("%Y.%m.%d"), []))
        

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
        Izvjesca[korisnik.zgrada-1].stanari.append(korisnik)

    conn.close()
    kreiraj_pdf()
    return "uspjeh"
# Kreiranje .pdf datoteke-------------------------------------------------------------------------------------------

def create_pdf(zgrada):
    # Fetching the latest accounting period in YYYYMM format
    database_path = os.path.join(os.path.dirname(__file__), 'datoteke', 'vodomjeri.db') #POTENCIJALNI PROBLEM U PUTANJI
    conn = sqlite3.connect(database_path)                                               #POTENCIJALNI PROBLEM U PUTANJI
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(Razdoblje_obracun) FROM Obracun")
    najnovije_razdoblje = cursor.fetchone()[0]
    najnovije_razdoblje = str(najnovije_razdoblje)
    MM = najnovije_razdoblje[5:7]  # Extract month
    if len(MM) == 1:
        MM = '0' + MM  # Ensure month is two digits
    YYYY = najnovije_razdoblje[:4]  # Extract year
    
    # Assuming that the 'zgrada' object has an ID or some identifier to query specific records
    cursor.execute("SELECT MAX(Datum_tren) FROM Ocitanje")
    najnoviji_datum = cursor.fetchone()[0]
    conn.close()
    
    # Format address as in the given code example
    adresa = zgrada.adresa.replace('/', '_')
    adresa_split = adresa.split()
    adresa_formatted = '_'.join([r[:6] for r in adresa_split])

    # Set up the PDF document
    pdf_path = os.path.join(os.path.dirname(__file__), 'izvjestaji', 'zgrade') #POTENCIJALNI PROBLEM U PUTANJI
    doc_filename = f'{pdf_path}/{adresa_formatted}_{MM}_{YYYY}.pdf'            #POTENCIJALNI PROBLEM U PUTANJI
    doc = SimpleDocTemplate(doc_filename, rightMargin=60, leftMargin=60)

    elementi = []
    printajMe = [(
        "Rbr", "Stan                     ", "Serijski broj      \nvodomjera", 
        "Serijski broj      \nradio modula", "Lokacija", "Iznos\n (m3)", "Napomena         "
    )]

    # Append rows of data for each water meter
    i = 0
    for stanar in zgrada.stanari:
        for vodomjer in stanar.vodomjer:
            i += 1
            thistuple = (
                i, f"{stanar.ime} {stanar.prezime}", vodomjer.broj_vodomjer, 
                vodomjer.broj_modul, vodomjer.lokacija, vodomjer.ocitanje, "            "
            )
            printajMe.append(thistuple)

    # Create table for PDF
    t = Table(printajMe)
    t.setStyle(TableStyle([
        ('FONT', (1, 1), (-2, -2), 'Helvetica'),
        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
        ('BOX', (0, 0), (-1, -1), 0.25, colors.black)
    ]))
    elementi += [
        Paragraph(zgrada.adresa.upper()),
        Paragraph(f"{zgrada.postanski_broj} {zgrada.mjesto.upper()}"),
        Spacer(1, 40),
        Paragraph("Izvještaj o očitanju internih vodomjera"),
        Paragraph(f"Razdoblje: {zgrada.Razdoblje}"),
        Spacer(1, 20),
        t,
        Spacer(1, 40),
        Paragraph(f"U {zgrada.mjesto}, {najnoviji_datum}")
    ]

    doc.build(elementi)
    print(f"Generated report: {doc_filename}")

def kreiraj_pdf():
    for izvjesce in Izvjesca:
        create_pdf(izvjesce)

#def main():
#    generacija_izvjestaja_zgrade()

#if __name__ == "__main__":
#    main()
