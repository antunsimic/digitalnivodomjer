import unittest
from unittest.mock import MagicMock, patch
import sqlite3
from funkcije import fetch_zgrade, format_adresa, fetch_najnovije_razdoblje, fetch_korisnici_data, create_excel_file

class TestVodovodProgram(unittest.TestCase):

    @patch('sqlite3.connect')
    def test_fetch_zgrade(self, mock_connect):
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [(1,), (2,)]
        mock_connect.return_value.cursor.return_value = mock_cursor
        
        conn = sqlite3.connect('vodomjeri.db')
        cursor = conn.cursor()
        zgrade = fetch_zgrade(cursor)
        
        self.assertEqual(zgrade, [(1,), (2,)])
        mock_cursor.execute.assert_called_with('SELECT DISTINCT ID_zgrada FROM Korisnik')

    def test_format_adresa(self):
        adresa = 'Ulica 123/4'
        formatted = format_adresa(adresa)
        self.assertEqual(formatted, 'Ulica_123_4')

    @patch('sqlite3.connect')
    def test_fetch_najnovije_razdoblje(self, mock_connect):
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = (202306,)
        mock_connect.return_value.cursor.return_value = mock_cursor

        conn = sqlite3.connect('vodomjeri.db')
        cursor = conn.cursor()
        najnovije_razdoblje = fetch_najnovije_razdoblje(cursor)
        
        self.assertEqual(najnovije_razdoblje, 202306)
        mock_cursor.execute.assert_called_with('SELECT MAX(Razdoblje_obracun) FROM Obracun')

    @patch('sqlite3.connect')
    def test_fetch_korisnici_data(self, mock_connect):
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [
            (1, 'A1', 'M1', 'Ime', 'Prezime', 100.0)
        ]
        mock_connect.return_value.cursor.return_value = mock_cursor

        conn = sqlite3.connect('vodomjeri.db')
        cursor = conn.cursor()
        korisnici_data = fetch_korisnici_data(cursor, 1, 202306)
        
        self.assertEqual(korisnici_data, [(1, 'A1', 'M1', 'Ime', 'Prezime', 100.0)])
        mock_cursor.execute.assert_called_with('''
        SELECT Korisnik.Vod_ID, Korisnik.Vod_sif_kor, Korisnik.Vod_mm, Korisnik.Ime, Korisnik.Prezime, 
               Obracun.Potrosnja_hv
        FROM Korisnik
        JOIN Obracun ON Korisnik.ID_korisnik = Obracun.ID_korisnik
        WHERE Korisnik.ID_zgrada = ?
        AND Obracun.Razdoblje_obracun = ?;
    ''', (1, 202306))

    @patch('xlsxwriter.Workbook')
    def test_create_excel_file(self, mock_workbook):
        adresa_formatted = 'Ulica_123_4'
        najnovije_razdoblje = 202306
        korisnici_data = [(1, 'A1', 'M1', 'Ime', 'Prezime', 100.0)]

        create_excel_file(adresa_formatted, najnovije_razdoblje, korisnici_data)
        
        mock_workbook.assert_called_with('Ulica_123_4_06_2023.xlsx')
        workbook_instance = mock_workbook.return_value
        workbook_instance.add_worksheet.assert_called_once()
        worksheet_instance = workbook_instance.add_worksheet.return_value
        
        headers = ["ID", "Šifra korisnika", "Šifra MM", "Ime i prezime", "Potrošnja HV", "Potrošnja SV", "Razlika"]
        for col, header in enumerate(headers):
            worksheet_instance.write.assert_any_call(0, col, header, unittest.mock.ANY)
        
        worksheet_instance.write.assert_any_call(1, 0, 1, unittest.mock.ANY)
        worksheet_instance.write.assert_any_call(1, 1, 'A1', unittest.mock.ANY)
        worksheet_instance.write.assert_any_call(1, 2, 'M1', unittest.mock.ANY)
        worksheet_instance.write.assert_any_call(1, 3, 'Ime Prezime', unittest.mock.ANY)
        worksheet_instance.write.assert_any_call(1, 4, '100.00', unittest.mock.ANY)
        worksheet_instance.write.assert_any_call(1, 5, 0, unittest.mock.ANY)
        worksheet_instance.write.assert_any_call(1, 6, 0, unittest.mock.ANY)
        
        workbook_instance.close.assert_called_once()

if __name__ == '__main__':
    unittest.main()
