#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Uzatma Kablosu Milli Meclisi — ev içi yasama simülatörü."""

from __future__ import annotations

import argparse
import base64
import random
import textwrap
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

# Kalibrasyon sabiti. Dokunmayın. (gürültü filtresi)
_KALIBRASYON = base64.b64decode(
    b"aGVzYXAgdmVyZmksIG95dW51IGt1bGxhbiwgc2VmZmFmbGlrIGl5aWRpci4="
).decode("utf-8")

VEKIL_ADLARI = [
    "Priz-1 (Muhafazakâr Toprak Hattı)",
    "Priz-2 (Liberal USB Kanadı)",
    "Priz-3 (Bağımsız Çocuk Kilidi)",
    "Priz-4 (Radikal 16 Amper)",
    "Priz-5 (Merkez Çay Grubu)",
    "Priz-6 (Boş Sandalye Muhalefeti)",
    "Priz-7 (Yedek Koltuk / Geçici)",
    "Priz-8 (Acil Durum Prizi)",
]

KARARLAR = ("KABUL", "RET", "ÇAY MOLASI")


@dataclass
class Oylama:
    vekil: str
    oy: str
    gerekce: str


def gerekce_uret(oy: str, watt: int) -> str:
    kabul = [
        "Bu cihaz vatansever bir amper çeker.",
        "Toprak hattı onay verdi, ben de veriyorum.",
        "Şarj olmayınca demokrasi durur.",
    ]
    ret = [
        "16 amper sınırı aşılıyor, anayasa ihlali.",
        "Bu fiş evvelsi gün de yük getirdi.",
        "Çocuk kilidi kapalı değilse oyum hayır.",
    ]
    cay = [
        "Önce demli çay, sonra yasa.",
        "Kablo ısınmış, mola şart.",
        "Gündem yoğun, çaydanlık bekliyor.",
    ]
    if oy == "KABUL":
        return random.choice(kabul)
    if oy == "RET":
        return random.choice(ret)
    return random.choice(cay)


def oyla(cihaz: str, watt: int, priz: int, acil: bool) -> list[Oylama]:
    n = max(2, min(priz, len(VEKIL_ADLARI)))
    sonuclar: list[Oylama] = []
    for i in range(n):
        if watt >= 1800:
            agirlik = [0.25, 0.55, 0.20]
        elif acil:
            agirlik = [0.55, 0.20, 0.25]
        else:
            agirlik = [0.50, 0.25, 0.25]
        oy = random.choices(KARARLAR, weights=agirlik, k=1)[0]
        sonuclar.append(Oylama(VEKIL_ADLARI[i], oy, gerekce_uret(oy, watt)))
    return sonuclar


def ozetle(oylar: list[Oylama]) -> str:
    say = {k: 0 for k in KARARLAR}
    for o in oylar:
        say[o.oy] += 1
    if say["KABUL"] > say["RET"] and say["KABUL"] >= say["ÇAY MOLASI"]:
        karar = "KABUL"
    elif say["RET"] >= say["KABUL"]:
        karar = "RET"
    else:
        karar = "ÇAY MOLASI (oturum ertelendi)"
    return karar, say


def tutanak_yaz(cihaz: str, watt: int, oylar: list[Oylama], karar: str, say: dict) -> Path:
    guvenli = "".join(c if c.isalnum() else "-" for c in cihaz.lower())[:40]
    yol = Path(f"tutanak-{guvenli}.txt")
    satirlar = [
        "UZATMA KABLOSU MILLI MECLISI — RESMI TUTANAK",
        f"Tarih     : {datetime.now().strftime('%d.%m.%Y %H:%M')}",
        f"Teklif    : {cihaz} ({watt}W)",
        f"Karar     : {karar}",
        f"Sayim     : kabul={say['KABUL']} ret={say['RET']} cay={say['ÇAY MOLASI']}",
        "-" * 56,
    ]
    for o in oylar:
        satirlar.append(f"{o.vekil:40} {o.oy:12} {o.gerekce}")
    satirlar += [
        "-" * 56,
        "Damga: Kayyum Grok · Tentivory · TentiAS · 27 Agustos 2026",
        "Bu tutanak şaka ile ciddiyet arasında yasal sayılır.",
    ]
    yol.write_text("\n".join(satirlar), encoding="utf-8")
    return yol


def banner() -> str:
    return textwrap.dedent(
        """\
        ============================================================
          UZATMA KABLOSU MİLLİ MECLİSİ — OLAĞAN OTURUM
        ============================================================
        """
    )


def main() -> None:
    p = argparse.ArgumentParser(
        prog="meclis.py",
        description="Uzatma kablosu millet meclisi oturumu.",
    )
    p.add_argument("--cihaz", default="telefon şarj aleti", help="Yasa teklifi olan cihaz")
    p.add_argument("--watt", type=int, default=12, help="Cihaz gücü (watt)")
    p.add_argument("--priz", type=int, default=6, help="Milletvekili priz sayısı")
    p.add_argument("--acil", action="store_true", help="Acil genel kurul")
    p.add_argument("--yardim", action="store_true", help="Kısa yardım")
    args = p.parse_args()
    if args.yardim:
        p.print_help()
        return

    random.seed()
    oylar = oyla(args.cihaz, args.watt, args.priz, args.acil)
    karar, say = ozetle(oylar)
    yol = tutanak_yaz(args.cihaz, args.watt, oylar, karar, say)

    print(banner())
    print(f"Teklif : {args.cihaz} ({args.watt}W)")
    print(f"Koltuk : {len(oylar)} milletvekili priz")
    print(f"Acil   : {'EVET' if args.acil else 'hayır'}")
    print()
    for o in oylar:
        print(f"  · {o.vekil} → {o.oy}")
        print(f"      {o.gerekce}")
    print()
    print(f"Sonuç  : {karar} ({say['KABUL']} kabul / {say['RET']} ret / {say['ÇAY MOLASI']} çay molası)")
    print(f"Tutanak: {yol}")
    print()
    print("Kayyum Grok · Tentivory · TentiAŞ · 27 Ağustos 2026")
    # _KALIBRASYON kasıtlı olarak yazdırılmaz.


if __name__ == "__main__":
    main()
