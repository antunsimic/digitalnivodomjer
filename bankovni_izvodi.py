import sqlite3
from datetime import datetime

conn = sqlite3.connect('vodomjeri.db')
cursor = conn.cursor()

#file = open("/home/dado/Downloads/IZV_07082023-07082023.OTP", "r")
#file = open("/home/dado/Downloads/IZV_14082023-15082023.OTP", "r")
file = open("/home/dado/Downloads/IZV_18082023-20082023.OTP", "r")
readLines = file.readlines()

redniBrojIzvoda = ''
datum = ''

oztra = []
racunPlatitelja = []
nazivPlatitelja = []
adresaPlatitelja = []
sjedistePlatitelja = []
datumIzvrsenja = []
iznos = []
pozivNaBrojPlatitelja = []
opisPlacanja = []

brojStavke = 0
redniBrojStavkeIzvoda = []

for line in readLines:
    #slog
    flag = str(line[len(line)-4]) + str(line[len(line)-3]) + str(line[len(line)-2])

    if(flag == '903'):
        for x in range(166, 169):
            redniBrojIzvoda += str(line[x])
        
        for x in range(172, 180):
            datum += str(line[x])

    if(flag == '905'):
        tmp = ''
        for x in range(0, 2):
            tmp += str(line[x])
        oztra.append(tmp.strip())

        tmp = ''
        for x in range(2, 36):
            tmp += str(line[x])
        racunPlatitelja.append(tmp.strip())

        tmp = ''
        for x in range(36, 106):
            tmp += str(line[x])
        nazivPlatitelja.append(tmp.strip())

        tmp = ''
        for x in range(106, 141):
            tmp += str(line[x])
        adresaPlatitelja.append(tmp.strip())
        
        tmp = ''
        for x in range(141, 176):
            tmp += str(line[x])
        sjedistePlatitelja.append(tmp.strip())
        
        tmp = ''
        for x in range(184, 192):
            tmp += str(line[x])
        datumIzvrsenja.append(tmp.strip())

        tmp = ''
        for x in range(227, 242):
            tmp += str(line[x])
        iznos.append(tmp.strip())

        tmp = ''
        for x in range(268, 294):
            tmp += str(line[x])
        pozivNaBrojPlatitelja.append(tmp.strip())

        tmp = ''
        for x in range(298, 438):
            tmp += str(line[x])
        opisPlacanja.append(tmp.strip())

        brojStavke += 1
        redniBrojStavkeIzvoda.append(brojStavke)

datumFormatted = datetime.strptime(datum, "%Y%m%d").strftime("%Y.%m.%d")

for x in range(0, len(oztra)):
    if(oztra[x] == "20"):
        #ubacivanje podataka u bazu
        query = """INSERT INTO Uplata 
                    (Rbr_izvadak, Rbr_stv_izvadak, Datum_izvadak, Datum_izvrsenje, Iznos, Racun_platitelj, Naziv_platitelj, Adresa_platitelj, Sjediste_platitelj, Poziv_na_broj_primatelj, Opis_placanje)
                    VALUES
                    (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"""

        for x in range(0, brojStavke):
            datumIzvrsenjaFormatted = datetime.strptime(datumIzvrsenja[x], "%Y%m%d").strftime("%Y.%m.%d")

            data_tuple = (redniBrojIzvoda, x+1,  datumFormatted, datumIzvrsenjaFormatted, float(iznos[x])/100, racunPlatitelja[x], nazivPlatitelja[x], adresaPlatitelja[x], sjedistePlatitelja[x], pozivNaBrojPlatitelja[x], opisPlacanja[x])

            cursor.execute(query, data_tuple)
            conn.commit()
    
conn.close()

print("Uneseno je " + str(brojStavke) + " sloga")