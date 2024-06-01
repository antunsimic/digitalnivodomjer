import datetime
import os
import sqlite3
import pandas as pd  # biblioteka za rad s podacima

# deklaracija klase koja sadržava sve potrebne informacije
# float varijable su spremljene kao stringovi da se izbjegnu krivi zapisi zbog nepreciznosti float vrijable
class RFU30:
    def __init__(self, A, B, C, D, E, F, G, H, I, J, K):
        temp = A
        self.A = A.strftime("%Y.%m.%d") # Datum mjerenja                        (datum, spremljen kao string)
        self.B = B # serijski broj E-RM30 modula                                (int)
        self.C = C # unaprijedna potrošnja u prošlom periodu plačanja           (float, ali spremljen kao string)
        self.D = D # peteroznamenkasti kod za unaprijednu potrošnju             (string)
        self.E = E # unazadna potrošnja vode u prošlom periodu plačanja         (float, ali spremljen kao string)
        self.F = F # peteroznamenkasti kod za unazadnu potrošnju                (string)
        self.G = G # apsolutna unapriedna potrošnja vode od početka mjerenja    (int)
        self.H = H # apsolutna unazadna potrošnja vode od početka mjerenja      (int)
        self.I = I # status elektroničkog pečata (0 - valjano, 1 - korumpirano) (int)
        self.J = J # početni datum perioda plačanja ( dan.mjesec )              (datum, spremljen kao string)
        self.K = K # reserva (za proizvođača)                                   (int)
        
        # datum zadnjeg dana u mjesecu (datum, spremljen kao string)
        self.datum_m3 = ((A - datetime.timedelta(days = (A.day))).strftime("%Y.%m.%d")) 


class Maddalena:
    def __init__(self, broj_rmodul, datum_tren, stanje_tren, stanje_preth_mj, datum_m3, potrosnja_preth_mj):
        self.broj_rmodul = broj_rmodul
        self.datum_tren = datum_tren
        self.stanje_tren = int(float(stanje_tren)*1000)
        self.stanje_preth_mj = int(float(stanje_preth_mj)*1000)
        self.datum_m3 = datum_m3
        self.potrosnja_preth_mj = potrosnja_preth_mj

