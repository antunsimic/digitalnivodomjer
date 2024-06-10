import os
from flask import send_file
import shutil

direktorij = os.path.dirname(__file__)

def get_izv_zgrade():

    path_izvjestaji = os.path.join(direktorij, 'izvjestaji', 'zgrade')

    DatotekeZgrade = []

    for file in os.listdir(path_izvjestaji):
        DatotekeZgrade.append(file)

    return DatotekeZgrade


def get_izv_vodovod():
    path_vodovod = os.path.join(direktorij, 'izvjestaji', 'vodovod')

    DatotekeVodovod = []

    for file in os.listdir(path_vodovod):
        DatotekeVodovod.append(file)

    return DatotekeVodovod

def preuzimanje_izv_zgrada():
    path_zgrade = os.path.join(direktorij, 'izvjestaji', 'zgrade')
    shutil.make_archive(path_zgrade, 'zip', path_zgrade)
    zip_path = os.path.join(direktorij, 'izvjestaji', 'zgrade.zip')
    return send_file(zip_path, as_attachment=True)

def preuzimanje_izv_vodovod():
    path_vodovod = os.path.join(direktorij, 'izvjestaji', 'vodovod')
    shutil.make_archive(path_vodovod, 'zip', path_vodovod)
    zip_path = os.path.join(direktorij, 'izvjestaji', 'vodovod.zip')
    return send_file(zip_path, as_attachment=True)


#def main():
#    preuzimanje_zgrada()

#if __name__ == "__main__":
#    main()