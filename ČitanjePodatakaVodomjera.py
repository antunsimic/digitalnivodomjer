# -*- coding: utf-8 -*-

import datetime as dt

class RFU30:
    def __init__(self, A, B, C, D, E, F, G, H, I, J, K):
        self.A = A
        self.B = B
        self.C = C
        self.D = D
        self.E = E
        self.F = F
        self.G = G
        self.H = H
        self.I = I
        self.J = J
        self.K = K
        datum_m3 = A - dt.timedelta(days = (A.day+1))


ParsedData = []
name = input("Enter filename: ")

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