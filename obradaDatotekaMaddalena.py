import pandas as pd  # biblioteka za rad s podacima
import os  # za pristupanje datotekama u direktoriju
import sqlite3
from datetime import datetime

class Maddalena:
    def __init__(self, broj_rmodul, datum_tren, stanje_tren, stanje_preth_mj, datum_m3, potrosnja_preth_mj):
        self.broj_rmodul = broj_rmodul
        self.datum_tren = datum_tren
        self.stanje_tren = int(float(stanje_tren)*1000)
        self.stanje_preth_mj = int(float(stanje_preth_mj)*1000)
        self.datum_m3 = datum_m3
        self.potrosnja_preth_mj = potrosnja_preth_mj

data_frames = []
excel_files = [file for file in os.listdir() if file.endswith('.xlsx')]  # sve excel datoteke u trenutnom direktoriju


# iteracija kroz sve excel datoteke i zapisivanje podataka u liste
for file in excel_files:
    data = pd.read_excel(file)
    selected_columns = ['Module serial', 'Timestamp', 'Reading', 'Value7'] #float mora imati tocku, a ne zarez (Reading, Value7)
    data = data[selected_columns]

    data['Reading'] = data['Reading'].str.replace(',','.')

    data['Value7'] = data['Value7'].str.replace(',','.')


    #data['Help'] = pd.to_datetime(data['Timestamp'], format='%d.%m.%Y %H:%M:%S')
    Help = pd.to_datetime(data['Timestamp'], format='%d.%m.%Y %H:%M:%S')
    #data['Datum_m3_help'] = (data['Help'] - pd.offsets.MonthEnd(1)).dt.date
    Datum_m3_help = (Help - pd.offsets.MonthEnd(1)).dt.date
    #data['Datum_m3'] = pd.to_datetime(data['Datum_m3_help']).dt.strftime("%d.%m.%Y")   
    data['Datum_m3'] = pd.to_datetime(Datum_m3_help).dt.strftime("%d.%m.%Y")            #unosi se u bazu
    data['Timestamp'] = pd.to_datetime(data['Timestamp']).dt.strftime("%m.%d.%Y")       #unosi se u bazu
    data_frames.append(data)
#1 data_frames element => 1 excel datoteka

svi_podaci = [] #pandas je glup

conn = sqlite3.connect('vodomjeri.db')

cur = conn.cursor()

#iteriraj kroz frameove; dodaj
for frame in data_frames:
    #iterirati od 0 do 29 (valjda je to max broj unosa)
    for i in range(28):

        #ovdje trazimo podatke za racunanje potrosnja_preth_mj -> stanje_preth_mj je value7, to imamo (trenutni datum 4.4)
        #racunamo datum_m3 od trenutnog datum_m3                                                      (trenutni datum_m3 31.3)
        #kad znamo datum_m3_inception onda uz broj modula najdemo trenutnu potrosnju                  (racunamo datum_m3 od 31.3 = 28/29. 2., TU JE RJESENJE)

        
        datum_m3 = pd.to_datetime(frame['Datum_m3'][i], format="%d.%m.%Y")
        datum_m3_m3 = (datum_m3 - pd.offsets.MonthEnd(1))
        datum_m3_m3 = datum_m3_m3.strftime('%d.%m.%Y')

        cur.execute(f"SELECT Stanje_tren FROM Ocitanje WHERE Broj_rmodul={frame['Module serial'][i]} AND Datum_preth_mj='{datum_m3_m3}'")

        stanje = cur.fetchone()
        if stanje is not None:
            stanje_predzadnje_ocitanje = stanje[0]
        else:
            stanje_predzadnje_ocitanje = 0


        potrosnja_preth_mj = float(float(frame['Value7'][i])*1000 - stanje_predzadnje_ocitanje) / 1000

        print("{:.2f}".format(potrosnja_preth_mj))

        #print(frame['Module serial'][i], frame['Timestamp'][i], frame['Reading'][i], frame['Value7'][i])
        svi_podaci.append(Maddalena(frame['Module serial'][i], frame['Timestamp'][i], frame['Reading'][i], frame['Value7'][i], frame['Datum_m3'][i], potrosnja_preth_mj))



for unos in svi_podaci:
                                            #INTEGER   #STRING     #INTEGER         #FLOAT         #STRING
    cur.execute(f"INSERT INTO Ocitanje (Broj_rmodul, Datum_tren, Stanje_tren, Stanje_preth_mj, Datum_preth_mj, Potrosnja_preth_mj) VALUES ({unos.broj_rmodul}, '{unos.datum_tren}', {unos.stanje_tren}, {unos.stanje_preth_mj}, '{unos.datum_m3}', {unos.potrosnja_preth_mj})")

conn.commit()
conn.close()