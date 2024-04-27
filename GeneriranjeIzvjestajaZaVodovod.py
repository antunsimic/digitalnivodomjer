import sqlite3
import sys
import xlsxwriter



if len(sys.argv) != 1:
    print("Koristite: python program.py")
    sys.exit(1)

def Vodovod_izvjestaj_func():

    conn = sqlite3.connect('vodomjeri.db')
    cursor = conn.cursor()

    #dohvaćanje svih ID_zgrada
    cursor.execute('SELECT DISTINCT ID_zgrada FROM Korisnik')
    zgrade = cursor.fetchall()

    for zgrada_id, in zgrade:
        cursor.execute('SELECT Ulica_kbr FROM Zgrada WHERE ID_zgrada = ?', (zgrada_id,))
        adresa = cursor.fetchone()[0]
        adresa = adresa.replace('/', '_')
        adresa_split = adresa.split()
        adresa_formatted = '_'.join([r[:6] for r in adresa_split])

        #dohvaćanje najnovijeg Razdoblja_obracuna
        cursor.execute('SELECT MAX(Razdoblje_obracun) FROM Obracun')
        najnovije_razdoblje = cursor.fetchone()[0]
        najnovije_razdoblje = str(najnovije_razdoblje)
        MM = najnovije_razdoblje[-2:]
        YYYY = najnovije_razdoblje[:4]

        #dohvaćanje podataka o korisnicima za trenutnu zgradu i najnovije razdoblje obračuna
        cursor.execute('''
            SELECT Korisnik.Vod_ID, Korisnik.Vod_sif_kor, Korisnik.Vod_mm, Korisnik.Ime, Korisnik.Prezime, 
                Obracun.Potrosnja_hv
            FROM Korisnik
            JOIN Obracun ON Korisnik.ID_korisnik = Obracun.ID_korisnik
            WHERE Korisnik.ID_zgrada = ?
            AND Obracun.Razdoblje_obracun = ?;
        ''', (zgrada_id, najnovije_razdoblje))

        #kreiranje Excel datoteke
        workbook = xlsxwriter.Workbook(f'{adresa_formatted}_{MM}_{YYYY}.xlsx')
        worksheet = workbook.add_worksheet()

        #postavljanje širine stupaca
        column_widths = [10, 15, 10, 20, 15, 15, 15]
        for col, width in enumerate(column_widths):
            worksheet.set_column(col, col, width)

        #naslovi stupaca
        headers = ["ID", "Šifra korisnika", "Šifra MM", "Ime i prezime", "Potrošnja HV", "Potrošnja SV", "Razlika"]
        cell_format = workbook.add_format({'border': 1}) 
        for col, header in enumerate(headers):
            worksheet.write(0, col, header, cell_format)

        #postavljanje formata za stupce koji trebaju biti obojani
        yellow_format = workbook.add_format({'bg_color': '#FFFF00', 'border': 1})  
        green_format = workbook.add_format({'bg_color': '#00FF00', 'border': 1})
        
        #upisivanje podataka u Excel datoteku
        row = 1  
        col = 0
        for data in cursor.fetchall():
            #Vod_ID
            worksheet.write(row, col, data[0], cell_format)
            #Vod_sif_kor 
            worksheet.write(row, col + 1, data[1], yellow_format)
            #Vod_mm
            worksheet.write(row, col + 2, data[2], yellow_format)
            #Ime i prezime
            worksheet.write(row, col + 3, f"{data[3]} {data[4]}", yellow_format)
            #Potrošnja HV
            potrosnja_hv = "{:.2f}".format(data[5])
            worksheet.write(row, col + 4, potrosnja_hv, green_format)
            #Potrošnja SV
            worksheet.write(row, col + 5, 0, green_format)
            #Razlika 
            worksheet.write(row, col + 6, 0, green_format)
            row += 1

        workbook.close()

    conn.close()
    return "Kreirane xlsx datoteke"

#Vodovod_izvjestaj_func()