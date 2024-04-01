f = open("/home/dado/Downloads/izvod.OTP", "r")
lines = f.readlines()

rbIzv = ''
datum = ''

rnPrPl = ''
nazPrPl = ''
adrPrPl = ''
sjPrPl = ''
datIzvr = ''
iznos = ''
pnBrPr = ''
opisPl = ''

brStavke = 0

for line in lines:
    flag = str(line[len(line)-4]) + str(line[len(line)-3]) + str(line[len(line)-2])
    if(flag == '903'):
        for x in range(166, 168):
            rbIzv += str(line[x])
        
        for x in range(172, 180):
            datum += str(line[x])

    if(flag == '905'):
        for x in range(2, 35):
            rnPrPl += str(line[x])

        for x in range(36, 105):
            nazPrPl += str(line[x])

        for x in range(106, 140):
            adrPrPl += str(line[x])
        
        for x in range(141, 175):
            sjPrPl += str(line[x])
        
        for x in range(184, 191):
            datIzvr += str(line[x])

        for x in range(227, 241):
            iznos += str(line[x])

        for x in range(268, 293):
            pnBrPr += str(line[x])

        for x in range(298, 437):
            opisPl += str(line[x])

        brStavke += 1

print(iznos)