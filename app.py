from flask import Flask
from ApatorMaddalena import Vodomjeri_func
from bankovni_izvodi import Bankovni_func
from GeneriranjeIzvjestajaZaVodovod import Vodovod_izvjestaj_func
from izracunObracuna import Obracun_izracun_func
from Izvjesce_zgrade import Ivjesce_zgrade_func

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Homepage(?)'

@app.route('/apator-maddalena')
def route_vodomjer():
    result = Vodomjeri_func()
    return result

@app.route('/bankovni-izvodi')
def route_bankovni():
    result = Bankovni_func()
    return result

@app.route('/vodovod-izvjestaj')
def route_vodovod_izvjestaj():
    result = Vodovod_izvjestaj_func()
    return result

@app.route('/obracun-izracun')
def route_obracun_izracun():
    result = Obracun_izracun_func()
    return result

@app.route('/zgrade-izvjestaj')
def route_zgrade_izvjestaj():
    result = Ivjesce_zgrade_func()
    return result



if __name__ == '__main__':
    app.run(debug=True)