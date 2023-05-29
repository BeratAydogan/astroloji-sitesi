from django.shortcuts import render
from . models import Burclar
from datetime import date,timedelta
from django.contrib.auth.models import User
from .helpers import get_kullanici_burc, yorumgetir
import pyaztro ,requests
from django.http import JsonResponse
from AstrolojiSitesi import settings
from geopy.geocoders import Nominatim
from astropy.coordinates import SkyCoord
from astropy import units as u
from astropy.time import Time
from astropy.coordinates import EarthLocation, AltAz

def anasayfa(request):
    resim = ""
    arananburc = ""

    if request.user.is_authenticated:
        arananburc, resim = get_kullanici_burc(request)

    data = {
        "Burcbilgi": Burclar.objects.all(),
        "kullanici_burc": arananburc,
        "kullanici_burc_resim":resim,

    }
    return render(request,"index.html",data)



def burclar(request):
    resim = ""
    arananburc = ""

    if request.user.is_authenticated:
        arananburc, resim = get_kullanici_burc(request)
    burclar = Burclar.objects.all()
    yorumgetir(request)
    data = {
        "kullanici_burc": arananburc,
        "kullanici_burc_resim": resim,
        "Burcbilgi": Burclar.objects.all(),


        }

    return render(request,"burclar.html",data)


def detaylar(request,id):
    resim = ""
    arananburc = ""

    if request.user.is_authenticated:
        arananburc, resim = get_kullanici_burc(request)



    burc_obj = Burclar.objects.get(id=id)


    data = {

        "burc": Burclar.objects.get(id=id),
        "kullanici_burc": arananburc,
        "kullanici_burc_resim": resim,
    }
    return render(request,"detaylar.html",data)






def burc_hesapla(request):

    if request.method == 'POST':
        gun = int(request.POST.get('gun'))
        ay = int(request.POST.get('ay'))


        # burç hesaplama işlemleri
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
            arananburc = "Hatalı giriş"


        burc_obj = Burclar.objects.get(burc_adi=arananburc)
        burcimg1 = burc_obj.resim
        burctarih1 = burc_obj.tarih
        burcid1 = burc_obj.id



        resim = ""
        arananburc2 = ""

        if request.user.is_authenticated:
            arananburc2, resim = get_kullanici_burc(request)
        data = {

            "Burcbilgi": Burclar.objects.all(),
            "kullanici_burc": arananburc2,
            "kullanici_burc_resim": resim,
            "arananburc": arananburc,
            "arananburc_img":burcimg1,
            "arananburc_id":burcid1,

        }

        return render(request, 'burclar.html', data)



    return render(request, 'burclar.html',data)





def burc_yukselen_hesapla(request):

    if request.user.is_authenticated:
        arananburc2, resim = get_kullanici_burc(request)
    else:
        arananburc2, resim =" "," "
    data = {}
    if request.method == 'POST':
        yil = int(request.POST.get('yil'))
        gun = int(request.POST.get('gun'))
        ay = int(request.POST.get('ay'))
        saat = int(request.POST.get('saat'))
        dakika = int(request.POST.get('dakika'))
        saniye = int(request.POST.get('saniye'))
        sehir = request.POST.get('sehir')

        # burç hesaplama işlemleri
        geolocator = Nominatim(user_agent="Zodiac Ascendant Calculator")

        # Kullanıcının doğum yeri bilgilerini al
        birth_city = sehir

        # Geolocator nesnesini kullanarak doğum yerinin koordinatlarını al
        location = geolocator.geocode(birth_city)
        birth_location = EarthLocation(lat=location.latitude * u.deg, lon=location.longitude * u.deg)

        # Kullanıcının doğum tarih ve saat bilgilerini al
        birth_time = f"{yil}-{ay}-{gun} {saat}:{dakika}:{saniye}"
        birth_time = Time(birth_time)

        asc_coords = SkyCoord(ra=0 * u.hourangle, dec=0 * u.deg, frame='icrs')
        alt_az = AltAz(location=birth_location, obstime=birth_time)
        asc_coords_altaz = asc_coords.transform_to(alt_az)
        asc_alt = asc_coords_altaz.alt.degree
        asc_sign = int((asc_alt / 30.0) + 1) % 12  # Calculate the zodiac sign based on altitude

        # Sonucu ekrana yazdır
        zodiac_signs = ['Koç', 'Boğa', 'İkizler', 'Yengeç', 'Aslan', 'Başak', 'Terazi', 'Akrep', 'Yay',
                        'Oğlak', 'Kova', 'Balık']

        yukselen_burc = zodiac_signs[asc_sign]
        burc_obj2 = Burclar.objects.get(burc_adi=yukselen_burc)
        burcimg2 = burc_obj2.resim
        burctarih2 = burc_obj2.tarih
        burcid2 = burc_obj2.id
        burc_yukselen = burc_obj2.yukselen



        data = {
            "Burcbilgi": Burclar.objects.all(),
            "yukselen_burc":yukselen_burc,
            "yukselen_burc_img":burcimg2,
            "yukselen_burc_tarih":burctarih2,
            "yukselen_burc_id": burcid2,
            "burc_yukselen": burc_yukselen,
            "kullanici_burc": arananburc2,
            "kullanici_burc_resim": resim,


        }

        return render(request, 'yukselenhesap.html', data)



    return render(request, 'yukselenhesap.html', data)




