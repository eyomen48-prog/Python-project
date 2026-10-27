import json
from datetime import date

DOSYA = "harcamalar.json"
KATEGORI_DOSYA = "kategoriler.json"


def harcamalari_oku():
    try:
        with open(DOSYA, "r") as dosya:
            return json.load(dosya)
    except FileNotFoundError:
        return []


def harcamalari_kaydet(harcamalar):
    with open(DOSYA, "w") as dosya:
        json.dump(harcamalar, dosya)


def kategorileri_oku():
    try:
        with open(KATEGORI_DOSYA, "r") as dosya:
            return json.load(dosya)
    except FileNotFoundError:
        return ["benzin", "market", "cafe"]


def kategorileri_kaydet(kategoriler):
    with open(KATEGORI_DOSYA, "w") as dosya:
        json.dump(kategoriler, dosya)


def kategori_ekle(kategoriler):
    yeni = input("Yeni kategori adı: ").strip().lower()

    if yeni == "":
        print("Kategori adı boş olamaz.")
        return

    if yeni in kategoriler:
        print("Bu kategori zaten var.")
        return

    kategoriler.append(yeni)
    kategorileri_kaydet(kategoriler)
    print("Kategori eklendi:", yeni)


def kategori_sil(kategoriler, harcamalar):
    print("Kategoriler:", ", ".join(kategoriler))
    silinecek = input("Silinecek kategori: ").strip().lower()

    if silinecek not in kategoriler:
        print("Böyle bir kategori yok.")
        return

    kullanimda = False
    for harcama in harcamalar:
        if harcama["kategori"] == silinecek:
            kullanimda = True

    if kullanimda:
        print("Bu kategoride harcama var, silinemez.")
        print("Önce o harcamaları sil (menüden 5).")
        return

    kategoriler.remove(silinecek)
    kategorileri_kaydet(kategoriler)
    print("Kategori silindi:", silinecek)


def tarih_sor():
    giris = input("Tarih (YYYY-AA-GG, boş bırakırsan bugün): ").strip()

    if giris == "":
        return str(date.today())

    try:
        tarih = date.fromisoformat(giris)
    except ValueError:
        print("Geçersiz tarih. Örnek: 2026-10-25")
        return None

    if tarih > date.today():
        print("Gelecek bir tarih girilemez.")
        return None

    return str(tarih)


def harcama_ekle(harcamalar, kategoriler):
    print("Kategoriler:", ", ".join(kategoriler))
    kategori = input("Kategori: ").strip().lower()

    if kategori not in kategoriler:
        print("Geçersiz kategori.")
        return

    try:
        tutar = float(input("Tutar kaç TL? "))
    except ValueError:
        print("Geçersiz tutar, sayı yazmalısın.")
        return

    tarih = tarih_sor()

    if tarih is None:
        return

    harcamalar.append({"kategori": kategori, "tutar": tutar, "tarih": tarih})
    harcamalari_kaydet(harcamalar)
    print("Harcama kaydedildi:", tarih, "-", kategori, "-", tutar, "TL")


def listele(harcamalar):
    if len(harcamalar) == 0:
        print("Henüz harcama yok.")
        return

    for sira, harcama in enumerate(harcamalar, start=1):
        tarih = harcama.get("tarih", "tarih yok")
        print(sira, "-", tarih, "-", harcama["kategori"], "-", harcama["tutar"], "TL")


def harcama_sil(harcamalar):
    if len(harcamalar) == 0:
        print("Silinecek harcama yok.")
        return

    listele(harcamalar)

    try:
        numara = int(input("Silinecek harcamanın numarası: "))
    except ValueError:
        print("Geçersiz numara, sayı yazmalısın.")
        return

    if numara < 1 or numara > len(harcamalar):
        print("Böyle bir numara yok.")
        return

    silinen = harcamalar.pop(numara - 1)
    harcamalari_kaydet(harcamalar)
    print("Silindi:", silinen["kategori"], "-", silinen["tutar"], "TL")


def ozet_goster(harcamalar):
    toplam = 0
    kategori_toplam = {}

    for harcama in harcamalar:
        kategori = harcama["kategori"]
        toplam = toplam + harcama["tutar"]
        kategori_toplam[kategori] = kategori_toplam.get(kategori, 0) + harcama["tutar"]

    print("Toplam harcama:", toplam, "TL")
    print(kategori_toplam)


def aylik_ozet(harcamalar):
    bu_ay = str(date.today())[:7]
    toplam = 0
    kategori_toplam = {}

    for harcama in harcamalar:
        tarih = harcama.get("tarih", "")

        if tarih.startswith(bu_ay):
            kategori = harcama["kategori"]
            toplam = toplam + harcama["tutar"]
            kategori_toplam[kategori] = kategori_toplam.get(kategori, 0) + harcama["tutar"]

    print("Bu ay (" + bu_ay + ") toplam harcama:", toplam, "TL")
    print(kategori_toplam)


def sifirla(harcamalar):
    onay = input("Tüm harcamalar silinecek. Emin misin? (e/h): ")

    if onay == "e":
        harcamalar.clear()
        harcamalari_kaydet(harcamalar)
        print("Tüm harcamalar silindi.")
    else:
        print("Vazgeçildi.")


harcamalar = harcamalari_oku()
kategoriler = kategorileri_oku()

while True:
    print()
    print("1) Harcama ekle")
    print("2) Harcamaları listele")
    print("3) Toplamı gör")
    print("4) Bu ayın toplamını gör")
    print("5) Harcama sil")
    print("6) Yeni kategori ekle")
    print("7) Kategori sil")
    print("8) Hepsini sıfırla")
    print("9) Çık")

    secim = input("Seçimin: ")

    if secim == "1":
        harcama_ekle(harcamalar, kategoriler)
    elif secim == "2":
        listele(harcamalar)
    elif secim == "3":
        ozet_goster(harcamalar)
    elif secim == "4":
        aylik_ozet(harcamalar)
    elif secim == "5":
        harcama_sil(harcamalar)
    elif secim == "6":
        kategori_ekle(kategoriler)
    elif secim == "7":
        kategori_sil(kategoriler, harcamalar)
    elif secim == "8":
        sifirla(harcamalar)
    elif secim == "9":
        break
    else:
        print("Geçersiz seçim.")

print("Görüşürüz!")