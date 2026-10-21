#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
cari_hiperparameter.py
======================
Pencarian hiperparameter menyeluruh menurut Subbab 3.5.3 Bab III:

    laju belajar {2, 3, 5} x 10^-5  x  ukuran tumpukan {16, 32}  x  epoch {2, 3, 4}
    = 18 kombinasi, masing-masing dilatih untuk IndoBERT dan IndoBERTweet (36 lari).

Aturan pemilihan (ditetapkan sebelum pencarian dijalankan)
----------------------------------------------------------
  1. Ukuran: F1-pasangan pada himpunan pengembangan, dari bobot akhir epoch terakhir,
     benih 42 -- sama dengan yang dipakai `latih_prediksi.py` untuk prediksi.
  2. Satu pencarian untuk kedua model: skor sebuah kombinasi = rerata F1-pasangan
     IndoBERT dan IndoBERTweet. Kombinasi terpilih = skor tertinggi.
  3. Seri (selisih skor < 0,01 poin persentase dari yang tertinggi) diputus berurutan
     menurut epoch paling sedikit, laju belajar paling kecil, ukuran tumpukan paling kecil.

Jaminan
-------
  * Lingkar pelatihan TIDAK ditulis ulang di sini: tiap lari memanggil
    `latih_prediksi.bangun_dan_latih`, fungsi yang sama dengan lari utama.
  * Hanya latih.csv dan pengembangan.csv yang dibuka. Himpunan uji tidak dimuat,
    tidak ditokenisasi, dan tidak diprediksi.
  * Kombinasi Tabel 12 dijalankan paling dahulu dan, bila --acuan-dir diberikan,
    dibandingkan dengan riwayat pada catatan_lari_<model>_benih42.json. Bila F1
    pengembangan per epoch tidak sama, pencarian berhenti sebelum 34 lari sisanya
    (lihat --lanjut-walau-beda).
  * Dapat dilanjutkan: lari yang sudah selesai dilewati, sehingga sambungan Colab
    yang terputus cukup diatasi dengan menjalankan ulang perintah yang sama.

Pemakaian
---------
  python cari_hiperparameter.py --data-dir data --keluaran-dir keluaran_pencarian \
         --acuan-dir keluaran

  --ringkas-saja     menyusun ulang tabel dan ringkasan dari lari yang sudah ada, tanpa melatih

Keluaran (di dalam --keluaran-dir)
----------------------------------
  pencarian_hiperparameter.csv   satu baris per kombinasi (18 baris), terurut menurut peringkat
  pencarian_riwayat.csv          kinerja pengembangan per epoch untuk ke-36 lari
  ringkasan_pencarian.md         kombinasi terpilih, perbandingan dengan Tabel 12, langkah lanjut
  catatan_pencarian.json         kisi, aturan, hash berkas, hasil pemeriksaan reproduksi
  lari/<model>/<kombinasi>/      prediksi pengembangan per butir dan selesai.json tiap lari
