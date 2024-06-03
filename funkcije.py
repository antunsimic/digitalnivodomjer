import sqlite3
import xlsxwriter

def fetch_zgrade(cursor):
    cursor.execute('SELECT DISTINCT ID_zgrada FROM Korisnik')
    return cursor.fetchall()

def format_adresa(adresa):
    adresa = adresa.replace('/', '_')
    adresa_split = adresa.split()
    adresa_formatted = '_'.join([r[:6] for r in adresa_split])
    return adresa_formatted

def fetch_najnovije_razdoblje(cursor):
    cursor.execute('SELECT MAX(Razdoblje_obracun) FROM Obracun')
    return cursor.fetchone()[0]

def fetch_korisnici_data(cursor, zgrada_id, najnovije_razdoblje):
    cursor.execute('''
        SELECT Korisnik.Vod_ID, Korisnik.Vod_sif_kor, Korisnik.Vod_mm, Korisnik.Ime, Korisnik.Prezime, 
               Obracun.Potrosnja_hv
        FROM Korisnik
        JOIN Obracun ON Korisnik.ID_korisnik = Obracun.ID_korisnik
        WHERE Korisnik.ID_zgrada = ?
        AND Obracun.Razdoblje_obracun = ?;
    ''', (zgrada_id, najnovije_razdoblje))
    return cursor.fetchall()

def create_excel_file(adresa_formatted, najnovije_razdoblje, korisnici_data):
    najnovije_razdoblje = str(najnovije_razdoblje)
    MM = najnovije_razdoblje[-2:]
    YYYY = najnovije_razdoblje[:4]
    
    workbook = xlsxwriter.Workbook(f'{adresa_formatted}_{MM}_{YYYY}.xlsx')
    worksheet = workbook.add_worksheet()

    column_widths = [10, 15, 10, 20, 15, 15, 15]
    for col, width in enumerate(column_widths):
        worksheet.set_column(col, col, width)

    headers = ["ID", "Šifra korisnika", "Šifra MM", "Ime i prezime", "Potrošnja HV", "Potrošnja SV", "Razlika"]
    cell_format = workbook.add_format({'border': 1}) 
    for col, header in enumerate(headers):
        worksheet.write(0, col, header, cell_format)

    yellow_format = workbook.add_format({'bg_color': '#FFFF00', 'border': 1})  
    green_format = workbook.add_format({'bg_color': '#00FF00', 'border': 1})

    row = 1
    for data in korisnici_data:
        worksheet.write(row, 0, data[0], cell_format)
        worksheet.write(row, 1, data[1], yellow_format)
        worksheet.write(row, 2, data[2], yellow_format)
        worksheet.write(row, 3, f"{data[3]} {data[4]}", yellow_format)
        potrosnja_hv = "{:.2f}".format(data[5])
        worksheet.write(row, 4, potrosnja_hv, green_format)
        worksheet.write(row, 5, 0, green_format)
        worksheet.write(row, 6, 0, green_format)
        row += 1

    workbook.close()
