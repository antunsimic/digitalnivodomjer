import sqlite3
from datetime import datetime
import os

    


def process_file(file_path):
    directory = os.path.join(os.path.dirname(__file__), 'uploads')
    directory = os.path.abspath(directory)

    database_path = os.path.join(os.path.dirname(__file__), 'datoteke', 'vodomjeri.db')
    database_path = os.path.abspath(database_path)
    conn = sqlite3.connect(database_path, check_same_thread=False)
    cursor = conn.cursor()
    with open(file_path, "r") as file:
        readLines = file.readlines()

    datum = ''
    brojStavke = 0

    for line in readLines:
        flag = line[-4:].strip()  # Adjusted to strip any accidental whitespace

        if flag == '903':
            redniBrojIzvoda = line[166:169].strip()
            datum = line[172:180].strip()

        if flag == '905' and line[0:2].strip() == "20":  # Checks oztra right in the condition
            datum_izvrsenje = datetime.strptime(line[184:192].strip(), "%Y%m%d").strftime("%Y.%m.%d")
            data_tuple = (
                redniBrojIzvoda,
                brojStavke + 1,
                datetime.strptime(datum, "%Y%m%d").strftime("%Y.%m.%d"),
                datum_izvrsenje,
                float(line[227:242].strip()) / 100,
                line[2:36].strip(),
                line[36:106].strip(),
                line[106:141].strip(),
                line[141:176].strip(),
                line[268:294].strip(),
                line[298:438].strip()
            )
            print("baza")
            # Check for existing entry by redniBrojIzvoda, redniBrojStavkeIzvoda and Datum_izvrsenje
            cursor.execute("SELECT COUNT(*) FROM Uplata WHERE Rbr_izvadak=? AND Rbr_stv_izvadak=? AND Datum_izvrsenje=?", (redniBrojIzvoda, brojStavke + 1, datum_izvrsenje))
            if cursor.fetchone()[0] == 0:
                cursor.execute('INSERT INTO Uplata (Rbr_izvadak, Rbr_stv_izvadak, Datum_izvadak, Datum_izvrsenje, Iznos, Racun_platitelj, Naziv_platitelj, Adresa_platitelj, Sjediste_platitelj, Poziv_na_broj_primatelj, Opis_placanje) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);', data_tuple)
                conn.commit()
                brojStavke += 1

    print(f"Processed {brojStavke} entries from {file_path}")

# List all .OTP files in the specified directory and process them
def ucitavanje_izvoda():
    directory = os.path.join(os.path.dirname(__file__), 'uploads')
    directory = os.path.abspath(directory)

    database_path = os.path.join(os.path.dirname(__file__), 'datoteke', 'vodomjeri.db')
    database_path = os.path.abspath(database_path)
    conn = sqlite3.connect(database_path, check_same_thread=False)
    cursor = conn.cursor()
    for filename in os.listdir(directory):
        print(filename)
        if filename.endswith(".OTP"):
            file_path = os.path.join(directory, filename)
            process_file(file_path)
    conn.close()
    print("Completed processing all files.")

#ucitavanje_izvoda()
