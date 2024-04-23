#import sqlite3
from datetime import datetime
import os

import sqlalchemy as db

current_dir = os.getcwd()
next_dir = "datoteke"
directory = os.path.join(current_dir, next_dir)
    #directory = r"C:\Users\antun_81f2caf\OneDrive\studij\6._semestar\programsko_inzenjerstvo\projekt\unos_izvoda"  # Update this path as necessary
    #conn = sqlite3.connect('vodomjeri.db', check_same_thread=False)
    #cursor = conn.cursor()
engine = db.create_engine('sqlite:///vodomjeri.db')
conn = engine.connect()
metadata = db.MetaData()
uplata = db.Table('Uplata', metadata, autoload_with=engine)


def process_file(file_path):
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

            # Check for existing entry by redniBrojIzvoda, redniBrojStavkeIzvoda and Datum_izvrsenje
                    #cursor.execute("SELECT COUNT(*) FROM Uplata WHERE Rbr_izvadak=? AND Rbr_stv_izvadak=? AND Datum_izvrsenje=?", (redniBrojIzvoda, brojStavke + 1, datum_izvrsenje))
                    #if cursor.fetchone()[0] == 0:
                    #    cursor.execute('INSERT INTO Uplata (Rbr_izvadak, Rbr_stv_izvadak, Datum_izvadak, Datum_izvrsenje, Iznos, Racun_platitelj, Naziv_platitelj, Adresa_platitelj, Sjediste_platitelj, Poziv_na_broj_primatelj, Opis_placanje) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);', data_tuple)
                    #    conn.commit()
                    #    brojStavke += 1
            query = db.Select(db.func.count("*")).select_from(uplata).where(db.and_(uplata.columns.Rbr_Izvadak == int(redniBrojIzvoda), uplata.columns.Rbr_stv_izvadak == int(brojStavke + 1), uplata.columns.Datum_izvrsenje == datum_izvrsenje))
            ResultProxy = conn.execute(query)
            if ResultProxy.fetchone()[0] == 0:
                query = db.insert(uplata).values(Rbr_Izvadak=int(data_tuple[0]), Rbr_stv_izvadak=data_tuple[1], Datum_izvadak=data_tuple[2], Datum_izvrsenje=data_tuple[3], Iznos=data_tuple[4], Racun_platitelj=data_tuple[5], Naziv_platitelj=data_tuple[6], Adresa_platitelj=data_tuple[7], Sjediste_platitelj=data_tuple[8], Poziv_na_broj_primatelj=data_tuple[9], Opis_placanje=data_tuple[10])
                ResultProxy = conn.execute(query)
                conn.commit()
                brojStavke += 1
            
            

    #print(f"Processed {brojStavke} entries from {file_path}")

# List all .OTP files in the specified directory and process them
def Bankovni_func():
    for filename in os.listdir(directory):
        if filename.endswith(".OTP"):
            file_path = os.path.join(directory, filename)
            process_file(file_path)

            #conn.close()
    #print("Completed processing all files.")
    return "Completed processing all files."

Bankovni_func()