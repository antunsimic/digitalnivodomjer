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
        for x in range(166, 168):
            redniBrojIzvoda += str(line[x])
        
        for x in range(172, 180):
            datum += str(line[x])

    if(flag == '905'):
        tmp = ''
        for x in range(2, 35):
            tmp += str(line[x])
        racunPlatitelja.append(tmp.strip())

        tmp = ''
        for x in range(36, 105):
            tmp += str(line[x])
        nazivPlatitelja.append(tmp.strip())

        tmp = ''
        for x in range(106, 140):
            tmp += str(line[x])
        adresaPlatitelja.append(tmp.strip())
        
        tmp = ''
        for x in range(141, 175):
            tmp += str(line[x])
        sjedistePlatitelja.append(tmp.strip())
        
        tmp = ''
        for x in range(184, 191):
            tmp += str(line[x])
        datumIzvrsenja.append(tmp.strip())

        tmp = ''
        for x in range(227, 241):
            tmp += str(line[x])
        iznos.append(tmp.strip())

        tmp = ''
        for x in range(268, 293):
            tmp += str(line[x])
        pozivNaBrojPlatitelja.append(tmp.strip())

        tmp = ''
        for x in range(298, 437):
            tmp += str(line[x])
        opisPlacanja.append(tmp.strip())

        brojStavke += 1
        redniBrojStavkeIzvoda.append(brojStavke)