def ocitanja_vodomjera():
    print('a')
    ###################     APATOR PARSING  ########################################
    # svi podatci datoteke spremljeni u listu
    ParsedDataApator = []
    
    directory = os.path.join(os.path.dirname(__file__), 'uploads')
    directory = os.path.abspath(directory)
    print(directory)
    apator_files = [file for file in os.listdir(directory) if file.endswith('.txt')]
    print(apator_files)

    # otvaranje i čitanje datoteke te pretvaranje podataka u odgovarajući format
    for file in apator_files:
        f = open(os.path.join(directory, file), "r")
        data = f.readlines()
        for l in data:
            p = l.split()
            if len(p) > 1:
                ParsedDataApator.append(RFU30(datetime.datetime.strptime(p[0], '%d.%m.%Y'),
                                    int(p[1]),
                                    p[2],
                                    p[3],
                                    p[4],
                                    p[5],
                                    int(p[6]),
                                    int(p[7]),
                                    int(p[8]),
                                    p[9], int(p[10])))


    #uzimaju se A,B,C,G,datum_m3 i stavljaju u bazu podataka:
    #prolazi se kroz sve (3) .txt datoteke, u tablicu Ocitanje se unose podaci

    ###################    /APATOR PARSING     ########################################



    ###################    MADDALENA PARSING   ########################################

    data_frames = []                                                         #za pandas
    excel_files = [file for file in os.listdir(directory) if file.endswith(('.xlsx', '.xls'))]  # sve excel datoteke u trenutnom direktoriju
    ParsedDataMaddalena = []                                                 #za laksu iteraciju kroz podatke te spremanje u bazu


    # iteracija kroz sve excel datoteke i zapisivanje podataka u liste
    for file in excel_files:
        data = pd.read_excel(os.path.join(directory, file))
        selected_columns = ['Module serial', 'Timestamp', 'Reading', 'Value7'] #float mora imati tocku, a ne zarez (Reading, Value7)
        data = data[selected_columns]

        data['Reading'] = data['Reading'].str.replace(',','.')
        data['Value7'] = data['Value7'].str.replace(',','.')


        #data['Help'] = pd.to_datetime(data['Timestamp'], format='%d.%m.%Y %H:%M:%S')
        Help = pd.to_datetime(data['Timestamp'], format='%d.%m.%Y %H:%M:%S')
        Datum_m3_help = (Help - pd.offsets.MonthEnd(1)).dt.date 
        data['Datum_m3'] = pd.to_datetime(Datum_m3_help).dt.strftime("%Y.%m.%d")            #unosi se u bazu
        data['Timestamp'] = pd.to_datetime(data['Timestamp'], dayfirst=True)
        data['Timestamp'] = data['Timestamp'].dt.strftime("%Y.%m.%d")
        data_frames.append(data)
    #1 data_frames element => 1 excel datoteka

    ###################    /MADDALENA PARSING   ########################################

    database_path = os.path.join(os.path.dirname(__file__), 'datoteke', 'vodomjeri.db')
    database_path = os.path.abspath(database_path)
    conn = sqlite3.connect(database_path, check_same_thread=False)
    cur = conn.cursor()         #koristi se za SQL naredbe

    #iteriraj kroz frameove; dodaj
    for frame in data_frames:
        #iterirati dok god frame['Timestamp'][tableRow] nije NaN (NULL?)
        tableRow = 0
        while not pd.isnull(frame['Timestamp'][tableRow]):
            
            datum_m3 = pd.to_datetime(frame['Datum_m3'][tableRow], format="%Y.%m.%d") #kraj prethodnog mjeseca od referente točke
            datum_m3_m3 = (datum_m3 - pd.offsets.MonthEnd(1))                  #kraj pret-prethodnog mjeseca
            datum_m3_m3 = datum_m3_m3.strftime('%Y.%m.%d')                     #pretvorba u string

            cur.execute(f"SELECT Stanje_tren FROM Ocitanje WHERE Broj_rmodul={frame['Module serial'][tableRow]} AND Datum_preth_mj='{datum_m3_m3}'") #filtriraju se stanja iz predzadnjeg ocitanja 

            stanje = cur.fetchone()
            if stanje is not None: #moguće je da nema unosa stanja u prethodnom mjesecu u tablici (greška je kod formatiranja datuma u bazi podataka)
                stanje_predzadnje_Ocitanje = stanje[0]
            else:
                stanje_predzadnje_Ocitanje = 0

            potrosnja_preth_mj = float(float(frame['Value7'][tableRow])*1000 - stanje_predzadnje_Ocitanje) / 1000
            if potrosnja_preth_mj>90000 or potrosnja_preth_mj<0:
                potrosnja_preth_mj = 0
            #print("{:.2f}".format(potrosnja_preth_mj))

            ParsedDataMaddalena.append(Maddalena(frame['Module serial'][tableRow], frame['Timestamp'][tableRow], frame['Reading'][tableRow], frame['Value7'][tableRow], frame['Datum_m3'][tableRow], potrosnja_preth_mj))
            tableRow = tableRow + 1


    brojUnosa = 0  #(u bazu podataka)

    #unos ucitanih podataka Maddalena uredaja u bazu podataka
    for unos in ParsedDataMaddalena:
                                                #INTEGER   #STRING     #INTEGER         #INTEGER         #STRING    #REAL
        cur.execute(f"INSERT OR REPLACE INTO Ocitanje (Broj_rmodul, Datum_tren, Stanje_tren, Stanje_preth_mj, Datum_preth_mj, Potrosnja_preth_mj) VALUES ({unos.broj_rmodul}, '{unos.datum_tren}', {unos.stanje_tren}, {unos.stanje_preth_mj}, '{unos.datum_m3}', ROUND({unos.potrosnja_preth_mj}, 2))")
        brojUnosa = brojUnosa + 1


    #unos ucitanih podataka Apator uredaja u bazu podataka
    for unos in ParsedDataApator:
                                            #TEXT       INTEGER         REAL              INTEGER         TEXT         INTEGER[prazno]
                                #Ocitanje: Datum_tren,   Broj_rmodul, Potrosnja_preth_mj, Stanje_tren, Datum_preth_mj, (Stanje_preth_mj)
        cur.execute(f"INSERT OR REPLACE INTO Ocitanje (Datum_tren, Broj_rmodul, Potrosnja_preth_mj, Stanje_tren, Datum_preth_mj) VALUES ('{unos.A}', {unos.B}, {float(unos.C.replace(',', '.'))}, {unos.G}, '{unos.datum_m3}')")
        #umjesto pretvaranja u float ovdje, to je moguce napraviti pri dodavanju u listu, makar nema veze
        brojUnosa = brojUnosa + 1

    print(f"Napravljeno je {brojUnosa} unosa u bazu podataka")

    conn.commit()
    conn.close() #zatvaranje veze s bazom podataka

#ocitanja_vodomjera()
