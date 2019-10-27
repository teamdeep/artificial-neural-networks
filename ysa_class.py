from numpy import *
import pandas as pd

# G = giriş değerleri
# cevap = son adımda beklenen çıkış değeri
# net_sayisi = her adım için olması gereken net sayisi
# ag_agirlik = sinir ağları ilk atanan random ağırlıklar
# ag_agirlik_yeni = Geri yayılım ile güncellenen ağ ağırlığı
# a ilk giris dizisinden veri çekmek için
# c cevap dizisinden çekiceğimiz verinin numarası
# d ilk dönüş dizisinden veri çekmek için
# e ikinci dönüş dizisinden veri çekmek için
# f ikinci dönüş dizisinden veri çekmek için
class Ysa():
    def __init__(self,):
        self.ag_agirlik = []
        df = pd.read_csv("haberman.csv")
        #print(df.head(2))
        #print(df.iloc[0:2,:4:2].head()) # [baslangıc degeri:kaca kadar yazıcak,: kaç sutun yazacak: hangi stunu yazacak]
        #print(df.iloc[4:5, :2].values)# degerleri alıyoruz. [baslangıc degeri: kaca kadar, : hangi sutun]
        #deger = list(df.iloc[4:5, :2].values)
        #print(deger[0][1]) #id sı 4 olan adamın yaşı 31 dir.
        #print(list(df["Age"].head(len(df['ID'])))[4]) #unutursanız diye yukardaki yazımı unutursanız böylede yapabilirsiniz.
        #self.ilk_giris = [1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1, 1, 0, 0, 0, 1]

        #self.cevap = [1, 0, 0, 1, 0, 1, 1, 0]
        self.ilk_giris = []
        self.diziAge = list(df["Age"].head(len(df["ID"])))
        self.diziYears = list(df["Years"].head(len(df["ID"])))
        self.diziNode =list(df["Node"].head(len(df["ID"])))

        #print(self.diziAge,"\n",self.diziYears,"\n",self.diziNode,"\n")

        for i in range(len(self.diziAge)):
            self.ilk_giris.append(self.diziAge[i])
            self.ilk_giris.append(self.diziYears[i])
            self.ilk_giris.append(self.diziNode[i])
        #print(self.ilk_giris)

        self.hedefDegisken = list(df["Status"].head(len(df["ID"])))
        #print(self.hedefDegisken)

        self.ag_agirlik_r = random.random(11)
        self.fnet = []
        self.X = 0
        self.Y = 0
        self.hata_payi = float(input("Hata payi nedir? : "))
        self.c = -1
        self.a = 0
        self.hata = 0
        self.Sm = 0
        self.lamda = 0.5
        self.delta = 0.8
        self.b = 0
        self.d = 0
        self.eski_fnet = []
        self.eski_ag_agirlik = []
        self.S = []
        self.g = 0
        self.h = 0
        self.j = 0
        self.i = 0
        self.sayac = 0
        self.saniye = 0

    def ata(self):
        for i in range(0, 11):
            self.X = self.ag_agirlik_r[i]
            self.ag_agirlik.append(self.X)

    def dongu(self):
        while(True):
            ilk.ilkfnethesapla()

    def ilkfnethesapla(self):
        self.sayac = self.sayac + 1
        for i in range(3):
            X = self.ilk_giris[self.g] * self.ag_agirlik[self.a] + self.ilk_giris[self.g + 1] * self.ag_agirlik[self.a + 1] + self.ilk_giris[self.g + 2] * self.ag_agirlik[self.a + 2] + self.ilk_giris[self.g + 3] * self.ag_agirlik[self.a + 3]
            Y = 1 / (1 + math.exp(-X))
            self.fnet.append(Y)
        for i in range(4):
            self.X = self.ilk_giris[0]
            self.ilk_giris.append(self.X)
            del self.ilk_giris[0]
        ilk.sonfnethesapla()

    def sonfnethesapla(self):
        self.X = self.fnet[self.g] * self.ag_agirlik[self.a+8] + self.fnet[self.g+1] * self.ag_agirlik[self.a + 9] + self.fnet[self.g+2] * self.ag_agirlik[self.a + 10]
        self.Y = 1 / (1 + math.exp(-(self.X)))
        self.fnet.append(self.Y)
        #print("Son fnet değerleri : ",self.fnet)
        ilk.karsilastir()

    def karsilastir(self):
        self.c = self.c + 1
        if self.c == len(self.hedefDegisken):
            self.c = 0
        if self.hedefDegisken[self.c] - self.hata_payi <= self.fnet[3] <= self.hedefDegisken[self.c] + self.hata_payi:
            print("Olması gereken değer : ",self.hedefDegisken[self.c])
            print("Bulunan değerr : ", self.fnet[3],self.fnet)
            print(self.sayac, '. seferde Makine Doğru Cevabı Verdi')
            ilk.ilkgeridonus()
        else:
            print(self.sayac,'.sefer dönüyor')
            print("Olması gereken değer : ",self.hedefDegisken[self.c])
            print("Bulunan değer : ", self.fnet[3])
            ilk.ilkgeridonus()
    def ilkgeridonus(self):
        self.hata = self.hedefDegisken[self.c] - self.fnet[3]
        self.Sm = self.fnet[3] * (1 - self.fnet[3]) * self.hata
        #print("Sm : ", self.Sm," | ", "Hata(Em) : ", self.hata)
        self.b = self.b+1
        if self.b == 1:
            for i in range(0,3):
                self.X = self.lamda * self.Sm * self.fnet[i]
                self.Y = self.fnet[i] + self.X
                self.eski_fnet.append(self.fnet[0])
                del self.fnet[0]
                self.fnet.append(self.Y)
            self.eski_fnet.append(self.fnet[0])
            del self.fnet[0]
        else:
            for i in range(0,3):
                self.X = self.lamda * self.Sm * self.fnet[i] + self.delta * self.eski_fnet[i]
                self.Y = self.fnet[i] + self.X
                self.eski_fnet.append(self.fnet[i])
                self.fnet.append(self.Y)
                self.eski_fnet.pop(0)
                del self.fnet[0]
            self.eski_fnet.pop(0)
            self.eski_fnet.append(self.fnet[0])
            del self.fnet[0]
        #print("Eski fnet değerleri : ",self.eski_fnet)
        self.ag_agirlik.extend(self.fnet)
        ilk.ikifnethesapla()
    def ikifnethesapla(self):
        self.d = self.d + 1
        for i in range(0,2):
            self.X = (self.eski_fnet[i] * (1 - self.eski_fnet[i]) * self.Sm * self.eski_fnet[i])
            self.S.append(self.X)
        if self.d == 1:
            for i in range(0,8):
                self.X = self.lamda * self.S[self.j] * self.ilk_giris[self.h]
                self.Y = self.ag_agirlik[i] + self.X
                self.ag_agirlik.append(self.Y)
                self.h = self.h + 1
                if self.h == 3:
                    self.h = 0
                if self.h == 4:
                    self.j = self.j + 1
        else:
            for i in range(0,8):
                self.X = self.lamda * self.S[self.j] * self.ilk_giris[self.h] + self.delta * self.eski_ag_agirlik[i]
                self.Y = self.ag_agirlik[i] + self.X
                self.ag_agirlik.append(self.Y)
                self.h = self.h + 1
                if self.h == 3:
                    self.h = 0
                if self.h == 4:
                    self.j = self.j + 1
        self.h = 0
        for i in range(11):
            self.X = self.ag_agirlik[0]
            self.ag_agirlik.pop(0)
            self.eski_ag_agirlik.append(self.X)
        for i in range(4):
            self.X = self.ilk_giris[0]
            self.ilk_giris.pop(0)
            self.ilk_giris.append(self.X)
        self.fnet.clear()

        #print("Yeni ağ ağırlık değerleri : ", self.ag_agirlik)

ilk = Ysa()
ilk.ata()
ilk.dongu()

