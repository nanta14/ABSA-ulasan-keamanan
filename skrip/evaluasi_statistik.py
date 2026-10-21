#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
evaluasi_statistik.py
=====================
Menghitung seluruh angka Bab IV dari PREDIKSI MENTAH PER BUTIR yang ditulis
`latih_prediksi.py`. Tidak memuat model; dapat diulang kapan saja di CPU.

Pemakaian
---------
  python evaluasi_statistik.py --prediksi-dir keluaran/prediksi --hasil-dir keluaran/hasil
  pilihan: --benih 42   --n-bootstrap 10000   --polaritas {terbatas,penuh}
           --tanpa-terpotong   (analisis kepekaan; pakai --hasil-dir lain)

Definisi (Subbab 3.5.4-3.5.5)
-----------------------------
Butir            = satu pasangan (ulasan, aspek). Label: TIDAK_ADA / NEGATIF / POSITIF.
F1-ACD           = F1 kelas ADA; ADA berarti label bukan TIDAK_ADA.
F1-ACSA          = F1 kelas NEGATIF, dihitung HANYA pada butir berlabel emas ADA.
                   Mode "terbatas" (bawaan): keputusan polaritas = argmax atas logit
                   NEGATIF dan POSITIF saja, sehingga kekeliruan deteksi tidak ikut
                   terhitung. Mode "penuh": argmax tiga kelas; prediksi TIDAK_ADA
                   pada butir emas ADA dihitung luput.
F1-pasangan      = F1 atas rangkap (aspek, polaritas): benar hanya bila aspek
                   terdeteksi DAN polaritasnya tepat. Metrik utama.
Agregasi         = mikro: TP/FP/FN dijumlahkan lintas aspek dalam satu cakupan.
Cakupan          = SEMUA (5 aspek), KEAMANAN (3), KONTROL (2), dan tiap aspek.
Delta-F1         = F1(FORMAL) - F1(INFORMAL), per model per metrik. Positif = turun
                   pada ragam takbaku.
Delta-kuadrat    = Delta-F1(IndoBERT) - Delta-F1(IndoBERTweet). Positif = IndoBERT
                   lebih rapuh.
Selisih subtugas = Delta-F1-ACSA - Delta-F1-ACD, per model.

Pengujian (alfa 0,05; koreksi Holm per keluarga, per cakupan gabungan)
----------------------------------------------------------------------
Cakupan SEMUA berstatus KONFIRMATORI: hanya hasilnya yang dipakai untuk menerima
atau menolak H1-H3. Cakupan KEAMANAN dan KONTROL berstatus LANJUTAN (koreksi Holm
di dalam kelompoknya masing-masing). Per aspek berstatus EKSPLORATORI.
H1 penjaga  (6 uji) : McNemar eksak satu arah, dua register dalam satu model.
Antarmodel  (6 uji) : McNemar eksak dua arah, dua model dalam satu register.
H2          (3 uji) : bootstrap berkluster dua arah atas Delta-kuadrat.
H3          (2 uji) : bootstrap berkluster satu arah atas selisih subtugas.
Per aspek           : selang kepercayaan bootstrap saja, tanpa angka p.
Kluster bootstrap   = ULASAN (pasangan): kedua versi register, kelima aspek, dan
                      prediksi kedua model ditarik bersama.
