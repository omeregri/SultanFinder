import json
import datetime
import random
import requests
import wikipediaapi


AYLAR = [
    "Ocak",
    "Şubat",
    "Mart",
    "Nisan",
    "Mayıs",
    "Haziran",
    "Temmuz",
    "Ağustos",
    "Eylül",
    "Ekim",
    "Kasım",
    "Aralık"
]


def tarih_yuzyil(tarih):
    return tarih.year // 100 + 1

def parse_tarih(satir):
    tarih = satir.split("=")[1].strip()
    gun = 1
    ay = 1
    yil = None

    tarih = tarih.replace("-", " ")

    if tarih == "":
        pass
    elif "{" in tarih:
        tarih = tarih.replace("{", " ").replace("}", " ").replace("|", " ")
        S = tarih.split(" ")
        tarihler = [s for s in S if s in AYLAR or s.isnumeric()][:3]

        if len(tarihler) == 3:
            yil, ay, gun = int(tarihler[0]), int(tarihler[1]), int(tarihler[2])
        else:
            yil = int(tarihler[0])
    else:
        S = tarih.split(" ")
        tarihler = [s for s in S if s in AYLAR or s.isnumeric()][:3]
        if len(tarihler) == 3:
            gun, ay, yil = int(tarihler[0]), AYLAR.index(tarihler[1]) + 1, int(tarihler[2])
        elif len(tarihler) == 2:
            ay, yil = AYLAR.index(tarihler[0]) + 1, int(tarihler[1])
        elif len(tarihler) == 1:
            yil = int(tarihler[0])

    return datetime.datetime(yil, ay, gun).date()

def dogum_olum_tarih(hukumdar):
    url = "https://tr.wikipedia.org/w/api.php?format=json&action=query&titles={title}&prop=revisions&rvprop=content"
    r = requests.get(url.replace("{title}", hukumdar))
    js = json.loads(r.text)
    p = js["query"]["pages"]

    dogum, olum = None, None
    for satir in p[list(p.keys())[0]]["revisions"][0]["*"].split("\n"):
        try:
            if "doğum_tarihi" in satir:
                dogum = parse_tarih(satir)
            elif "ölüm_tarihi" in satir:
                olum = parse_tarih(satir)
        except Exception as e:
            pass
    return dogum, olum

gun, ay, yil = [int(x) for x in input("Tarih Giriniz (GG/AA/YY)").split("/")]
tarih = datetime.datetime(year = yil, month = ay, day = gun).date()

wiki = wikipediaapi.Wikipedia('tr')
doneme_gore_hukumdarlar = wiki.page(u"Kategori:Dönemlerine göre hükümdarlar")

yuzyila_gore_hukumdarlar = {}
yuzyila_gore_hukumdarlar = dict(yuzyila_gore_hukumdarlar.items() | doneme_gore_hukumdarlar.categorymembers[f"Kategori:{tarih_yuzyil(tarih) - 1}. yüzyıl hükümdarları"].categorymembers.items())
yuzyila_gore_hukumdarlar = dict(yuzyila_gore_hukumdarlar.items() | doneme_gore_hukumdarlar.categorymembers[f"Kategori:{tarih_yuzyil(tarih)}. yüzyıl hükümdarları"].categorymembers.items())
yuzyila_gore_hukumdarlar = dict(yuzyila_gore_hukumdarlar.items() | doneme_gore_hukumdarlar.categorymembers[f"Kategori:{tarih_yuzyil(tarih) + 1}. yüzyıl hükümdarları"].categorymembers.items())

for hukumdar in yuzyila_gore_hukumdarlar:
    dogum, olum = dogum_olum_tarih(hukumdar)
    if dogum == None or olum == None:
        continue
    elif dogum <= tarih <= olum:
        print("-" * 20)
        print(hukumdar)
        print("Doğum Tarihi: " + str(dogum))
        print("Ölüm  Tarihi: " + str(olum))
        print(yuzyila_gore_hukumdarlar[hukumdar].summary.split("\n\n")[0][:500])
        print()
