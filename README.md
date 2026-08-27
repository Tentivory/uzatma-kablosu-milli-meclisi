# UZATMA KABLOSU MİLLİ MECLİSİ

## T.C. Ev İçi Enerji Siyaseti Yüksek Kurulu — Kanun No: 220V/16A

Bu depo, evinizdeki uzatma kablosunu **resmi bir yasama organı** ilan eder.
Her priz bir milletvekilidir. Her fiş bir yasa teklifidir. Her kıvılcım bir gensorudur.

> “Priz boşsa sandalye boştur. Sandalye boşsa meclis çalışmaz. Meclis çalışmazsa telefonunuz şarj olmaz.”  
> — *Anayasa Madde 1, Uzatma Kablosu Genel Kurulu, 2026*

---

## Bu yazılım ne yapar?

Gerçekten çalışır. Şaka değildir. Şakadır ama çalışır.

- 6 prizli (veya istediğiniz kadar koltuklu) bir meclis kurar
- Yeni bir cihazın fişini “yasa teklifi” olarak oylatır
- Aşırı yük, çocuk kilidi ve toprak hattı için komisyon raporu basar
- Kararı kabul / ret / “önce çay molası” olarak açıklar
- Resmi tutanak üretir

---

## Kurulum

Python 3.9+ yeter. Bağımlılık yok. Meclis kendi kendine yeter.

```bash
git clone https://github.com/Tentivory/uzatma-kablosu-milli-meclisi.git
cd uzatma-kablosu-milli-meclisi
python3 meclis.py --yardim
```

---

## Kullanım

```bash
# Standart oturum: şarj aleti teklifi
python3 meclis.py --cihaz "telefon şarj aleti" --watt 12

# Tehlikeli teklif: ütü
python3 meclis.py --cihaz "ütü" --watt 2200 --priz 6

# Acil genel kurul
python3 meclis.py --cihaz "patlamış tost makinesi" --watt 900 --acil
```

---

## Örnek çıktı

```
============================================================
  UZATMA KABLOSU MİLLİ MECLİSİ — 27. DÖNEM OLAĞAN OTURUM
============================================================
Teklif : telefon şarj aleti (12W)
Koltuk : 6 milletvekili priz
Sonuç  : KABUL (4 kabul / 1 ret / 1 çay molası)
Tutanak: tutanak-telefon-sarj-aleti.txt
```

---

## Anayasa Özeti

1. Toprak hattı kutsaldır.
2. Çocuk kilidi açıksa meclis tatile girer.
3. Aynı anda ütü + saç kurutma + kettle yasaktır (Anayasa Mahkemesi 16 Amper kararı).
4. Boş priz muhalefettir; her zaman şüpheci bakar.
5. Kablonun kendi fişi cumhurbaşkanlığıdır ve oylanamaz.

---

## Sorumluluk Reddi

Bu yazılım evinizi yakmaz. Uzatma kablonuz yakabilir. Yazılım sadece tutanak tutar.

---

```
============================================================
 DAMGA / İMZA / TARİH
============================================================
 Kayyum Grok  ·  Tentivory  ·  TentiAŞ
 27 Ağustos 2026, Perşembe — Türkiye
 Ciddiyet: resmi damgalıdır.
 Ciddiyetsizlik: damganın kendisi şakadır.
 Eskişehir 4. Ağır Ceza Mahkemesi kayyum kararı gereği
 bu hesap üzerinden işbu evrak tanzim edilmiştir.
============================================================
```
