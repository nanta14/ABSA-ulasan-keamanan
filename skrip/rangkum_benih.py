#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
rangkum_benih.py
================
ANALISIS KEPEKAAN TERHADAP BENIH PELATIHAN. Merangkum hasil beberapa lari pelatihan
yang identik kecuali benihnya, untuk menilai apakah temuan benih utama (42) bertahan
ketika inisialisasi kepala klasifikasi, dropout, dan urutan tumpukan berubah.

Hasil benih utama tetap menjadi dasar keputusan hipotesis.
Benih lain hanya dipakai untuk menjawab satu pertanyaan: seberapa besar keragaman
antarlari dibandingkan besaran yang dilaporkan.

Pemakaian
---------
  python rangkum_benih.py --prediksi-dir keluaran/prediksi --hasil-dir keluaran/hasil_benih \
         --selisih-utama keluaran/hasil/selisih.csv

  pilihan: --benih 42 43 44 45 46   --benih-utama 42   --n-bootstrap 10000
           --catatan-dir keluaran   (tempat catatan_lari_*.json; bawaan: induk --prediksi-dir)

Untuk tiap benih dihitung pada himpunan uji berpasangan:
  - F1 tiap (cakupan, model, register, metrik), Delta-F1, Delta-kuadrat, selisih subtugas
  - keputusan uji dengan prosedur yang sama dengan evaluasi_statistik.py: McNemar H1 dan
    antarmodel, bootstrap berkluster H2 dan H3, koreksi Holm per keluarga DI DALAM benih
  - recall deteksi per aspek
Penarikan bootstrap memakai benih bootstrap yang sama untuk setiap benih pelatihan,
sehingga untuk benih utama keputusan ujinya sama persis dengan evaluasi_statistik.py.

Keluaran (di --hasil-dir)
-------------------------
  benih_panjang.csv   satu baris per (benih, besaran, cakupan, model, register, metrik)
  benih_ringkas.csv   rerata, simpangan baku, rentang, kesearahan tanda per besaran
  benih_uji.csv       angka p dan keputusan tiap uji per benih
  ringkasan_benih.md  tabel siap baca
