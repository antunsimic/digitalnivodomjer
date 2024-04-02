# -*- coding: utf-8 -*-

import datetime as dt

# deklaracija klase koja sadržava sve potrebne informacije
# float varijable su spremljene kao stringovi da se izbjegnu krivi zapisi zbog nepreciznosti float vrijable
class RFU30:
    def __init__(self, A, B, C, D, E, F, G, H, I, J, K):
        temp = A
        self.A = A.strftime("%d.%m.%Y") # Datum mjerenja                        (datum, spremljen kao string)
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
        self.datum_m3 = ((A - dt.timedelta(days = (A.day+1))).strftime("%d.%m.%Y")) 

# svi podatci datoteke spremljeni u listu
ParsedData = []

name = input("Enter filename: ")

# otvaranje i čitanje datoteke te pretvaranje podataka u odgovarajući format
f = open(name, "r")
data = f.readlines()
for l in data:
    p = l.split()
    if len(p) > 1:
        ParsedData.append(RFU30(dt.datetime.strptime(p[0], '%m.%d.%Y'),
                            int(p[1]),
                            p[2],
                            p[3],
                            p[4],
                            p[5],
                            int(p[6]),
                            int(p[7]),
                            int(p[8]),
                            p[9], int(p[10])))