Angka p bootstrap   = pembalikan selang persentil, (1 + #{theta* <= 0}) / (B + 1).

Kelas POSITIF hanya dilaporkan untuk cakupan kelompok yang dukungannya >= 20 butir
pada himpunan uji berpasangan, dan selalu bertanda EKSPLORATORI.

Himpunan uji tak berpasangan = pemeriksaan ketahanan. Kedua register di sana
berisi ulasan yang BERBEDA, jadi selisih antarregister diuji dengan bootstrap
berstrata (bukan McNemar) dan tidak masuk keluarga koreksi Holm mana pun.

--tanpa-terpotong (ANALISIS KEPEKAAN)
-------------------------------------
Membuang setiap pasangan yang salah satu versinya terpotong pada salah satu model
(dan setiap ulasan tak berpasangan yang terpotong pada salah satu model), lalu
mengulang seluruh perhitungan. Seluruh status menjadi KEPEKAAN; hasil ini tidak
dipakai untuk menerima atau menolak hipotesis. Aturan pelaporan kelas POSITIF tetap
ditentukan dari himpunan berpasangan yang utuh.

Keluaran
--------
  kinerja.csv     F1 tiap (himpunan, cakupan, model, register, metrik) + selang 95%
  selisih.csv     Delta-F1, Delta-kuadrat, selisih subtugas + selang + keputusan uji
  mcnemar.csv     tabel kontingensi lengkap tiap uji McNemar
  kekeliruan.csv  sebaran kekeliruan (luput, muncul palsu, polaritas terbalik) dan
                  recall kelas NEGATIF ujung-ke-ujung per aspek dan per kelompok
  ringkasan.md    tabel siap baca untuk Bab IV
"""
import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import binom, norm

MODEL = ["indobert", "indobertweet"]      # urutan menentukan tanda Delta-kuadrat
REGISTER = ["FORMAL", "INFORMAL"]         # urutan menentukan tanda Delta-F1
ASPEK = ["keamanan_akun", "autentikasi", "privasi_data", "antarmuka", "keandalan"]
LABEL = ["TIDAK_ADA", "NEGATIF", "POSITIF"]
KELOMPOK = {"KEAMANAN": ["keamanan_akun", "autentikasi", "privasi_data"],
            "KONTROL": ["antarmuka", "keandalan"]}
METRIK = ["ACD", "ACSA", "PASANGAN", "ACSA_POS"]
METRIK_UTAMA = ["ACD", "ACSA", "PASANGAN"]
ALFA = 0.05
AMBANG_DUKUNGAN_POSITIF = 20
N_BOOTSTRAP = 10000                       # naskah: minimal 2.000
CAKUPAN_KONFIRMATORI = "SEMUA"            # Subbab 3.5.5: agregat atas seluruh kategori aspek
BENIH_BOOTSTRAP = 42
MODE_KEPEKAAN = False                     # diatur oleh --tanpa-terpotong

CAKUPAN = ([("SEMUA", "GABUNGAN", list(range(len(ASPEK))))]
           + [(g, "GABUNGAN", [ASPEK.index(a) for a in anggota]) for g, anggota in KELOMPOK.items()]
           + [(a, "ASPEK", [j]) for j, a in enumerate(ASPEK)])
I_ACD, I_ACSA = METRIK.index("ACD"), METRIK.index("ACSA")


# =============================================================================
# FUNGSI PENENTU ANGKA (diuji di test_evaluasi.py)
# =============================================================================
def indikator(emas, pred, pol, metrik, mode_pol="terbatas"):
    """Mengembalikan (TP, FP, FN) boolean per butir untuk satu metrik.

    emas, pred : kode kelas 0/1/2 (TIDAK_ADA/NEGATIF/POSITIF)
    pol        : keputusan polaritas terbatas (1/2), dari argmax dua logit polaritas
    """
    ada_e, ada_p = emas != 0, pred != 0
    if metrik == "ACD":
        return ada_e & ada_p, ~ada_e & ada_p, ada_e & ~ada_p
    if metrik == "PASANGAN":
        tepat = pred == emas
        # polaritas keliru pada aspek yang terdeteksi = satu FP dan satu FN sekaligus
        return ada_e & tepat, ada_p & ~tepat, ada_e & ~tepat
    kelas = 1 if metrik == "ACSA" else 2
    kep = pol if mode_pol == "terbatas" else pred
    return (ada_e & (emas == kelas) & (kep == kelas),
            ada_e & (emas != kelas) & (kep == kelas),
            ada_e & (emas == kelas) & (kep != kelas))


def benar_per_butir(emas, pred, pol, metrik, mode_pol="terbatas"):
    """Keputusan benar/salah per butir untuk McNemar, beserta topeng butir yang sah."""
    if metrik == "ACD":
        return (emas != 0) == (pred != 0), np.ones_like(emas, dtype=bool)
    if metrik == "PASANGAN":
        return pred == emas, np.ones_like(emas, dtype=bool)
    kep = pol if mode_pol == "terbatas" else pred
    return kep == emas, emas != 0            # ACSA: hanya butir emas ADA


def f1_dari(tp, fp, fn):
    """F1 = 2TP / (2TP + FP + FN); NaN bila penyebut nol."""
    tp, fp, fn = (np.asarray(x, dtype=float) for x in (tp, fp, fn))
    penyebut = 2 * tp + fp + fn
    with np.errstate(divide="ignore", invalid="ignore"):
        return np.where(penyebut > 0, 2 * tp / penyebut, np.nan)


def mcnemar_eksak(b, c, arah="dua"):
    """Uji McNemar eksak (binomial) atas pasangan tak selaras.

    b = benar pada kondisi pertama, salah pada kondisi kedua; c = sebaliknya.
    arah="lebih": H1 kondisi pertama lebih sering benar (satu arah).
    """
    b, c = int(b), int(c)
    n = b + c
    if n == 0:
        return 1.0
    if arah == "lebih":
        return float(binom.sf(b - 1, n, 0.5))
    return float(min(1.0, 2 * binom.cdf(min(b, c), n, 0.5)))


def holm(p):
    """Angka p terkoreksi Holm (step-down), urutan masukan dipertahankan."""
    p = np.asarray(p, dtype=float)
    m = len(p)
    hasil = np.empty(m)
    berjalan = 0.0
    for peringkat, i in enumerate(np.argsort(p, kind="stable")):
        berjalan = max(berjalan, min(1.0, (m - peringkat) * p[i]))
        hasil[i] = berjalan
    return hasil


def p_bootstrap(sebaran, arah="dua"):
    """Angka p untuk H0: theta = 0 dari sebaran bootstrap theta* (pembalikan persentil)."""
    s = np.asarray(sebaran, dtype=float)
    s = s[~np.isnan(s)]
    if len(s) == 0:
        return float("nan")
    bawah = (1 + np.sum(s <= 0)) / (len(s) + 1)      # bukti melawan theta > 0
    atas = (1 + np.sum(s >= 0)) / (len(s) + 1)
    return float(bawah) if arah == "lebih" else float(min(1.0, 2 * min(bawah, atas)))


def selang(sebaran, alfa=ALFA):
    s = np.asarray(sebaran, dtype=float)
    if np.all(np.isnan(s)):
        return float("nan"), float("nan")
    bawah, atas = np.nanpercentile(s, [100 * alfa / 2, 100 * (1 - alfa / 2)])
    return float(bawah), float(atas)


def wilson(k, n, alfa=ALFA):
    """Selang skor Wilson untuk proporsi k/n (persen). NaN bila n = 0."""
    if n == 0:
        return float("nan"), float("nan"), float("nan")
    z = norm.ppf(1 - alfa / 2)
    p = k / n
    pusat = (p + z * z / (2 * n)) / (1 + z * z / n)
    lebar = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    return 100 * p, 100 * max(0.0, pusat - lebar), 100 * min(1.0, pusat + lebar)


def hitung_cacah(emas, pred, pol, hadir, mode_pol="terbatas"):
    """Cacah TP/FP/FN per kluster.

    emas[n, a]; pred, pol[m, r, n, a]; hadir[r, n] (apakah ulasan n punya versi register r)
    -> C[n, m, r, s, k, 3]  dengan s = cakupan, k = metrik
    """
    n = emas.shape[0]
    C = np.zeros((n, len(MODEL), len(REGISTER), len(CAKUPAN), len(METRIK), 3))
    for m in range(len(MODEL)):
        for r in range(len(REGISTER)):
            for k, metrik in enumerate(METRIK):
                trio = indikator(emas, pred[m, r], pol[m, r], metrik, mode_pol)
                for j, x in enumerate(trio):
                    x = x & hadir[r][:, None]
                    for s, (_, _, idx) in enumerate(CAKUPAN):
                        C[:, m, r, s, k, j] = x[:, idx].sum(axis=1)
    return C


def turunan(C):
    """Dari cacah [..., m, r, s, k, 3] ke F1 (persen) dan besaran turunannya."""
    f1 = 100 * f1_dari(C[..., 0], C[..., 1], C[..., 2])          # [..., m, r, s, k]
    delta = f1[..., 0, :, :] - f1[..., 1, :, :]                  # [..., m, s, k]
    delta2 = delta[..., 0, :, :] - delta[..., 1, :, :]           # [..., s, k]
    subtugas = delta[..., I_ACSA] - delta[..., I_ACD]            # [..., m, s]
    G = C.sum(axis=-4)                                           # gabung register
    f1_gab = 100 * f1_dari(G[..., 0], G[..., 1], G[..., 2])      # [..., m, s, k]
    return {"f1": f1, "delta": delta, "delta2": delta2, "subtugas": subtugas, "f1_gab": f1_gab}


def bootstrap_kluster(C, n_ulang, rng, strata=None, potong=1000):
    """Menarik ulang KLUSTER (ulasan) dengan pengembalian; mengembalikan sebaran turunan().

    strata: larik kode strata per kluster; bila diberikan, penarikan dilakukan di dalam
    tiap strata (dipakai pada himpunan tak berpasangan yang registernya saling lepas).
    """
    n = C.shape[0]
    datar = C.reshape(n, -1)
    kelompok = [np.arange(n)] if strata is None else [np.where(strata == g)[0]
                                                      for g in np.unique(strata)]
    bagian = []
    for mulai in range(0, n_ulang, potong):
        b = min(potong, n_ulang - mulai)
        W = np.zeros((b, n))
        for idx in kelompok:
            W[:, idx] = rng.multinomial(len(idx), np.full(len(idx), 1 / len(idx)), size=b)
        bagian.append(turunan((W @ datar).reshape((b,) + C.shape[1:])))
    return {kunci: np.concatenate([x[kunci] for x in bagian]) for kunci in bagian[0]}


def saring_terpotong(S):
    """Membuang ulasan yang salah satu versinya terpotong pada salah satu model.

    Mengembalikan (S baru, jumlah ulasan yang dibuang).
    """
    buang = S["terpotong"].any(axis=(0, 1))                       # [n]
    tetap = ~buang
    S2 = dict(S)
    S2["ids"] = [u for u, t in zip(S["ids"], tetap) if t]
    S2["emas"] = S["emas"][tetap]
    S2["pred"] = S["pred"][:, :, tetap]
    S2["pol"] = S["pol"][:, :, tetap]
    S2["hadir"] = S["hadir"][:, tetap]
    S2["terpotong"] = S["terpotong"][:, :, tetap]
    return S2, int(buang.sum())


def kekeliruan(nama, S):
    """Sebaran kekeliruan per (model, register, cakupan) dan recall kelas NEGATIF.

    Keputusan yang dinilai adalah keputusan tiga kelas (argmax tiga logit).
    luput            : emas ADA, prediksi TIDAK_ADA
    muncul_palsu     : emas TIDAK_ADA, prediksi ADA
    polaritas_terbalik: emas ADA, prediksi ADA, polaritas berbeda
    recall_negatif   : butir emas NEGATIF yang diprediksi NEGATIF / butir emas NEGATIF
    """
    emas, pred, hadir = S["emas"], S["pred"], S["hadir"]
    baris = []
    daftar_r = [(r, reg) for r, reg in enumerate(REGISTER)] if S["ada_register"] else [(0, "SEMUA")]
    for m, model in enumerate(MODEL):
        for r, reg in daftar_r:
            topeng = hadir[r][:, None]
            p = pred[m, r]
            for cak, jenis, idx in CAKUPAN:
                e, q, t = emas[:, idx], p[:, idx], np.broadcast_to(topeng, emas[:, idx].shape)
                ada_e, ada_p = (e != 0) & t, (q != 0) & t
                n_neg = int(((e == 1) & t).sum())
                tp_neg = int(((e == 1) & (q == 1) & t).sum())
                rec, bw, at = wilson(tp_neg, n_neg)
                baris.append({
                    "himpunan": nama, "cakupan": cak, "jenis_cakupan": jenis, "model": model,
                    "register": reg, "n_butir": int(t.sum()), "emas_ada": int(ada_e.sum()),
                    "emas_negatif": n_neg, "emas_positif": int(((e == 2) & t).sum()),
                    "deteksi_tepat": int((ada_e & ada_p).sum()),
                    "luput": int((ada_e & ~ada_p).sum()),
                    "muncul_palsu": int((~(e != 0) & ada_p).sum()),
                    "polaritas_terbalik": int((ada_e & ada_p & (q != e)).sum()),
                    "pasangan_tepat": int((ada_e & (q == e)).sum()),
                    "recall_negatif_persen": rec, "recall_negatif_ik95_bawah": bw,
                    "recall_negatif_ik95_atas": at,
                    "recall_deteksi_persen": (100 * float((ada_e & ada_p).sum()) / ada_e.sum()
                                              if ada_e.sum() else np.nan),
                })
    return baris


# =============================================================================
# PEMUATAN PREDIKSI
# =============================================================================
class GalatData(Exception):
    pass


def muat_prediksi(dir_pred: Path, himpunan: str, benih: int) -> dict:
    hasil = {}
    for m in MODEL:
        jalur = dir_pred / f"{m}_benih{benih}_{himpunan}.csv"
        if not jalur.exists():
            raise GalatData(f"Berkas prediksi tidak ditemukan: {jalur}")
        hasil[m] = pd.read_csv(jalur, dtype=str, keep_default_na=False)
    return hasil


def susun(pred_model: dict, berpasangan: bool) -> dict:
    """Menyusun prediksi panjang menjadi larik dan memeriksa keselarasan kedua model."""
    d0 = pred_model[MODEL[0]]
    ids = sorted(d0["id_ulasan"].unique())
    posisi = {u: i for i, u in enumerate(ids)}
    n, A, M, R = len(ids), len(ASPEK), len(MODEL), len(REGISTER)
    ada_register = set(d0["register"].unique()) <= set(REGISTER)
    if berpasangan and not ada_register:
        raise GalatData("Himpunan berpasangan tanpa kolom register yang sah.")
    kode = {l: i for i, l in enumerate(LABEL)}

    emas = np.full((M, R, n, A), -1)
    pred = np.zeros((M, R, n, A), dtype=int)
    pol = np.ones((M, R, n, A), dtype=int)
    terpotong = np.zeros((M, R, n), dtype=bool)
    isi = np.zeros((M, R, n, A), dtype=int)
    for mi, m in enumerate(MODEL):
        d = pred_model[m]
        if set(d["id_ulasan"]) != set(ids):
            raise GalatData(f"Himpunan pengenal {m} berbeda dari {MODEL[0]}.")
        i = d["id_ulasan"].map(posisi).to_numpy()
        r = (d["register"].map({x: j for j, x in enumerate(REGISTER)}).to_numpy()
             if ada_register else np.zeros(len(d), dtype=int))
        a = d["aspek"].map({x: j for j, x in enumerate(ASPEK)}).to_numpy()
        kol = {k: d[k].map(kode).to_numpy() for k in ("emas", "prediksi", "prediksi_polaritas")}
        if any(pd.isna(x).any() for x in (r, a, *kol.values())):
            raise GalatData(f"Nilai tak dikenal pada berkas prediksi {m}.")
        r, a = r.astype(int), a.astype(int)
        np.add.at(isi[mi], (r, i, a), 1)
        emas[mi, r, i, a] = kol["emas"].astype(int)
        pred[mi, r, i, a] = kol["prediksi"].astype(int)
        pol[mi, r, i, a] = kol["prediksi_polaritas"].astype(int)
        terpotong[mi, r, i] = d["terpotong"].astype(int).to_numpy().astype(bool)

    if isi.max() > 1:
        raise GalatData("Ada butir (ulasan, register, aspek) yang muncul lebih dari sekali.")
    if not (isi[0] == isi[1]).all():
        raise GalatData("Kedua model tidak memprediksi himpunan butir yang sama.")
    hadir = isi[0].all(axis=2).astype(bool)                       # [r, n]
    if not (isi[0].any(axis=2) == hadir).all():
        raise GalatData("Ada ulasan yang tidak lengkap kelima aspeknya.")
    if berpasangan and not hadir.all():
        raise GalatData("Ada pasangan yang tidak memiliki kedua versi register.")
    if not berpasangan and not (hadir.sum(axis=0) == 1).all():
        raise GalatData("Himpunan tak berpasangan: tiap ulasan harus muncul tepat sekali.")

    acuan = np.where(hadir[0][:, None], emas[0, 0], emas[0, 1])  # [n, a]
    for mi in range(M):
        for r in range(R):
            if not (emas[mi, r][hadir[r]] == acuan[hadir[r]]).all():
                raise GalatData("Label emas tidak identik antarmodel atau antarregister.")
    return {"ids": ids, "emas": acuan, "pred": pred, "pol": pol, "hadir": hadir,
            "ada_register": ada_register, "terpotong": terpotong}


# =============================================================================
# ANALISIS SATU HIMPUNAN
# =============================================================================
def analisis(nama, S, berpasangan, lapor_pos, n_ulang, rng, mode_pol):
    emas, pred, pol, hadir = S["emas"], S["pred"], S["pol"], S["hadir"]
    ada_reg = S["ada_register"]
    C = hitung_cacah(emas, pred, pol, hadir, mode_pol)
    titik = turunan(C.sum(axis=0))
    cacah = C.sum(axis=0)                                         # [m, r, s, k, 3]
    strata = None if berpasangan or not ada_reg else hadir[1].astype(int)
    ulang = bootstrap_kluster(C, n_ulang, rng, strata)
    nama_uji_boot = ("bootstrap berkluster (ulasan)" if berpasangan
                     else "bootstrap berstrata register (ulasan)")
    ada_emas = emas != 0

    def status_dasar(jenis, metrik, cak):
        if metrik == "ACSA_POS":
            return "EKSPLORATORI" if lapor_pos.get(cak, False) else "TIDAK_DILAPORKAN"
        if not berpasangan:
            return "KETAHANAN"
        if jenis != "GABUNGAN":
            return "EKSPLORATORI"
        if MODE_KEPEKAAN:
            return "KEPEKAAN"
        return "KONFIRMATORI" if cak == CAKUPAN_KONFIRMATORI else "LANJUTAN"

    def dipakai(jenis, metrik, cak):
        return metrik != "ACSA_POS" or cak in KELOMPOK

    kinerja, selisih, mcnemar = [], [], []

    # ---------------- kinerja ---------------------------------------------------
    for s, (cak, jenis, idx) in enumerate(CAKUPAN):
        for m, model in enumerate(MODEL):
            daftar_r = ([(r, reg) for r, reg in enumerate(REGISTER)] if ada_reg else [])
            if not berpasangan:
                daftar_r.append((None, "SEMUA"))
            for r, reg in daftar_r:
                for k, metrik in enumerate(METRIK):
                    if not dipakai(jenis, metrik, cak):
                        continue
                    st = status_dasar(jenis, metrik, cak)
                    if r is None:
                        tp, fp, fn = cacah[m, :, s, k].sum(axis=0)
                        f1, seb = titik["f1_gab"][m, s, k], ulang["f1_gab"][:, m, s, k]
                        topeng = np.ones(len(emas), dtype=bool)
                    else:
                        tp, fp, fn = cacah[m, r, s, k]
                        f1, seb = titik["f1"][m, r, s, k], ulang["f1"][:, m, r, s, k]
                        topeng = hadir[r]
                    n_ada = int(ada_emas[topeng][:, idx].sum())
                    n_butir = n_ada if metrik.startswith("ACSA") else int(topeng.sum()) * len(idx)
                    bw, at = selang(seb)
                    sembunyi = st == "TIDAK_DILAPORKAN"
                    kinerja.append({
                        "himpunan": nama, "cakupan": cak, "jenis_cakupan": jenis,
                        "model": model, "register": reg, "metrik": metrik,
                        "n_ulasan": int(topeng.sum()), "n_butir": n_butir,
                        "dukungan": int(tp + fn),
                        "tp": np.nan if sembunyi else int(tp),
                        "fp": np.nan if sembunyi else int(fp),
                        "fn": np.nan if sembunyi else int(fn),
                        "presisi_persen": np.nan if sembunyi or tp + fp == 0 else 100 * tp / (tp + fp),
                        "recall_persen": np.nan if sembunyi or tp + fn == 0 else 100 * tp / (tp + fn),
                        "f1_persen": np.nan if sembunyi else f1,
                        "ik95_bawah": np.nan if sembunyi else bw,
                        "ik95_atas": np.nan if sembunyi else at,
                        "status": st,
                    })

    # ---------------- McNemar -----------------------------------------------------
    def tabel_mcnemar(benar_1, benar_2, sah):
        return (int((sah & benar_1 & benar_2).sum()), int((sah & benar_1 & ~benar_2).sum()),
                int((sah & ~benar_1 & benar_2).sum()), int((sah & ~benar_1 & ~benar_2).sum()))

    p_h1 = {}
    for s, (cak, jenis, idx) in enumerate(CAKUPAN):
        if jenis != "GABUNGAN":
            continue
        for metrik in METRIK_UTAMA:
            benar = np.zeros(pred.shape, dtype=bool)
            for m in range(len(MODEL)):
                for r in range(len(REGISTER)):
                    benar[m, r], sah = benar_per_butir(emas, pred[m, r], pol[m, r], metrik, mode_pol)
            sah = sah[:, idx]
            if berpasangan:      # dua register dalam satu model (H1, satu arah)
                for m, model in enumerate(MODEL):
                    kk, b, c, ss = tabel_mcnemar(benar[m, 0][:, idx], benar[m, 1][:, idx], sah)
                    p = mcnemar_eksak(b, c, "lebih")
                    p_h1[(cak, model, metrik)] = (p, b, c)
                    mcnemar.append({
                        "himpunan": nama, "cakupan": cak, "perbandingan": "REGISTER_DALAM_MODEL",
                        "model": model, "register": "FORMAL vs INFORMAL", "metrik": metrik,
                        "n_butir": kk + b + c + ss, "benar_keduanya": kk, "b": b, "c": c,
                        "salah_keduanya": ss, "arti_b": "benar FORMAL, salah INFORMAL",
                        "arti_c": "salah FORMAL, benar INFORMAL", "arah": "satu arah (b > c)",
                        "p_mentah": p, "keluarga": f"H1 penjaga [{cak}]",
                        "status": status_dasar(jenis, metrik, cak)})
            # dua model dalam satu register (dua arah)
            daftar = [(r, reg, hadir[r]) for r, reg in enumerate(REGISTER)] if ada_reg else []
            if not berpasangan:
                daftar.append((None, "SEMUA", np.ones(len(emas), dtype=bool)))
            for r, reg, topeng in daftar:
                if r is None:    # tiap ulasan hanya hadir pada satu register
                    b1 = np.where(hadir[0][:, None], benar[0, 0], benar[0, 1])
                    b2 = np.where(hadir[0][:, None], benar[1, 0], benar[1, 1])
                else:
                    b1, b2 = benar[0, r], benar[1, r]
                kk, b, c, ss = tabel_mcnemar(b1[:, idx], b2[:, idx], sah & topeng[:, None])
                mcnemar.append({
                    "himpunan": nama, "cakupan": cak, "perbandingan": "MODEL_DALAM_REGISTER",
                    "model": f"{MODEL[0]} vs {MODEL[1]}", "register": reg, "metrik": metrik,
                    "n_butir": kk + b + c + ss, "benar_keduanya": kk, "b": b, "c": c,
                    "salah_keduanya": ss, "arti_b": f"benar {MODEL[0]}, salah {MODEL[1]}",
                    "arti_c": f"salah {MODEL[0]}, benar {MODEL[1]}", "arah": "dua arah",
                    "p_mentah": mcnemar_eksak(b, c, "dua"),
                    "keluarga": f"Antarmodel per register [{cak}]" if berpasangan else "",
                    "status": status_dasar(jenis, metrik, cak)})

    if not ada_reg:      # tanpa register tidak ada selisih antarregister yang dapat dihitung
        return kinerja, selisih, mcnemar

    # ---------------- selisih -------------------------------------------------------
    def baris_selisih(cak, jenis, besaran, model, metrik, est, seb, st, uji="", arah="",
                      p=np.nan, keluarga="", p_boot=np.nan, catatan=""):
        bw, at = selang(seb)
        sembunyi = st == "TIDAK_DILAPORKAN"
        return {"himpunan": nama, "cakupan": cak, "jenis_cakupan": jenis, "besaran": besaran,
                "model": model, "metrik": metrik,
                "estimasi_pp": np.nan if sembunyi else est,
                "ik95_bawah_pp": np.nan if sembunyi else bw,
                "ik95_atas_pp": np.nan if sembunyi else at,
                "uji_keputusan": uji, "arah": arah, "p_mentah": p, "keluarga": keluarga,
                "p_bootstrap": p_boot, "n_ulang_sah": int((~np.isnan(seb)).sum()),
                "status": st, "catatan": catatan}

    for s, (cak, jenis, idx) in enumerate(CAKUPAN):
        gab = jenis == "GABUNGAN"
        for k, metrik in enumerate(METRIK):
            if not dipakai(jenis, metrik, cak):
                continue
            st = status_dasar(jenis, metrik, cak)
            diuji = gab and metrik in METRIK_UTAMA
            # Delta-F1 per model
            for m, model in enumerate(MODEL):
                seb = ulang["delta"][:, m, s, k]
                kw = {}
                if diuji and berpasangan:
                    p, b, c = p_h1[(cak, model, metrik)]
                    kw = dict(uji="McNemar eksak", arah="satu arah (> 0)", p=p,
                              keluarga=f"H1 penjaga [{cak}]", p_boot=p_bootstrap(seb, "lebih"),
                              catatan=f"b={b}, c={c}; p_bootstrap = pemeriksaan kepekaan")
                elif diuji:
                    pb = p_bootstrap(seb, "lebih")
                    kw = dict(uji=nama_uji_boot, arah="satu arah (> 0)", p=pb, p_boot=pb,
                              catatan="register berisi ulasan berbeda; bukan uji berpasangan")
                selisih.append(baris_selisih(cak, jenis, "DELTA_F1", model, metrik,
                                             titik["delta"][m, s, k], seb, st, **kw))
            # Delta-kuadrat
            seb = ulang["delta2"][:, s, k]
            kw = {}
            if diuji:
                pb = p_bootstrap(seb, "dua")
                kw = dict(uji=nama_uji_boot, arah="dua arah", p=pb, p_boot=pb,
                          keluarga=f"H2 [{cak}]" if berpasangan else "")
            selisih.append(baris_selisih(cak, jenis, "DELTA_KUADRAT",
                                         f"{MODEL[0]} - {MODEL[1]}", metrik,
                                         titik["delta2"][s, k], seb, st, **kw))
        # selisih subtugas (Delta-F1-ACSA - Delta-F1-ACD) per model
        st = status_dasar(jenis, "ACSA", cak)
        for m, model in enumerate(MODEL):
            seb = ulang["subtugas"][:, m, s]
            kw = {}
            if gab:
                pb = p_bootstrap(seb, "lebih")
                kw = dict(uji=nama_uji_boot, arah="satu arah (> 0)", p=pb, p_boot=pb,
                          keluarga=f"H3 [{cak}]" if berpasangan else "")
            selisih.append(baris_selisih(cak, jenis, "SELISIH_SUBTUGAS", model, "ACSA - ACD",
                                         titik["subtugas"][m, s], seb, st, **kw))
    return kinerja, selisih, mcnemar


def terapkan_holm(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["p_holm"] = np.nan
    df["tolak_h0"] = ""
    for keluarga, sub in df[df["keluarga"] != ""].groupby("keluarga"):
        adj = holm(sub["p_mentah"].to_numpy())
        df.loc[sub.index, "p_holm"] = adj
        df.loc[sub.index, "tolak_h0"] = np.where(adj < ALFA, "YA", "TIDAK")
        df.loc[sub.index, "ukuran_keluarga"] = len(sub)
    return df


# =============================================================================
# RINGKASAN
# =============================================================================
def a(x, d=2):
    """Angka berkoma desimal Indonesia."""
    return "-" if x is None or (isinstance(x, float) and np.isnan(x)) else f"{x:.{d}f}".replace(".", ",")


def ap(p):
    if p is None or np.isnan(p):
        return "-"
    return "< 0,001" if p < 0.001 else f"{p:.3f}".replace(".", ",")


NAMA_METRIK = {"ACD": "F1-ACD", "ACSA": "F1-ACSA (NEGATIF)", "PASANGAN": "F1-pasangan",
               "ACSA_POS": "F1-ACSA (POSITIF)"}


def tulis_ringkasan(kin, sel, mcn, kek, info, jalur: Path):
    judul = "# Ringkasan evaluasi" + (" (ANALISIS KEPEKAAN: tanpa teks terpotong)" if MODE_KEPEKAAN else "")
    L = [judul, "",
         f"Benih pelatihan {info['benih']} | {info['n_ulang']} penarikan bootstrap "
         f"(benih {BENIH_BOOTSTRAP}) | polaritas mode {info['mode_pol']} | alfa {a(ALFA)} "
         f"| koreksi Holm per keluarga", ""]
    if MODE_KEPEKAAN:
        L += [f"Dibuang karena terpotong pada salah satu versi atau salah satu model: "
              f"{info['dibuang']['uji_berpasangan']} dari {info['n_awal']['uji_berpasangan']} pasangan, "
              f"{info['dibuang']['uji_takberpasangan']} dari {info['n_awal']['uji_takberpasangan']} "
              f"ulasan tak berpasangan. Seluruh hasil di bawah berstatus KEPEKAAN dan tidak dipakai "
              f"untuk menerima atau menolak hipotesis; bandingkan arah dan besarnya dengan ringkasan utama.", ""]

    L += ["## Dukungan kelas pada himpunan uji berpasangan (per pasangan)", "",
          "| Kelompok | Emas ADA | NEGATIF | POSITIF | Kelas POSITIF dilaporkan? |",
          "|---|---|---|---|---|"]
    for g, d in info["dukungan"].items():
        L.append(f"| {g} | {d['ada']} | {d['neg']} | {d['pos']} | "
                 f"{'ya, eksploratori' if d['lapor'] else f'tidak (< {AMBANG_DUKUNGAN_POSITIF})'} |")
    L += ["", "## Pemotongan token pada himpunan uji berpasangan", "",
          "| Model | FORMAL terpotong | INFORMAL terpotong | Pasangan yang hanya satu versinya terpotong |",
          "|---|---|---|---|"]
    for m, d in info["terpotong"].items():
        L.append(f"| {m} | {a(d['FORMAL'])}% | {a(d['INFORMAL'])}% | {d['timpang']} |")
    L.append("")

    P = kin[kin.himpunan == "uji_berpasangan"]
    SP = sel[sel.himpunan == "uji_berpasangan"]
    MP = mcn[mcn.himpunan == "uji_berpasangan"]
    for cak, jenis, _ in CAKUPAN:
        if jenis != "GABUNGAN":
            continue
        if MODE_KEPEKAAN:
            peran = "KEPEKAAN: tidak dipakai untuk menerima atau menolak H1-H3"
        else:
            peran = ("KONFIRMATORI: dasar keputusan H1-H3" if cak == CAKUPAN_KONFIRMATORI else
                     "ANALISIS LANJUTAN: tidak dipakai untuk menerima atau menolak H1-H3")
        L += [f"## Himpunan uji berpasangan - cakupan {cak} ({peran})", "",
              "### Kinerja dan penurunan (H1, uji penjaga)", "",
              "| Model | Metrik | F1 FORMAL | F1 INFORMAL | Delta-F1 (pp) | Selang 95% | "
              "McNemar b/c | p | p Holm | H0 ditolak |", "|---|---|---|---|---|---|---|---|---|---|"]
        for model in MODEL:
            for metrik in METRIK_UTAMA:
                f = P[(P.cakupan == cak) & (P.model == model) & (P.metrik == metrik)].set_index("register")
                d = SP[(SP.cakupan == cak) & (SP.besaran == "DELTA_F1") & (SP.model == model)
                       & (SP.metrik == metrik)].iloc[0]
                t = MP[(MP.cakupan == cak) & (MP.perbandingan == "REGISTER_DALAM_MODEL")
                       & (MP.model == model) & (MP.metrik == metrik)].iloc[0]
                L.append(f"| {model} | {NAMA_METRIK[metrik]} | {a(f.loc['FORMAL', 'f1_persen'])} | "
                         f"{a(f.loc['INFORMAL', 'f1_persen'])} | {a(d.estimasi_pp)} | "
                         f"{a(d.ik95_bawah_pp)} s.d. {a(d.ik95_atas_pp)} | {t.b}/{t.c} | "
                         f"{ap(d.p_mentah)} | {ap(d.p_holm)} | {d.tolak_h0} |")
        lolos = SP[(SP.cakupan == cak) & (SP.keluarga == f"H1 penjaga [{cak}]")]
        L += ["", f"Uji penjaga: {int((lolos.tolak_h0 == 'YA').sum())} dari {len(lolos)} "
                  f"hipotesis nol ditolak."
              + ("" if (lolos.tolak_h0 == "YA").all() else
                 " Bagi sel yang tidak ditolak, H2 dan H3 tetap dilaporkan tetapi ditafsirkan "
                 "hati-hati."), "",
              "### Delta-kuadrat (H2)", "",
              "| Metrik | Delta-kuadrat (pp) | Selang 95% | p | p Holm | H0 ditolak |",
              "|---|---|---|---|---|---|"]
        for metrik in METRIK_UTAMA:
            d = SP[(SP.cakupan == cak) & (SP.besaran == "DELTA_KUADRAT") & (SP.metrik == metrik)].iloc[0]
            L.append(f"| {NAMA_METRIK[metrik]} | {a(d.estimasi_pp)} | {a(d.ik95_bawah_pp)} s.d. "
                     f"{a(d.ik95_atas_pp)} | {ap(d.p_mentah)} | {ap(d.p_holm)} | {d.tolak_h0} |")
        L += ["", "### Selisih subtugas, Delta-F1-ACSA dikurangi Delta-F1-ACD (H3)", "",
              "| Model | Selisih (pp) | Selang 95% | p | p Holm | H0 ditolak |",
              "|---|---|---|---|---|---|"]
        for model in MODEL:
            d = SP[(SP.cakupan == cak) & (SP.besaran == "SELISIH_SUBTUGAS") & (SP.model == model)].iloc[0]
            L.append(f"| {model} | {a(d.estimasi_pp)} | {a(d.ik95_bawah_pp)} s.d. "
                     f"{a(d.ik95_atas_pp)} | {ap(d.p_mentah)} | {ap(d.p_holm)} | {d.tolak_h0} |")
        L += ["", "### Dua model dalam satu register (McNemar dua arah)", "",
              f"| Register | Metrik | b ({MODEL[0]} saja benar) | c ({MODEL[1]} saja benar) | "
              "p | p Holm | H0 ditolak |", "|---|---|---|---|---|---|---|"]
        for reg in REGISTER:
            for metrik in METRIK_UTAMA:
                t = MP[(MP.cakupan == cak) & (MP.perbandingan == "MODEL_DALAM_REGISTER")
                       & (MP.register == reg) & (MP.metrik == metrik)].iloc[0]
                L.append(f"| {reg} | {NAMA_METRIK[metrik]} | {t.b} | {t.c} | {ap(t.p_mentah)} | "
                         f"{ap(t.p_holm)} | {t.tolak_h0} |")
        if cak in KELOMPOK and info["dukungan"][cak]["lapor"]:
            L += ["", "### Kelas POSITIF (EKSPLORATORI, tanpa pengujian)", "",
                  "| Model | F1 FORMAL (selang 95%) | F1 INFORMAL (selang 95%) | Delta-F1 (selang 95%) |",
                  "|---|---|---|---|"]
            for model in MODEL:
                f = P[(P.cakupan == cak) & (P.model == model) & (P.metrik == "ACSA_POS")].set_index("register")
                d = SP[(SP.cakupan == cak) & (SP.besaran == "DELTA_F1") & (SP.model == model)
                       & (SP.metrik == "ACSA_POS")].iloc[0]
                sel_f1 = lambda r: (f"{a(f.loc[r, 'f1_persen'])} ({a(f.loc[r, 'ik95_bawah'])} s.d. "
                                    f"{a(f.loc[r, 'ik95_atas'])})")
                L.append(f"| {model} | {sel_f1('FORMAL')} | {sel_f1('INFORMAL')} | {a(d.estimasi_pp)} "
                         f"({a(d.ik95_bawah_pp)} s.d. {a(d.ik95_atas_pp)}) |")
        L.append("")

    L += ["## Per kategori aspek (EKSPLORATORI: selang kepercayaan, tanpa angka p)", "",
          "| Aspek | Model | Delta-F1-ACD | Delta-F1-ACSA | Delta-F1-pasangan |", "|---|---|---|---|---|"]
    for cak, jenis, _ in CAKUPAN:
        if jenis != "ASPEK":
            continue
        for model in MODEL:
            sel_d = []
            for metrik in METRIK_UTAMA:
                d = SP[(SP.cakupan == cak) & (SP.besaran == "DELTA_F1") & (SP.model == model)
                       & (SP.metrik == metrik)].iloc[0]
                sel_d.append(f"{a(d.estimasi_pp)} ({a(d.ik95_bawah_pp)} s.d. {a(d.ik95_atas_pp)})")
            L.append(f"| {cak} | {model} | " + " | ".join(sel_d) + " |")
    L.append("")

    # ---- recall NEGATIF dan sebaran kekeliruan (Subbab 3.5.4) --------------------
    K = kek[kek.himpunan == "uji_berpasangan"]
    if len(K):
        L += ["## Recall kelas NEGATIF dan sebaran kekeliruan (himpunan uji berpasangan)", "",
              "Recall NEGATIF = proporsi butir emas NEGATIF yang diprediksi NEGATIF oleh keputusan "
              "tiga kelas, yaitu keluhan yang tertangkap sistem dengan polaritas tepat. Selang 95% "
              "Wilson. Luput = aspek hadir tetapi diprediksi TIDAK_ADA; muncul palsu = aspek tidak "
              "hadir tetapi diprediksi hadir; terbalik = aspek tertangkap dengan polaritas keliru.", "",
              "| Cakupan | Model | Register | Emas NEGATIF | Recall NEGATIF (selang 95%) | "
              "Recall deteksi | Luput | Muncul palsu | Terbalik |",
              "|---|---|---|---|---|---|---|---|---|"]
        urutan = KELOMPOK["KEAMANAN"] + ["KEAMANAN", "KONTROL", "SEMUA"]
        for cak in urutan:
            for model in MODEL:
                for reg in REGISTER:
                    r = K[(K.cakupan == cak) & (K.model == model) & (K.register == reg)]
                    if not len(r):
                        continue
                    r = r.iloc[0]
                    L.append(f"| {cak} | {model} | {reg} | {r.emas_negatif} | "
                             f"{a(r.recall_negatif_persen, 1)} ({a(r.recall_negatif_ik95_bawah, 1)} s.d. "
                             f"{a(r.recall_negatif_ik95_atas, 1)}) | {a(r.recall_deteksi_persen, 1)} | "
                             f"{r.luput} | {r.muncul_palsu} | {r.polaritas_terbalik} |")
        L.append("")

    T = kin[kin.himpunan == "uji_takberpasangan"]
    ST = sel[sel.himpunan == "uji_takberpasangan"]
    if len(T):
        L += ["## Himpunan uji tak berpasangan (pemeriksaan KETAHANAN, tidak mengikat)", "",
              ("Kedua register berisi ulasan yang berbeda, sehingga selisih di bawah ini memuat "
               "pengaruh isi di samping pengaruh register. Yang diperiksa hanyalah apakah ARAH "
               "dan urutan besarnya sejalan dengan himpunan berpasangan. Angka p tidak dikoreksi."
               if len(ST) else
               "Berkas ini tidak berkolom register, sehingga hanya kinerja keseluruhan dan "
               "perbandingan antarmodel yang dihitung. Tambahkan kolom `register` pada "
               "uji_takberpasangan.csv untuk memperoleh selisih antarregister."), ""]
        for cak, jenis, _ in CAKUPAN:
            if jenis != "GABUNGAN":
                continue
            L += [f"### Cakupan {cak}", "",
                  "| Model | Metrik | F1 seluruhnya | F1 FORMAL | F1 INFORMAL | Delta-F1 (pp) | Selang 95% |",
                  "|---|---|---|---|---|---|---|"]
            for model in MODEL:
                for metrik in METRIK_UTAMA:
                    f = T[(T.cakupan == cak) & (T.model == model) & (T.metrik == metrik)].set_index("register")
                    d = (ST[(ST.cakupan == cak) & (ST.besaran == "DELTA_F1") & (ST.model == model)
                            & (ST.metrik == metrik)] if len(ST) else ST)
                    ambil = lambda r: a(f.loc[r, "f1_persen"]) if r in f.index else "-"
                    L.append(f"| {model} | {NAMA_METRIK[metrik]} | {ambil('SEMUA')} | {ambil('FORMAL')} | "
                             f"{ambil('INFORMAL')} | "
                             + (f"{a(d.iloc[0].estimasi_pp)} | {a(d.iloc[0].ik95_bawah_pp)} s.d. "
                                f"{a(d.iloc[0].ik95_atas_pp)} |" if len(d) else "- | - |"))
            mt = mcn[(mcn.himpunan == "uji_takberpasangan") & (mcn.cakupan == cak)]
            if len(mt):
                L += ["", f"| Register | Metrik | b ({MODEL[0]} saja benar) | c ({MODEL[1]} saja benar) | "
                          "p McNemar dua arah (tak dikoreksi) |", "|---|---|---|---|---|"]
                for _, t in mt.iterrows():
                    L.append(f"| {t.register} | {NAMA_METRIK[t.metrik]} | {t.b} | {t.c} | {ap(t.p_mentah)} |")
            d2 = (ST[(ST.cakupan == cak) & (ST.besaran == "DELTA_KUADRAT") & ST.metrik.isin(METRIK_UTAMA)]
                  if len(ST) else ST)
            if len(d2):
                L += ["", "| Metrik | Delta-kuadrat (pp) | Selang 95% | p (tak dikoreksi) |", "|---|---|---|---|"]
                for _, d in d2.iterrows():
                    L.append(f"| {NAMA_METRIK[d.metrik]} | {a(d.estimasi_pp)} | {a(d.ik95_bawah_pp)} "
                             f"s.d. {a(d.ik95_atas_pp)} | {ap(d.p_mentah)} |")
            L.append("")
    jalur.write_text("\n".join(L), encoding="utf-8")


# =============================================================================
# UTAMA
# =============================================================================
def main():
    global MODE_KEPEKAAN
    ap_ = argparse.ArgumentParser(description="Evaluasi tiga metrik, McNemar, dan bootstrap berkluster.")
    ap_.add_argument("--prediksi-dir", required=True, type=Path)
    ap_.add_argument("--hasil-dir", required=True, type=Path)
    ap_.add_argument("--benih", type=int, default=42, help="benih pelatihan yang dievaluasi")
    ap_.add_argument("--n-bootstrap", type=int, default=N_BOOTSTRAP)
    ap_.add_argument("--polaritas", choices=["terbatas", "penuh"], default="terbatas")
    ap_.add_argument("--tanpa-terpotong", action="store_true",
                     help="analisis kepekaan: buang ulasan yang terpotong pada salah satu versi/model")
    args = ap_.parse_args()
    if args.n_bootstrap < 2000:
        sys.exit("GALAT: naskah menetapkan minimal 2.000 penarikan bootstrap.")
    MODE_KEPEKAAN = args.tanpa_terpotong
    if MODE_KEPEKAAN and (args.hasil_dir / "ringkasan.md").exists():
        lama = (args.hasil_dir / "ringkasan.md").read_text(encoding="utf-8").splitlines()[0]
        if "KEPEKAAN" not in lama:
            sys.exit(f"GALAT: {args.hasil_dir} berisi hasil UTAMA. Pakai --hasil-dir lain untuk "
                     f"analisis kepekaan, mis. keluaran/hasil_tanpa_terpotong.")

    try:
        SP = susun(muat_prediksi(args.prediksi_dir, "uji_berpasangan", args.benih), True)
        ST = susun(muat_prediksi(args.prediksi_dir, "uji_takberpasangan", args.benih), False)
    except GalatData as g:
        sys.exit(f"GALAT: {g}")

    # aturan pelaporan kelas POSITIF ditetapkan dari himpunan berpasangan UTUH (per pasangan)
    dukungan, lapor_pos = {}, {}
    for g, anggota in KELOMPOK.items():
        sub = SP["emas"][:, [ASPEK.index(x) for x in anggota]]
        pos = int((sub == 2).sum())
        lapor_pos[g] = pos >= AMBANG_DUKUNGAN_POSITIF
        dukungan[g] = {"ada": int((sub != 0).sum()), "neg": int((sub == 1).sum()),
                       "pos": pos, "lapor": lapor_pos[g]}
    terpotong = {m: {"FORMAL": 100 * SP["terpotong"][i, 0].mean(),
                     "INFORMAL": 100 * SP["terpotong"][i, 1].mean(),
                     "timpang": int((SP["terpotong"][i, 0] != SP["terpotong"][i, 1]).sum())}
                 for i, m in enumerate(MODEL)}

    n_awal = {"uji_berpasangan": len(SP["ids"]), "uji_takberpasangan": len(ST["ids"])}
    dibuang = {"uji_berpasangan": 0, "uji_takberpasangan": 0}
    if MODE_KEPEKAAN:
        SP, dibuang["uji_berpasangan"] = saring_terpotong(SP)
        ST, dibuang["uji_takberpasangan"] = saring_terpotong(ST)
        print(f"ANALISIS KEPEKAAN: dibuang {dibuang['uji_berpasangan']} dari "
              f"{n_awal['uji_berpasangan']} pasangan dan {dibuang['uji_takberpasangan']} dari "
              f"{n_awal['uji_takberpasangan']} ulasan tak berpasangan.", flush=True)

    rng = np.random.default_rng(BENIH_BOOTSTRAP)
    print(f"Himpunan berpasangan: {len(SP['ids'])} pasangan | tak berpasangan: "
          f"{len(ST['ids'])} ulasan | {args.n_bootstrap} penarikan bootstrap ...", flush=True)
    k1, s1, m1 = analisis("uji_berpasangan", SP, True, lapor_pos, args.n_bootstrap, rng, args.polaritas)
    k2, s2, m2 = analisis("uji_takberpasangan", ST, False, lapor_pos, args.n_bootstrap, rng, args.polaritas)
    if not ST["ada_register"]:
        print("PERINGATAN: berkas tak berpasangan tidak berkolom register; hanya kinerja "
              "keseluruhan yang dihitung.", flush=True)

    kin = pd.DataFrame(k1 + k2)
    sel = terapkan_holm(pd.DataFrame(s1 + s2))
    mcn = terapkan_holm(pd.DataFrame(m1 + m2))
    kek = pd.DataFrame(kekeliruan("uji_berpasangan", SP) + kekeliruan("uji_takberpasangan", ST))

    args.hasil_dir.mkdir(parents=True, exist_ok=True)
    kin.to_csv(args.hasil_dir / "kinerja.csv", index=False, float_format="%.4f")
    sel.to_csv(args.hasil_dir / "selisih.csv", index=False, float_format="%.6g")
    mcn.to_csv(args.hasil_dir / "mcnemar.csv", index=False, float_format="%.6g")
    kek.to_csv(args.hasil_dir / "kekeliruan.csv", index=False, float_format="%.4f")
    tulis_ringkasan(kin, sel, mcn, kek, {"benih": args.benih, "n_ulang": args.n_bootstrap,
                                         "mode_pol": args.polaritas, "dukungan": dukungan,
                                         "terpotong": terpotong, "n_awal": n_awal, "dibuang": dibuang},
                    args.hasil_dir / "ringkasan.md")
    print(f"Selesai. Lihat {args.hasil_dir / 'ringkasan.md'}", flush=True)


if __name__ == "__main__":
    main()
