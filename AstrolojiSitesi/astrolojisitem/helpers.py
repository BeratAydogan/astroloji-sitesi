from burclar import burclar

from .models import Burclar




def get_kullanici_burc(request):
    arananburc = ""
    resim = ""
    if request.user.is_authenticated:
        gun = request.user.profile.gun
        ay = request.user.profile.ay
        if (ay == 1 and gun >= 20) or (ay == 2 and gun <= 18):
            arananburc = "Kova"
        elif (ay == 2 and gun >= 19) or (ay == 3 and gun <= 20):
            arananburc = "Balık"
        elif (ay == 3 and gun >= 21) or (ay == 4 and gun <= 19):
            arananburc = "Koç"
        elif (ay == 4 and gun >= 20) or (ay == 5 and gun <= 20):
            arananburc = "Boğa"
        elif (ay == 5 and gun >= 21) or (ay == 6 and gun <= 21):
            arananburc = "İkizler"
        elif (ay == 6 and gun >= 22) or (ay == 7 and gun <= 22):
            arananburc = "Yengeç"
        elif (ay == 7 and gun >= 23) or (ay == 8 and gun <= 22):
            arananburc = "Aslan"
        elif (ay == 8 and gun >= 23) or (ay == 9 and gun <= 22):
            arananburc = "Başak"
        elif (ay == 9 and gun >= 23) or (ay == 10 and gun <= 22):
            arananburc = "Terazi"
        elif (ay == 10 and gun >= 23) or (ay == 11 and gun <= 21):
            arananburc = "Akrep"
        elif (ay == 11 and gun >= 22) or (ay == 12 and gun <= 21):
            arananburc = "Yay"
        elif (ay == 12 and gun >= 22) or (ay == 1 and gun <= 19):
            arananburc = "Oğlak"
        else:
            arananburc = ""

        resim = Burclar.objects.all().get(burc_adi=arananburc).resim.url

    return arananburc, resim



def yorumgetir(request):




    koc = burclar.koc('gunluk')
    boga = burclar.boga('gunluk')
    ikizler = burclar.ikizler('gunluk')
    yengec = burclar.yengec('gunluk')
    aslan = burclar.aslan('gunluk')
    basak = burclar.basak('gunluk')
    terazi = burclar.terazi('gunluk')
    akrep = burclar.akrep('gunluk')
    yay = burclar.yay('gunluk')
    oglak = burclar.oglak('gunluk')
    kova = burclar.kova('gunluk')
    balik = burclar.balik('gunluk')
    koc_burcu = Burclar.objects.get(id=1)
    koc_burcu.gunluk_yorum = koc
    koc_burcu.save()

    boga_burcu = Burclar.objects.get(id=2)
    boga_burcu.gunluk_yorum = boga
    boga_burcu.save()

    ikizler_burcu = Burclar.objects.get(id=3)
    ikizler_burcu.gunluk_yorum = ikizler
    ikizler_burcu.save()

    yengec_burcu = Burclar.objects.get(id=4)
    yengec_burcu.gunluk_yorum = yengec
    yengec_burcu.save()

    aslan_burcu = Burclar.objects.get(id=5)
    aslan_burcu.gunluk_yorum = aslan
    aslan_burcu.save()

    basak_burcu = Burclar.objects.get(id=6)
    basak_burcu.gunluk_yorum = basak
    basak_burcu.save()

    terazi_burcu = Burclar.objects.get(id=7)
    terazi_burcu.gunluk_yorum = terazi
    terazi_burcu.save()

    akrep_burcu = Burclar.objects.get(id=8)
    akrep_burcu.gunluk_yorum = akrep
    akrep_burcu.save()

    yay_burcu = Burclar.objects.get(id=9)
    yay_burcu.gunluk_yorum = yay
    yay_burcu.save()

    oglak_burcu = Burclar.objects.get(id=10)
    oglak_burcu.gunluk_yorum = oglak
    oglak_burcu.save()

    kova_burcu = Burclar.objects.get(id=11)
    kova_burcu.gunluk_yorum = kova
    kova_burcu.save()

    balik_burcu = Burclar.objects.get(id=12)
    balik_burcu.gunluk_yorum = balik
    balik_burcu.save()





def yorumgonder(user):
    arananburc = ""
    resim = ""

    gun = user.profile.gun
    ay = user.profile.ay
    if (ay == 1 and gun >= 20) or (ay == 2 and gun <= 18):
        arananburc = "Kova"
    elif (ay == 2 and gun >= 19) or (ay == 3 and gun <= 20):
        arananburc = "Balık"
    elif (ay == 3 and gun >= 21) or (ay == 4 and gun <= 19):
        arananburc = "Koç"
    elif (ay == 4 and gun >= 20) or (ay == 5 and gun <= 20):
        arananburc = "Boğa"
    elif (ay == 5 and gun >= 21) or (ay == 6 and gun <= 21):
        arananburc = "İkizler"
    elif (ay == 6 and gun >= 22) or (ay == 7 and gun <= 22):
        arananburc = "Yengeç"
    elif (ay == 7 and gun >= 23) or (ay == 8 and gun <= 22):
        arananburc = "Aslan"
    elif (ay == 8 and gun >= 23) or (ay == 9 and gun <= 22):
        arananburc = "Başak"
    elif (ay == 9 and gun >= 23) or (ay == 10 and gun <= 22):
        arananburc = "Terazi"
    elif (ay == 10 and gun >= 23) or (ay == 11 and gun <= 21):
        arananburc = "Akrep"
    elif (ay == 11 and gun >= 22) or (ay == 12 and gun <= 21):
        arananburc = "Yay"
    elif (ay == 12 and gun >= 22) or (ay == 1 and gun <= 19):
        arananburc = "Oğlak"
    else:
        arananburc = ""

        resim = Burclar.objects.all().get(burc_adi=arananburc).resim.url

    return arananburc, resim
