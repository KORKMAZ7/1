from flask import Flask, request, jsonify

app = Flask(__name__)

class Calisan:
    def __init__(self, ad, soyad, pozisyon, saatlik_ucret, calisma_gunleri):
        self.ad = ad
        self.soyad = soyad
        self.pozisyon = pozisyon
        self.saatlik_ucret = saatlik_ucret
        self.calisma_gunleri = calisma_gunleri

    def maas_hesapla(self, calisma_saatleri):
        calisma_saati = sum(calisma_saatleri)

        if self.pozisyon == "muhendis" or self.pozisyon == "operator":
            if calisma_saati > 8:
                maas = 8 * self.saatlik_ucret + (calisma_saati - 8) * 1.5 * self.saatlik_ucret
            else:
                maas = calisma_saati * self.saatlik_ucret
        else:
            # "isci" için varsayılan hesaplama
            if calisma_saati > 8:
                maas = 8 * self.saatlik_ucret + (calisma_saati - 8) * 1.5 * self.saatlik_ucret
            else:
                maas = calisma_saati * self.saatlik_ucret

        if "pazar" in self.calisma_gunleri:
            maas *= 2

        return calisma_saati, maas

@app.route('/maas_hesapla', methods=['POST'])
def maas_hesapla():
    data = request.get_json()

    ad = data['ad']
    soyad = data['soyad']
    pozisyon = data['pozisyon']
    saatlik_ucret = float(data['saatlik_ucret'])
    calisma_gunleri = data['calisma_gunleri']

    calisma_saatleri = data['calisma_saatleri']

    calisan = Calisan(ad, soyad, pozisyon, saatlik_ucret, calisma_gunleri)

    calisma_saat, maas = calisan.maas_hesapla(calisma_saatleri)

    result = {
        'ad': calisan.ad,
        'soyad': calisan.soyad,
        'pozisyon': calisan.pozisyon,
        'calisma_saat': calisma_saat,
        'maas': maas
    }

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, port=3000 )
