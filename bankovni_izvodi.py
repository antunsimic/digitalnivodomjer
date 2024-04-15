import mysql.connector

mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "root",
    database = "vodomjer"
)

file = open("/home/dado/Downloads/izvod.OTP", "r")
readLines = file.readlines()

redniBrojIzvoda = ''
datum = ''

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
    flag = str(line[len(line)-4]) + str(line[len(line)-3]) + str(line[len(line)-2])
    if(flag == '903'):
        for x in range(166, 169):
            redniBrojIzvoda += str(line[x])
        
        for x in range(172, 180):
            datum += str(line[x])

    if(flag == '905'):
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

#ubacivanje podataka u bazu
mycursor = mydb.cursor()

sql = "INSERT INTO Uplata (Rbr_Izvadak, Datum_izvrsenja, Iznos, Racun_platitelj, Naziv_platitelj, Adresa_platitelj, Sjediste_platitelj, Poziv_na_broj_primatelj, Opis_placanje) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"

for x in range(0, brojStavke):

    val = [
        redniBrojIzvoda,
        datumIzvrsenja,
        iznos,
        racunPlatitelja,
        nazivPlatitelja,
        adresaPlatitelja,
        sjedistePlatitelja,
        pozivNaBrojPlatitelja,
        opisPlacanja
    ]

    mycursor.executemany(sql, val)
    mydb.commit()