"""
import argparse
import gc
import itertools
import json
import sys
import time
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import pandas as pd

import latih_prediksi as lp
from latih_prediksi import ASPEK, BENIH, LABEL, MODEL, TABEL_12, GalatData, cetak

# =============================================================================
# KISI DAN ATURAN (Subbab 3.5.3) -- jangan diubah tanpa mengubah naskah
# =============================================================================
KISI_LAJU_BELAJAR = [2e-5, 3e-5, 5e-5]
KISI_UKURAN_TUMPUKAN = [16, 32]
KISI_EPOCH = [2, 3, 4]
AMBANG_SERI = 0.01            # poin persentase
N_BOOTSTRAP = 10000           # hanya untuk selang pembanding terpilih vs Tabel 12
TOLERANSI_RUGI = 1e-3         # pemeriksaan reproduksi: batas derau numerik pada nilai rugi
HIMPUNAN = ("latih", "pengembangan")
NAMA_TAMPIL = {"indobert": "IndoBERT", "indobertweet": "IndoBERTweet"}


def daftar_kombinasi() -> list:
    """Ke-18 kombinasi; Tabel 12 paling dahulu agar pemeriksaan reproduksi terjadi di awal."""
    semua = list(itertools.product(KISI_LAJU_BELAJAR, KISI_UKURAN_TUMPUKAN, KISI_EPOCH))
    return [k for k in semua if k == TABEL_12] + [k for k in semua if k != TABEL_12]


def nama_kombinasi(lr: float, bs: int, ep: int) -> str:
    return f"lr{lr:g}_bs{bs}_ep{ep}"


# =============================================================================
# METRIK PENGEMBANGAN (rumus sama dengan ringkas_pengembangan pada latih_prediksi.py)
# =============================================================================
def cacah_per_ulasan(emas: np.ndarray, pred: np.ndarray) -> dict:
    """emas, pred: [N, 5] indeks kelas. Mengembalikan cacah per ulasan untuk dua metrik."""
    ada_e, ada_p = emas != 0, pred != 0
    return {
        "pasangan": np.stack([(ada_e & (pred == emas)).sum(1), (ada_p & (pred != emas)).sum(1),
                              (ada_e & (pred != emas)).sum(1)], axis=1),
        "acd": np.stack([(ada_e & ada_p).sum(1), (~ada_e & ada_p).sum(1),
                         (ada_e & ~ada_p).sum(1)], axis=1),
    }


def f1_mikro(cacah) -> float:
    """cacah: [..., 3] = (TP, FP, FN). F1 mikro dalam persen."""
    tp, fp, fn = np.asarray(cacah, dtype=float).reshape(-1, 3).sum(0)
    return float(100 * 2 * tp / (2 * tp + fp + fn)) if (2 * tp + fp + fn) else float("nan")


def baca_prediksi(jalur: Path, id_urut: list) -> tuple:
    """Membaca prediksi pengembangan satu lari menjadi (emas, pred) berukuran [N, 5]."""
    df = pd.read_csv(jalur, dtype=str, keep_default_na=False, encoding="utf-8")
    n = len(id_urut)
    if len(df) != n * len(ASPEK):
        raise GalatData(f"{jalur}: {len(df)} baris, diharapkan {n * len(ASPEK)}.")
    if df["aspek"].tolist() != ASPEK * n or df["id_ulasan"].tolist()[::len(ASPEK)] != list(id_urut):
        raise GalatData(f"{jalur}: urutan ulasan atau aspek tidak sesuai himpunan pengembangan.")
    indeks = {l: i for i, l in enumerate(LABEL)}
    ubah = lambda kol: df[kol].map(indeks).to_numpy().reshape(n, len(ASPEK))
    return ubah("emas"), ubah("prediksi")


# =============================================================================
# PEMILIHAN
# =============================================================================
def pilih(tabel: pd.DataFrame) -> int:
    """Indeks baris terpilih menurut aturan 2 dan 3 pada docstring modul."""
    skor = tabel["f1_pasangan_rerata"].to_numpy(dtype=float)
    calon = tabel[skor.max() - skor < AMBANG_SERI]
    return int(calon.sort_values(["epoch", "laju_belajar", "ukuran_tumpukan"]).index[0])


def urutkan(tabel: pd.DataFrame) -> pd.DataFrame:
    """Menambah kolom terpilih, tabel_12, peringkat; terpilih selalu peringkat 1."""
    t = tabel.copy()
    menang = pilih(t)
    t["terpilih"] = t.index == menang
    t["tabel_12"] = [(r.laju_belajar, r.ukuran_tumpukan, r.epoch) == TABEL_12
                     for r in t.itertuples()]
    t["_skor"] = -t["f1_pasangan_rerata"]
    t["_bukan"] = ~t["terpilih"]
    t = t.sort_values(["_bukan", "_skor", "epoch", "laju_belajar", "ukuran_tumpukan"])
    t = t.drop(columns=["_skor", "_bukan"]).reset_index(drop=True)
    t.insert(0, "peringkat", np.arange(1, len(t) + 1))
    return t


def bootstrap_selisih(cacah_a: dict, cacah_b: dict, n_ulang: int, benih: int) -> dict:
    """Selisih skor (rerata F1-pasangan kedua model) kombinasi A - kombinasi B.

    cacah_x: {model: [N, 3]} pada ulasan pengembangan yang sama. Ulasan ditarik ulang
    utuh, dan penarikan yang sama dikenakan pada kedua kombinasi serta kedua model.
    """
    n = len(next(iter(cacah_a.values())))
    rng = np.random.default_rng(benih)
    bobot = rng.multinomial(n, np.full(n, 1.0 / n), size=n_ulang).astype(float)   # [B, N]

    def skor(cacah, w):
        nilai = []
        for c in cacah.values():
            s = w @ c.astype(float)                                              # [B, 3]
            penyebut = 2 * s[:, 0] + s[:, 1] + s[:, 2]
            nilai.append(np.where(penyebut > 0, 200 * s[:, 0] / np.maximum(penyebut, 1), np.nan))
        return np.mean(nilai, axis=0)

    satu = np.ones((1, n))
    titik = float((skor(cacah_a, satu) - skor(cacah_b, satu))[0])
    ulang = skor(cacah_a, bobot) - skor(cacah_b, bobot)
    ulang = ulang[~np.isnan(ulang)]
    return {"selisih": titik, "bawah": float(np.percentile(ulang, 2.5)),
            "atas": float(np.percentile(ulang, 97.5)), "galat_baku": float(ulang.std(ddof=1)),
            "n_ulang": int(len(ulang))}


# =============================================================================
# LARI
# =============================================================================
def dir_lari(dasar: Path, kunci: str, kombinasi: tuple) -> Path:
    return dasar / "lari" / kunci / nama_kombinasi(*kombinasi)


def sidik_lari(kunci: str, kombinasi: tuple, data: dict) -> dict:
    return {"model": kunci, "hf": MODEL[kunci]["hf"], "panjang_maks": MODEL[kunci]["panjang_maks"],
            "benih": BENIH, "laju_belajar": kombinasi[0], "ukuran_tumpukan": kombinasi[1],
            "epoch": kombinasi[2], "sha256": {n: data[n]["sha256"] for n in HIMPUNAN}}


def muat_selesai(dasar: Path, kunci: str, kombinasi: tuple, data: dict):
    """Catatan lari yang sudah selesai, atau None. Menolak sisa lari dari data/model lain."""
    jalur = dir_lari(dasar, kunci, kombinasi) / "selesai.json"
    if not jalur.exists():
        return None
    catatan = json.loads(jalur.read_text(encoding="utf-8"))
    if catatan["sidik"] != sidik_lari(kunci, kombinasi, data):
        raise GalatData(
            f"{jalur} berasal dari data, model, atau konfigurasi yang berbeda dari lari ini. "
            f"Pakai --keluaran-dir baru; hasil lama tidak dicampur.")
    return catatan


def jalankan(dasar: Path, kunci: str, kombinasi: tuple, data: dict, args) -> dict:
    import torch
    tujuan = dir_lari(dasar, kunci, kombinasi)
    tujuan.mkdir(parents=True, exist_ok=True)
    lp.atur_hiperparameter(*kombinasi)
    ns = SimpleNamespace(benih=BENIH, periksa=False, simpan_model=False,
                         tumpukan_prediksi=args.tumpukan_prediksi)
    hasil = lp.bangun_dan_latih(kunci, data, ns, tujuan, himpunan_prediksi=("pengembangan",))
    catatan = {"sidik": sidik_lari(kunci, kombinasi, data), **hasil}
    (tujuan / "selesai.json").write_text(json.dumps(catatan, indent=2, ensure_ascii=False),
                                         encoding="utf-8")
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    return catatan


def periksa_acuan(acuan_dir: Path, catatan: dict, data: dict) -> dict:
    """Membandingkan lari Tabel 12 dengan catatan_lari benih 42 dari lari utama."""
    hasil = {}
    for kunci in MODEL:
        jalur = acuan_dir / f"catatan_lari_{kunci}_benih{BENIH}.json"
        if not jalur.exists():
            hasil[kunci] = {"status": "TIDAK_ADA", "berkas": str(jalur)}
            continue
        acuan = json.loads(jalur.read_text(encoding="utf-8"))
        hp = acuan["hiperparameter"]
        if (hp["laju_belajar"], hp["ukuran_tumpukan"], hp["epoch"]) != TABEL_12:
            hasil[kunci] = {"status": "BUKAN_TABEL_12", "berkas": str(jalur)}
            continue
        beda_data = [n for n in HIMPUNAN if acuan["berkas"][n]["sha256"] != data[n]["sha256"]]
        lama, baru = acuan["riwayat"], catatan[kunci]["riwayat"]
        kunci_angka = [k for k in lama[0] if k != "epoch"]
        kunci_f1 = [k for k in kunci_angka if k.startswith("f1_")]
        beda = lambda nama: max(abs(a[k] - b[k]) for a, b in zip(lama, baru) for k in nama)
        selisih_f1 = max(abs(a["f1_pasangan_pengembangan"] - b["f1_pasangan_pengembangan"])
                         for a, b in zip(lama, baru))
        if lama == baru:
            status = "COCOK"
        elif len(lama) == len(baru) and beda(kunci_f1) == 0 and beda(kunci_angka) < TOLERANSI_RUGI:
            status = "SETARA"        # F1 tiap epoch identik; rugi berbeda sebatas derau numerik
        else:
            status = "BEDA"
        hasil[kunci] = {
            "status": status,
            "selisih_maks": beda(kunci_angka) if len(lama) == len(baru) else None,
            "selisih_maks_f1_pasangan": selisih_f1,
            "f1_pasangan_acuan": [e["f1_pasangan_pengembangan"] for e in lama],
            "f1_pasangan_kini": [e["f1_pasangan_pengembangan"] for e in baru],
            "data_berbeda": beda_data,
            "versi_acuan": acuan.get("versi"), "versi_kini": catatan[kunci].get("versi"),
            "perangkat_acuan": acuan.get("perangkat"), "perangkat_kini": catatan[kunci].get("perangkat"),
        }
    return hasil


# =============================================================================
# RINGKASAN
# =============================================================================
def susun_tabel(dasar: Path, data: dict) -> tuple:
    """Mengumpulkan lari yang selesai. Mengembalikan (tabel, riwayat, cacah, belum)."""
    emas_data = data["pengembangan"]["y"]
    baris, riwayat, cacah, belum = [], [], {}, []
    for kombinasi in daftar_kombinasi():
        lr, bs, ep = kombinasi
        r = {"laju_belajar": lr, "ukuran_tumpukan": bs, "epoch": ep}
        lengkap = True
        for kunci in MODEL:
            catatan = muat_selesai(dasar, kunci, kombinasi, data)
            if catatan is None:
                belum.append((kunci, kombinasi))
                lengkap = False
                continue
            jalur = dir_lari(dasar, kunci, kombinasi) / "prediksi" / f"{kunci}_benih{BENIH}_pengembangan.csv"
            emas, pred = baca_prediksi(jalur, data["pengembangan"]["id"])
            if not np.array_equal(emas, emas_data):
                raise GalatData(f"{jalur}: label emas tidak sama dengan pengembangan.csv.")
            c = cacah_per_ulasan(emas, pred)
            akhir = catatan["riwayat"][-1]
            f1p, f1a = f1_mikro(c["pasangan"]), f1_mikro(c["acd"])
            if abs(round(f1p, 2) - akhir["f1_pasangan_pengembangan"]) > 0.011:
                raise GalatData(f"{jalur}: F1-pasangan dari prediksi ({f1p:.2f}) tidak sama dengan "
                                f"riwayat pelatihan ({akhir['f1_pasangan_pengembangan']:.2f}).")
            cacah[(kunci, kombinasi)] = c["pasangan"]
            r[f"f1_pasangan_{kunci}"] = f1p
            r[f"f1_acd_{kunci}"] = f1a
            r[f"rugi_pengembangan_{kunci}"] = akhir["rugi_pengembangan"]
            for e in catatan["riwayat"]:
                riwayat.append({"model": kunci, "laju_belajar": lr, "ukuran_tumpukan": bs,
                                "epoch_total": ep, **e})
        if lengkap:
            r["f1_pasangan_rerata"] = float(np.mean([r[f"f1_pasangan_{k}"] for k in MODEL]))
            baris.append(r)
    kolom = (["laju_belajar", "ukuran_tumpukan", "epoch", "f1_pasangan_rerata"]
             + [f"{m}_{k}" for m in ("f1_pasangan", "f1_acd", "rugi_pengembangan") for k in MODEL])
    return pd.DataFrame(baris, columns=kolom), pd.DataFrame(riwayat), cacah, belum


def angka(x: float, desimal: int = 2) -> str:
    return f"{x:.{desimal}f}".replace(".", ",")


def tulis_lr(lr: float) -> str:
    return f"{lr * 1e5:g} × 10⁻⁵"


def tulis_ringkasan(tabel: pd.DataFrame, selang, acuan: dict, data: dict, belum: list,
                    args) -> str:
    L = ["# Pencarian hiperparameter (Subbab 3.5.3)", "",
         f"Kisi: laju belajar {{{', '.join(f'{x * 1e5:g}' for x in KISI_LAJU_BELAJAR)}}} × 10⁻⁵, "
         f"ukuran tumpukan {{{', '.join(map(str, KISI_UKURAN_TUMPUKAN))}}}, "
         f"epoch {{{', '.join(map(str, KISI_EPOCH))}}}; benih {BENIH}; "
         f"dilatih pada himpunan latih ({len(data['latih']['teks'])} ulasan) dan dinilai pada "
         f"himpunan pengembangan ({len(data['pengembangan']['teks'])} ulasan).", "",
         "Aturan pemilihan: skor = rerata F1-pasangan pengembangan IndoBERT dan IndoBERTweet pada "
         "akhir epoch terakhir; skor tertinggi terpilih; seri (selisih < 0,01 poin persentase) "
         "diputus menurut epoch paling sedikit, lalu laju belajar paling kecil, lalu ukuran "
         "tumpukan paling kecil.", ""]
    if belum:
        L += [f"**BELUM LENGKAP**: {len(belum)} dari {len(daftar_kombinasi()) * len(MODEL)} lari "
              f"belum selesai. Kombinasi terpilih belum dapat ditetapkan; tabel di bawah hanya "
              f"memuat kombinasi yang kedua modelnya sudah selesai.", ""]
    L += ["| Peringkat | Laju belajar | Tumpukan | Epoch | F1-pasangan IndoBERT | "
          "F1-pasangan IndoBERTweet | Rerata | Keterangan |", "|---|---|---|---|---|---|---|---|"]
    for r in tabel.itertuples():
        ket = []
        if not belum and r.terpilih:
            ket.append("**terpilih**")
        if r.tabel_12:
            ket.append("Tabel 12")
        L.append(f"| {r.peringkat} | {tulis_lr(r.laju_belajar)} | {r.ukuran_tumpukan} | {r.epoch} | "
                 f"{angka(r.f1_pasangan_indobert)} | {angka(r.f1_pasangan_indobertweet)} | "
                 f"{angka(r.f1_pasangan_rerata)} | {', '.join(ket)} |")
    L.append("")

    if not belum:
        m = tabel[tabel.terpilih].iloc[0]
        t12 = tabel[tabel.tabel_12].iloc[0]
        rentang = tabel.f1_pasangan_rerata.max() - tabel.f1_pasangan_rerata.min()
        L += ["## Kombinasi terpilih", "",
              f"Laju belajar {tulis_lr(m.laju_belajar)}, ukuran tumpukan {m.ukuran_tumpukan}, "
              f"{m.epoch} epoch (rerata F1-pasangan pengembangan {angka(m.f1_pasangan_rerata)}). "
              f"Rentang skor antara kombinasi terbaik dan terburuk {angka(rentang)} poin persentase.", ""]
        if bool(m.tabel_12):
            L += ["Kombinasi terpilih **sama dengan Tabel 12**. Lari utama benih 42, lari benih "
                  "43–46, dan seluruh analisis yang sudah dikerjakan tetap berlaku; tidak ada yang "
                  "perlu dilatih ulang.", ""]
        else:
            L += [f"Kombinasi terpilih **berbeda dari Tabel 12** (peringkat {t12.peringkat} dari "
                  f"{len(tabel)}, rerata {angka(t12.f1_pasangan_rerata)}). Selisih skor terpilih "
                  f"dikurangi Tabel 12 = {angka(selang['selisih'])} poin persentase; selang "
                  f"kepercayaan 95% bootstrap atas ulasan pengembangan "
                  f"({selang['n_ulang']} ulangan) {angka(selang['bawah'])} sampai "
                  f"{angka(selang['atas'])}.",
                  "",
                  "Selang ini hanya keterangan tentang seberapa menentukan pilihan tersebut. Ia "
                  "tidak mengubah aturan: menurut Subbab 3.5.3 nilai akhir adalah hasil pencarian, "
                  "sehingga analisis konfirmatori dijalankan dengan kombinasi terpilih dan hasil "
                  "konfigurasi Tabel 12 dilaporkan sebagai analisis kepekaan.", "",
                  "Langkah lanjut (folder keluaran baru, agar hasil Tabel 12 tidak tertimpa):", "",
                  "```",
                  f"python latih_prediksi.py --data-dir {args.data_dir} --keluaran-dir keluaran_terpilih "
                  f"--laju-belajar {m.laju_belajar:g} --ukuran-tumpukan {m.ukuran_tumpukan} "
                  f"--epoch {m.epoch}",
                  "```", "",
                  "Perintah yang sama diulang dengan `--benih 43` sampai `--benih 46`, lalu "
                  "`evaluasi_statistik.py`, `rangkum_benih.py`, dan `analisis_fertilitas.py` "
                  "dijalankan ulang atas folder tersebut.", ""]

    L += ["## Pemeriksaan reproduksi lari utama", ""]
    if not acuan:
        L += ["Tidak dijalankan (`--acuan-dir` tidak diberikan).", ""]
    for kunci, a in acuan.items():
        if a["status"] == "TIDAK_ADA":
            L.append(f"- {NAMA_TAMPIL[kunci]}: catatan acuan tidak ditemukan (`{a['berkas']}`).")
        elif a["status"] == "BUKAN_TABEL_12":
            L.append(f"- {NAMA_TAMPIL[kunci]}: catatan acuan bukan lari Tabel 12 (`{a['berkas']}`).")
        else:
            deret = lambda v: ", ".join(angka(x) for x in v)
            kata = {"COCOK": "cocok persis", "BEDA": "BERBEDA",
                    "SETARA": "setara (F1 tiap epoch identik; nilai rugi berbeda sebatas derau numerik)"}
            L.append(f"- {NAMA_TAMPIL[kunci]}: **{kata[a['status']]}** "
                     f"dengan catatan lari utama. F1-pasangan pengembangan per epoch, lari utama: "
                     f"{deret(a['f1_pasangan_acuan'])}; pencarian ini: {deret(a['f1_pasangan_kini'])}."
                     + ("" if a["status"] == "COCOK" else
                        f" Selisih terbesar F1-pasangan {angka(a['selisih_maks_f1_pasangan'])} poin. "
                        f"Versi lari utama: {a['versi_acuan']} pada {a['perangkat_acuan']}; "
                        f"pencarian: {a['versi_kini']} pada {a['perangkat_kini']}.")
                     + (f" PERINGATAN: berkas {a['data_berbeda']} berbeda dari yang dipakai lari utama."
                        if a["data_berbeda"] else ""))
    L += ["", "## Berkas yang dibaca", ""]
    for n in HIMPUNAN:
        L.append(f"- `{Path(data[n]['jalur']).name}` ({len(data[n]['teks'])} baris), "
                 f"SHA-256 `{data[n]['sha256']}`")
    L += ["", "Himpunan uji takberpasangan dan uji berpasangan tidak dibuka oleh skrip ini.", ""]
    return "\n".join(L)


# =============================================================================
# UTAMA
# =============================================================================
def main():
    ap = argparse.ArgumentParser(description=__doc__.split("Pemakaian")[0],
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--data-dir", required=True, type=Path)
    ap.add_argument("--keluaran-dir", required=True, type=Path,
                    help="folder khusus pencarian; jangan sama dengan folder lari utama")
    ap.add_argument("--acuan-dir", type=Path, default=None,
                    help="folder lari utama yang memuat catatan_lari_<model>_benih42.json")
    ap.add_argument("--lanjut-walau-beda", action="store_true",
                    help="tetap meneruskan pencarian walau lari Tabel 12 tidak mereproduksi lari utama")
    ap.add_argument("--ringkas-saja", action="store_true",
                    help="tidak melatih; menyusun tabel dan ringkasan dari lari yang sudah ada")
    ap.add_argument("--model-indobert", default=None)
    ap.add_argument("--model-indobertweet", default=None)
    ap.add_argument("--peta-kolom", type=Path, default=None)
    ap.add_argument("--tumpukan-prediksi", type=int, default=64)
    args = ap.parse_args()

    if args.model_indobert:
        MODEL["indobert"]["hf"] = args.model_indobert
    if args.model_indobertweet:
        MODEL["indobertweet"]["hf"] = args.model_indobertweet
    peta = json.loads(args.peta_kolom.read_text(encoding="utf-8")) if args.peta_kolom else {}
    dasar = args.keluaran_dir

    try:
        if (dasar / "prediksi").exists() or list(dasar.glob("catatan_lari_*.json")):
            raise GalatData(f"{dasar} adalah folder lari utama. Pakai folder tersendiri untuk "
                            f"pencarian, mis. --keluaran-dir keluaran_pencarian.")
        cetak("Memuat himpunan latih dan pengembangan (himpunan uji tidak dibuka) ...")
        data = {}
        for n in HIMPUNAN:
            jalur = args.data_dir / lp.BERKAS[n]
            if not jalur.exists():
                raise GalatData(f"Berkas tidak ditemukan: {jalur}")
            data[n] = lp.muat_himpunan(jalur, n, peta)
        gerbang = lp.gerbang_kebocoran(data)
        cetak("  LOLOS: tidak ada pengenal maupun teks ternormalkan yang muncul di kedua himpunan.")

        dasar.mkdir(parents=True, exist_ok=True)
        kombinasi, acuan = daftar_kombinasi(), {}
        rencana = [(k, m) for k in kombinasi for m in MODEL]
        selesai = {(m, k): muat_selesai(dasar, m, k, data) for k, m in rencana}
        sisa = [(k, m) for k, m in rencana if selesai[(m, k)] is None]
        cetak(f"\n{len(kombinasi)} kombinasi x {len(MODEL)} model = {len(rencana)} lari; "
              f"{len(rencana) - len(sisa)} sudah selesai, {len(sisa)} tersisa.")

        def cek_acuan():
            if args.acuan_dir is None or any(selesai[(m, TABEL_12)] is None for m in MODEL):
                return {}
            a = periksa_acuan(args.acuan_dir, {m: selesai[(m, TABEL_12)] for m in MODEL}, data)
            cetak("\nPemeriksaan reproduksi lari utama (kombinasi Tabel 12):")
            for m, r in a.items():
                if r["status"] in ("COCOK", "SETARA", "BEDA"):
                    cetak(f"  {m:<13} {r['status']:<6} lari utama {r['f1_pasangan_acuan']} | "
                          f"pencarian {r['f1_pasangan_kini']}")
                else:
                    cetak(f"  {m:<13} {r['status']}: {r['berkas']}")
            return a

        acuan = cek_acuan()
        if not args.ringkas_saja:
            mulai, n_lari = time.time(), 0
            for i, (k, m) in enumerate(sisa, 1):
                cetak(f"\n>>> lari {i}/{len(sisa)}: {m}, {nama_kombinasi(*k)}"
                      + (f"   (perkiraan sisa {(time.time() - mulai) / n_lari * (len(sisa) - n_lari) / 60:.0f} menit)"
                         if n_lari else ""))
                selesai[(m, k)] = jalankan(dasar, m, k, data, args)
                n_lari += 1
                if k == TABEL_12 and all(selesai[(x, TABEL_12)] is not None for x in MODEL):
                    acuan = cek_acuan()
                    beda = [x for x, r in acuan.items() if r["status"] == "BEDA"]
                    if beda and not args.lanjut_walau_beda:
                        raise GalatData(
                            f"lari Tabel 12 pada pencarian ini TIDAK mereproduksi lari utama untuk "
                            f"{beda}. Pencarian dihentikan sebelum {len(sisa) - n_lari} lari sisanya.\n"
                            f"  Sebab yang mungkin: (1) versi torch/transformers atau GPU berbeda dari "
                            f"lari utama (bandingkan 'versi' pada catatan); (2) latih_prediksi.py di "
                            f"folder ini bukan versi yang dipakai lari utama.\n"
                            f"  Kirimkan keluaran ini bila ragu. Untuk meneruskan apa adanya, jalankan "
                            f"ulang perintah yang sama dengan --lanjut-walau-beda (lari yang sudah "
                            f"selesai tidak diulang).")

        tabel, riwayat, cacah, belum = susun_tabel(dasar, data)
        selang = None
        if len(tabel):
            tabel = urutkan(tabel)
            if belum:
                tabel["terpilih"] = False          # peringkat masih sementara
            else:
                m = tabel[tabel.terpilih].iloc[0]
                menang = (m.laju_belajar, int(m.ukuran_tumpukan), int(m.epoch))
                if menang != TABEL_12:
                    selang = bootstrap_selisih({x: cacah[(x, menang)] for x in MODEL},
                                               {x: cacah[(x, TABEL_12)] for x in MODEL},
                                               N_BOOTSTRAP, BENIH)
            tulis_g = lambda df: df.assign(laju_belajar=df.laju_belajar.map(lambda x: f"{x:g}"))
            tulis_g(tabel).to_csv(dasar / "pencarian_hiperparameter.csv", index=False,
                                  float_format="%.4f")
            tulis_g(riwayat).to_csv(dasar / "pencarian_riwayat.csv", index=False)
        ringkasan = tulis_ringkasan(tabel, selang, acuan, data, belum, args)
        (dasar / "ringkasan_pencarian.md").write_text(ringkasan, encoding="utf-8")
        (dasar / "catatan_pencarian.json").write_text(json.dumps({
            "kisi": {"laju_belajar": KISI_LAJU_BELAJAR, "ukuran_tumpukan": KISI_UKURAN_TUMPUKAN,
                     "epoch": KISI_EPOCH},
            "aturan": {"skor": "rerata F1-pasangan pengembangan kedua model, akhir epoch terakhir",
                       "ambang_seri_pp": AMBANG_SERI,
                       "pemutus_seri": ["epoch", "laju_belajar", "ukuran_tumpukan"]},
            "benih": BENIH, "model": {k: v for k, v in MODEL.items()},
            "berkas_dibaca": {n: {"jalur": data[n]["jalur"], "sha256": data[n]["sha256"],
                                  "baris": len(data[n]["teks"])} for n in HIMPUNAN},
            "himpunan_uji_dibuka": False, "gerbang_kebocoran": gerbang,
            "lari_selesai": len(rencana) - len(belum), "lari_total": len(rencana),
            "pemeriksaan_acuan": acuan, "selang_terpilih_vs_tabel_12": selang,
        }, indent=2, ensure_ascii=False), encoding="utf-8")
        cetak("\n" + ringkasan)
        cetak(f"Berkas ditulis di {dasar}")
    except GalatData as g:
        cetak(f"\nGALAT: {g}")
        sys.exit(1)


if __name__ == "__main__":
    main()