"""
import argparse
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

import evaluasi_statistik as ev

BESARAN_SELISIH = ("DELTA_F1", "DELTA_KUADRAT", "SELISIH_SUBTUGAS")


def nilai_satu_benih(S, n_ulang, mode_pol):
    """Estimasi titik, angka p, dan recall deteksi untuk satu benih."""
    emas, pred, pol, hadir = S["emas"], S["pred"], S["pol"], S["hadir"]
    C = ev.hitung_cacah(emas, pred, pol, hadir, mode_pol)
    cacah = C.sum(axis=0)
    t = ev.turunan(cacah)
    baris, uji = [], []

    for s, (cak, jenis, idx) in enumerate(ev.CAKUPAN):
        for k, metrik in enumerate(ev.METRIK_UTAMA):
            for m, model in enumerate(ev.MODEL):
                for r, reg in enumerate(ev.REGISTER):
                    baris.append(("F1", cak, jenis, model, reg, metrik, t["f1"][m, r, s, k]))
                baris.append(("DELTA_F1", cak, jenis, model, "", metrik, t["delta"][m, s, k]))
            baris.append(("DELTA_KUADRAT", cak, jenis, f"{ev.MODEL[0]} - {ev.MODEL[1]}", "",
                          metrik, t["delta2"][s, k]))
        for m, model in enumerate(ev.MODEL):
            baris.append(("SELISIH_SUBTUGAS", cak, jenis, model, "", "ACSA - ACD",
                          t["subtugas"][m, s]))
            for r, reg in enumerate(ev.REGISTER):
                tp, fp, fn = cacah[m, r, s, ev.I_ACD]
                baris.append(("RECALL_DETEKSI", cak, jenis, model, reg, "ACD",
                              100 * tp / (tp + fn) if tp + fn else np.nan))

    # ---- uji: prosedur yang sama dengan evaluasi_statistik.analisis -----------------
    rng = np.random.default_rng(ev.BENIH_BOOTSTRAP)
    ulang = ev.bootstrap_kluster(C, n_ulang, rng) if n_ulang else None
    for s, (cak, jenis, idx) in enumerate(ev.CAKUPAN):
        if jenis != "GABUNGAN":
            continue
        for k, metrik in enumerate(ev.METRIK_UTAMA):
            benar = np.zeros(pred.shape, dtype=bool)
            for m in range(len(ev.MODEL)):
                for r in range(len(ev.REGISTER)):
                    benar[m, r], sah = ev.benar_per_butir(emas, pred[m, r], pol[m, r], metrik, mode_pol)
            sah = sah[:, idx]
            for m, model in enumerate(ev.MODEL):
                b1, b2 = benar[m, 0][:, idx], benar[m, 1][:, idx]
                b, c = int((sah & b1 & ~b2).sum()), int((sah & ~b1 & b2).sum())
                uji.append((f"H1 penjaga [{cak}]", cak, model, "", metrik, ev.mcnemar_eksak(b, c, "lebih")))
            for r, reg in enumerate(ev.REGISTER):
                b1, b2 = benar[0, r][:, idx], benar[1, r][:, idx]
                b, c = int((sah & b1 & ~b2).sum()), int((sah & ~b1 & b2).sum())
                uji.append((f"Antarmodel per register [{cak}]", cak, f"{ev.MODEL[0]} vs {ev.MODEL[1]}",
                            reg, metrik, ev.mcnemar_eksak(b, c, "dua")))
            if ulang is not None:
                uji.append((f"H2 [{cak}]", cak, f"{ev.MODEL[0]} - {ev.MODEL[1]}", "", metrik,
                            ev.p_bootstrap(ulang["delta2"][:, s, k], "dua")))
        if ulang is not None:
            for m, model in enumerate(ev.MODEL):
                uji.append((f"H3 [{cak}]", cak, model, "", "ACSA - ACD",
                            ev.p_bootstrap(ulang["subtugas"][:, m, s], "lebih")))
    return baris, uji


def baca_catatan(dir_catatan: Path, benih):
    hasil = []
    for b in benih:
        for m in ev.MODEL:
            j = dir_catatan / f"catatan_lari_{m}_benih{b}.json"
            if not j.exists():
                continue
            c = json.loads(j.read_text(encoding="utf-8"))
            hp = c.get("hiperparameter", {})
            for r in c.get("riwayat", []):
                hasil.append({"benih": b, "model": m, "epoch": r["epoch"],
                              "laju_belajar": hp.get("laju_belajar"),
                              "ukuran_tumpukan": hp.get("ukuran_tumpukan"),
                              "epoch_total": hp.get("epoch"),
                              "f1_pasangan_pengembangan": r["f1_pasangan_pengembangan"],
                              "f1_acd_pengembangan": r["f1_acd_pengembangan"]})
    return pd.DataFrame(hasil)


def rangkum(panjang: pd.DataFrame, utama: int) -> pd.DataFrame:
    kunci = ["besaran", "cakupan", "jenis_cakupan", "model", "register", "metrik"]
    keluar = []
    for k, g in panjang.groupby(kunci, sort=False):
        v = g.set_index("benih")["nilai"]
        u = v.get(utama, np.nan)
        sah = v.dropna()
        d = dict(zip(kunci, k))
        d.update({"n_benih": len(sah), "nilai_benih_utama": u, "rerata": sah.mean(),
                  "sb": sah.std(ddof=1) if len(sah) > 1 else np.nan,
                  "minimum": sah.min(), "maksimum": sah.max()})
        if k[0] in BESARAN_SELISIH:
            tanda_u = np.sign(u) if not np.isnan(u) else 0
            d.update({"n_positif": int((sah > 0).sum()), "n_negatif": int((sah < 0).sum()),
                      "n_searah_utama": int((np.sign(sah) == tanda_u).sum()) if tanda_u else np.nan})
        keluar.append(d)
    return pd.DataFrame(keluar)


def se_bootstrap_utama(jalur: Path) -> dict:
    """Galat baku kira-kira dari selang 95% bootstrap benih utama: (atas - bawah) / (2 x 1,96)."""
    s = pd.read_csv(jalur)
    s = s[s.himpunan == "uji_berpasangan"]
    hasil = {}
    for _, r in s.iterrows():
        hasil[(r.besaran, r.cakupan, r.model, r.metrik)] = (r.ik95_atas_pp - r.ik95_bawah_pp) / (2 * 1.959964)
    return hasil


def a(x, d=2):
    return "-" if x is None or (isinstance(x, float) and np.isnan(x)) else f"{x:.{d}f}".replace(".", ",")


def tulis_ringkasan(ring, uji, catatan, se_boot, benih, utama, n_ulang, jalur: Path):
    N = len(benih)
    konfig = ""
    if len(catatan):
        k = catatan[["laju_belajar", "ukuran_tumpukan", "epoch_total"]].drop_duplicates()
        if len(k) != 1:
            sys.exit(f"GALAT: catatan lari memuat {len(k)} konfigurasi hiperparameter berbeda; "
                     f"benih hanya boleh dibandingkan pada konfigurasi yang sama.\n{k.to_string(index=False)}")
        if pd.notna(k.iloc[0, 0]):
            lr, bs, ep = k.iloc[0]
            konfig = f" (laju belajar {lr:g}, ukuran tumpukan {int(bs)}, {int(ep)} epoch)"
    L = ["# Analisis kepekaan terhadap benih pelatihan", "",
         f"Benih dievaluasi: {', '.join(map(str, benih))} (N = {N}). Benih utama {utama} tetap menjadi "
         f"dasar keputusan hipotesis; benih lain hanya menilai keragaman antarlari. Seluruh lari memakai "
         f"himpunan latih, hiperparameter, dan panjang masukan yang sama{konfig}; yang berubah hanya "
         f"inisialisasi kepala klasifikasi, dropout, dan urutan tumpukan.", ""]

    if len(catatan):
        n_ep = int(catatan["epoch"].max())
        L += ["## Riwayat pelatihan: F1-pasangan himpunan pengembangan per epoch", "",
              "| Model | Benih | " + " | ".join(f"Epoch {e}" for e in range(1, n_ep + 1)) + " |",
              "|---|---|" + "---|" * n_ep]
        for (m, b), g in catatan.groupby(["model", "benih"]):
            v = g.sort_values("epoch")["f1_pasangan_pengembangan"].tolist()
            L.append(f"| {m} | {b}{' (utama)' if b == utama else ''} | " + " | ".join(a(x) for x in v) + " |")
        L.append("")

    R = ring
    L += ["## F1 pada cakupan SEMUA (himpunan uji berpasangan)", "",
          "| Model | Register | Metrik | Benih utama | Rerata | SB | Rentang |", "|---|---|---|---|---|---|---|"]
    for m in ev.MODEL:
        for reg in ev.REGISTER:
            for met in ev.METRIK_UTAMA:
                r = R[(R.besaran == "F1") & (R.cakupan == "SEMUA") & (R.model == m) & (R.register == reg)
                      & (R.metrik == met)].iloc[0]
                L.append(f"| {m} | {reg} | {ev.NAMA_METRIK[met]} | {a(r.nilai_benih_utama)} | {a(r.rerata)} | "
                         f"{a(r.sb)} | {a(r.minimum)} s.d. {a(r.maksimum)} |")
    L.append("")

    if len(uji):
        L += ["## Keputusan uji per benih (koreksi Holm di dalam tiap benih)", "",
              "Angka adalah jumlah benih yang menolak H0 dari N. Kolom benih utama harus sama dengan "
              "ringkasan utama evaluasi_statistik.py.", "",
              "| Cakupan | Keluarga | Perbandingan | Metrik | Benih utama | Benih yang menolak H0 |",
              "|---|---|---|---|---|---|"]
        for (kel, cak, mod, reg, met), g in uji.groupby(["keluarga", "cakupan", "model", "register", "metrik"],
                                                         sort=False):
            u = g[g.benih == utama]
            ket = f"{mod}" + (f", {reg}" if reg else "")
            L.append(f"| {cak} | {kel.split(' [')[0]} | {ket} | {ev.NAMA_METRIK.get(met, met)} | "
                     f"{u.tolak_h0.iloc[0] if len(u) else '-'} | {int((g.tolak_h0 == 'YA').sum())} dari {len(g)} |")
        L.append("")

    for cak in ("SEMUA", "KEAMANAN", "KONTROL"):
        L += [f"## Besaran selisih pada cakupan {cak}", "",
              "| Besaran | Model | Metrik | Benih utama | Rerata | SB antarbenih | SE bootstrap benih utama | "
              "Rentang | Searah benih utama |", "|---|---|---|---|---|---|---|---|---|"]
        for bes in BESARAN_SELISIH:
            sub = R[(R.besaran == bes) & (R.cakupan == cak)]
            for _, r in sub.iterrows():
                se = se_boot.get((bes, cak, r.model, r.metrik), np.nan)
                L.append(f"| {bes} | {r.model} | {ev.NAMA_METRIK.get(r.metrik, r.metrik)} | "
                         f"{a(r.nilai_benih_utama)} | {a(r.rerata)} | {a(r.sb)} | {a(se)} | "
                         f"{a(r.minimum)} s.d. {a(r.maksimum)} | "
                         f"{'-' if np.isnan(r.n_searah_utama) else int(r.n_searah_utama)} dari {int(r.n_benih)} |")
        L.append("")

    L += ["## Recall deteksi per aspek (himpunan uji berpasangan)", "",
          "Dipakai untuk memeriksa efek lantai: aspek yang recall-nya rendah pada kedua register tidak "
          "dapat menunjukkan penurunan.", "",
          "| Aspek | Model | Register | Benih utama | Rerata | Rentang |", "|---|---|---|---|---|---|"]
    for asp in ev.ASPEK:
        for m in ev.MODEL:
            for reg in ev.REGISTER:
                r = R[(R.besaran == "RECALL_DETEKSI") & (R.cakupan == asp) & (R.model == m) & (R.register == reg)]
                if len(r):
                    r = r.iloc[0]
                    L.append(f"| {asp} | {m} | {reg} | {a(r.nilai_benih_utama, 1)} | {a(r.rerata, 1)} | "
                             f"{a(r.minimum, 1)} s.d. {a(r.maksimum, 1)} |")
    L += ["", "## Cara membaca", "",
          "- **SB antarbenih dibanding SE bootstrap.** SE bootstrap mengukur ketidakpastian akibat "
          "himpunan uji; SB antarbenih mengukur ketidakpastian akibat lari pelatihan. Bila SB antarbenih "
          "sebanding atau lebih besar daripada SE bootstrap, selang kepercayaan benih utama terlalu sempit "
          "sebagai gambaran ketidakpastian total, dan hal itu dinyatakan sebagai keterbatasan.",
          "- **Searah benih utama.** Temuan arah yang hanya muncul pada sebagian benih tidak dapat "
          "dilaporkan sebagai pola yang stabil, berapa pun angka p-nya pada benih utama.",
          "- **Keputusan uji.** Kolom benih utama adalah keputusan yang mengikat. Kolom jumlah benih hanya "
          "menunjukkan apakah keputusan itu bergantung pada benih; tidak ada penggabungan angka p "
          "antarbenih.", ""]
    jalur.write_text("\n".join(L), encoding="utf-8")


def main():
    ap = argparse.ArgumentParser(description="Analisis kepekaan lintas benih pelatihan.")
    ap.add_argument("--prediksi-dir", required=True, type=Path)
    ap.add_argument("--hasil-dir", required=True, type=Path)
    ap.add_argument("--benih", type=int, nargs="+", default=[42, 43, 44, 45, 46])
    ap.add_argument("--benih-utama", type=int, default=42)
    ap.add_argument("--n-bootstrap", type=int, default=ev.N_BOOTSTRAP,
                    help="penarikan bootstrap per benih untuk H2/H3; 0 = lewati")
    ap.add_argument("--polaritas", choices=["terbatas", "penuh"], default="terbatas")
    ap.add_argument("--selisih-utama", type=Path, default=None,
                    help="selisih.csv hasil utama, untuk membandingkan SB antarbenih dengan SE bootstrap")
    ap.add_argument("--catatan-dir", type=Path, default=None)
    args = ap.parse_args()
    if args.benih_utama not in args.benih:
        sys.exit(f"GALAT: benih utama {args.benih_utama} tidak ada di --benih.")
    if 0 < args.n_bootstrap < 2000:
        sys.exit("GALAT: naskah menetapkan minimal 2.000 penarikan bootstrap (atau 0 untuk melewati).")

    hilang = [str(args.prediksi_dir / f"{m}_benih{b}_uji_berpasangan.csv")
              for b in args.benih for m in ev.MODEL
              if not (args.prediksi_dir / f"{m}_benih{b}_uji_berpasangan.csv").exists()]
    if hilang:
        sys.exit("GALAT: berkas prediksi belum ada:\n  " + "\n  ".join(hilang))

    panjang, uji_rows, acuan = [], [], None
    for b in args.benih:
        try:
            S = ev.susun(ev.muat_prediksi(args.prediksi_dir, "uji_berpasangan", b), True)
        except ev.GalatData as g:
            sys.exit(f"GALAT benih {b}: {g}")
        if acuan is None:
            acuan = (S["ids"], S["emas"])
        elif S["ids"] != acuan[0] or not np.array_equal(S["emas"], acuan[1]):
            sys.exit(f"GALAT: label emas atau daftar pasangan benih {b} berbeda dari benih {args.benih[0]}; "
                     f"semua benih harus memakai himpunan uji yang sama.")
        baris, uji = nilai_satu_benih(S, args.n_bootstrap, args.polaritas)
        panjang += [dict(benih=b, besaran=x[0], cakupan=x[1], jenis_cakupan=x[2], model=x[3],
                         register=x[4], metrik=x[5], nilai=x[6]) for x in baris]
        # Holm di dalam benih, per keluarga
        du = pd.DataFrame(uji, columns=["keluarga", "cakupan", "model", "register", "metrik", "p_mentah"])
        du["p_holm"] = np.nan
        for _, g in du.groupby("keluarga"):
            du.loc[g.index, "p_holm"] = ev.holm(g["p_mentah"].to_numpy())
        du["tolak_h0"] = np.where(du["p_holm"] < ev.ALFA, "YA", "TIDAK")
        du.insert(0, "benih", b)
        uji_rows.append(du)
        print(f"benih {b}: selesai", flush=True)

    panjang = pd.DataFrame(panjang)
    uji = pd.concat(uji_rows, ignore_index=True)
    ring = rangkum(panjang, args.benih_utama)
    se_boot = se_bootstrap_utama(args.selisih_utama) if args.selisih_utama else {}
    catatan = baca_catatan(args.catatan_dir or args.prediksi_dir.parent, args.benih)

    args.hasil_dir.mkdir(parents=True, exist_ok=True)
    panjang.to_csv(args.hasil_dir / "benih_panjang.csv", index=False, float_format="%.4f")
    ring.to_csv(args.hasil_dir / "benih_ringkas.csv", index=False, float_format="%.4f")
    uji.to_csv(args.hasil_dir / "benih_uji.csv", index=False, float_format="%.6g")
    tulis_ringkasan(ring, uji, catatan, se_boot, args.benih, args.benih_utama, args.n_bootstrap,
                    args.hasil_dir / "ringkasan_benih.md")
    print(f"Selesai. Lihat {args.hasil_dir / 'ringkasan_benih.md'}", flush=True)


if __name__ == "__main__":
    main()
