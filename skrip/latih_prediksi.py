#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
latih_prediksi.py
=================
Penalaan halus IndoBERT dan IndoBERTweet sebagai klasifikasi multi-kepala
(5 kepala aspek x 3 kelas) dan penyimpanan PREDIKSI MENTAH PER BUTIR.

Skrip ini TIDAK menghitung angka kinerja akhir. Seluruh metrik, Delta-F1,
Delta-kuadrat, McNemar, dan bootstrap dikerjakan `evaluasi_statistik.py` dari
berkas prediksi yang ditulis di sini, sehingga pengujian dapat diulang tanpa
melatih ulang.

Pemakaian
---------
  # 1) periksa skema, gerbang kebocoran, sebaran label, pemotongan token (tanpa melatih)
  python latih_prediksi.py --data-dir data/05_pembagian --keluaran-dir keluaran --periksa

  # 2) latih kedua model lalu tulis prediksi
  python latih_prediksi.py --data-dir data/05_pembagian --keluaran-dir keluaran

  # pilihan
  --hanya indobert            melatih satu model saja
  --benih 43                  benih lain (analisis kepekaan; berkas keluaran tidak saling menimpa)
  --laju-belajar 3e-5 --ukuran-tumpukan 32 --epoch 3
                              mengganti tiga hiperparameter hasil pencarian (bawaan: Tabel 12).
                              Satu --keluaran-dir hanya boleh berisi satu konfigurasi; benih
                              lain dengan konfigurasi yang sama boleh masuk folder yang sama.
  --model-indobert NAMA       mengganti pengenal Hugging Face tanpa menyunting skrip
  --peta-kolom peta.json      memaksa nama kolom bila deteksi otomatis keliru
  --simpan-model              menyimpan bobot hasil penalaan (sekitar 440 MB per model)

Keluaran (di dalam --keluaran-dir)
----------------------------------
  prediksi/<model>_benih<b>_<himpunan>.csv   satu baris per (ulasan, register, aspek):
        emas, prediksi (argmax tiga kelas), prediksi_polaritas (argmax atas
        NEGATIF/POSITIF saja), ketiga logit, dan penanda terpotong
  catatan_lari_<model>_benih<b>.json         konfigurasi, hash berkas, versi pustaka,
        perangkat keras, kinerja pengembangan per epoch, diagnostik pemotongan
"""
import os

os.environ.setdefault("CUBLAS_WORKSPACE_CONFIG", ":4096:8")   # syarat determinisme cuBLAS
os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")

import argparse
import hashlib
import json
import platform
import random
import re
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

# =============================================================================
# KONFIGURASI TERKUNCI (Tabel 12 Bab III) -- jangan diubah tanpa mengubah naskah
# =============================================================================
MODEL = {
    "indobert":     {"hf": "indolem/indobert-base-uncased",     "panjang_maks": 97},
    "indobertweet": {"hf": "indolem/indobertweet-base-uncased", "panjang_maks": 92},
}
LAJU_BELAJAR = 2e-5
UKURAN_TUMPUKAN = 16
EPOCH = 4
PELURUHAN_BOBOT = 0.01
PROPORSI_PEMANASAN = 0.10
BENIH = 42
TABEL_12 = (2e-5, 16, 4)       # nilai awal pada naskah, untuk pembanding
HIMPUNAN_PREDIKSI = ("pengembangan", "uji_takberpasangan", "uji_berpasangan")


def atur_hiperparameter(laju_belajar: float, ukuran_tumpukan: int, epoch: int):
    """Mengganti tiga hiperparameter hasil pencarian; dipakai main() dan cari_hiperparameter.py."""
    global LAJU_BELAJAR, UKURAN_TUMPUKAN, EPOCH
    LAJU_BELAJAR, UKURAN_TUMPUKAN, EPOCH = float(laju_belajar), int(ukuran_tumpukan), int(epoch)

# Nilai bawaan yang TIDAK tercantum pada Tabel 12 (dicatat di catatan_lari agar terlapor)
DROPOUT_KEPALA = 0.1          # bawaan kepala klasifikasi BERT
BATAS_NORMA_GRADIEN = 1.0     # bawaan Trainer Hugging Face
# Model yang dipakai untuk prediksi = bobot pada akhir epoch terakhir (tanpa memilih
# titik simpan terbaik), karena Tabel 12 menetapkan jumlah epoch, bukan penghentian dini.

# =============================================================================
# SKEMA DATA
# =============================================================================
ASPEK = ["keamanan_akun", "autentikasi", "privasi_data", "antarmuka", "keandalan"]
LABEL = ["TIDAK_ADA", "NEGATIF", "POSITIF"]          # indeks kelas 0, 1, 2
REGISTER = ["FORMAL", "INFORMAL"]
BERKAS = {
    "latih": "latih.csv",
    "pengembangan": "pengembangan.csv",
    "uji_takberpasangan": "uji_takberpasangan.csv",
    "uji_berpasangan": "uji_berpasangan.csv",
}
# Jumlah baris yang diharapkan. Sunting hanya bila pembagian data memang dibuat ulang.
UKURAN_HARAPAN = {"latih": 1650, "pengembangan": 291,
                  "uji_takberpasangan": 744, "uji_berpasangan": 1146}

NAMA_TEKS = ["teks", "text", "ulasan", "teks_ulasan", "isi", "isi_ulasan", "content",
             "review", "teks_tersamar", "ulasan_tersamar", "teks_final", "kalimat"]
NAMA_ID = ["id_ulasan", "id", "uid", "kunci", "id_pasangan", "pair_id", "review_id",
           "id_review", "no", "nomor"]
NAMA_REGISTER = ["register", "ragam", "versi"]
KATA_BUKAN_EMAS = ["usulan", "llm", "pred", "saran", "anotator", "conf", "alasan",
                   "catatan", "yakin", "skor"]


class GalatData(Exception):
    """Galat yang menghentikan lari sebelum pelatihan dimulai."""


def cetak(*a):
    print(*a, flush=True)


# =============================================================================
# PEMUATAN DAN DETEKSI KOLOM
# =============================================================================
def baca_csv(jalur: Path) -> pd.DataFrame:
    """Membaca CSV sebagai teks murni. Pemisah ditentukan dari baris judul."""
    with open(jalur, "r", encoding="utf-8-sig", newline="") as f:
        judul = f.readline()
    pemisah = max([",", ";", "\t"], key=judul.count)
    df = pd.read_csv(jalur, dtype=str, keep_default_na=False, sep=pemisah,
                     encoding="utf-8-sig")
    df.columns = [str(c).strip() for c in df.columns]
    return df


def sha256_berkas(jalur: Path) -> str:
    h = hashlib.sha256()
    with open(jalur, "rb") as f:
        for potong in iter(lambda: f.read(1 << 20), b""):
            h.update(potong)
    return h.hexdigest()


def _nilai_label(seri: pd.Series) -> pd.Series:
    return seri.astype(str).str.strip().str.upper().str.replace(r"[\s\-]+", "_", regex=True)


def deteksi_kolom(df: pd.DataFrame, nama: str, berpasangan: bool, peta: dict) -> dict:
    """Menentukan kolom teks, pengenal, register, dan lima kolom aspek.

    Urutan: (1) --peta-kolom, (2) nama baku, (3) penelusuran berdasar isi.
    Gagal dengan pesan jelas bila rancu -- tidak pernah menebak diam-diam.
    """
    rendah = {c: c.lower() for c in df.columns}
    hasil = {"aspek": {}}

    # --- lima kolom aspek -----------------------------------------------------
    for a in ASPEK:
        if a in peta.get("aspek", {}):
            kol = peta["aspek"][a]
            if kol not in df.columns:
                raise GalatData(f"[{nama}] kolom '{kol}' (peta-kolom, aspek {a}) tidak ada.")
            hasil["aspek"][a] = kol
            continue
        tingkat = [
            {a, f"asp_{a}"},
            {f"label_{a}", f"label_asp_{a}", f"emas_{a}", f"emas_asp_{a}", f"final_{a}",
             f"final_asp_{a}", f"{a}_emas", f"asp_{a}_emas", f"{a}_final", f"asp_{a}_final"},
        ]
        calon = []
        for himp in tingkat:
            calon = [c for c in df.columns if rendah[c] in himp]
            if calon:
                break
        if not calon:   # penelusuran berdasar isi
            calon = [c for c in df.columns
                     if a in rendah[c]
                     and not any(k in rendah[c] for k in KATA_BUKAN_EMAS)
                     and set(_nilai_label(df[c]).unique()) <= set(LABEL)]
        if len(calon) != 1:
            raise GalatData(
                f"[{nama}] kolom label aspek '{a}' tidak dapat ditentukan "
                f"(calon: {calon or 'tidak ada'}). Kolom tersedia: {list(df.columns)}. "
                f"Tetapkan lewat --peta-kolom.")
        hasil["aspek"][a] = calon[0]
    kol_aspek = set(hasil["aspek"].values())

    # --- register -------------------------------------------------------------
    kol_reg = peta.get("register")
    if kol_reg is None:
        calon = [c for c in df.columns if rendah[c] in NAMA_REGISTER]
        if not calon:
            calon = [c for c in df.columns if c not in kol_aspek
                     and set(df[c].str.strip().str.upper().unique()) <= set(REGISTER)]
        kol_reg = calon[0] if calon else None
    elif kol_reg not in df.columns:
        raise GalatData(f"[{nama}] kolom register '{kol_reg}' (peta-kolom) tidak ada.")
    if berpasangan and kol_reg is None:
        raise GalatData(f"[{nama}] kolom register tidak ditemukan pada berkas berpasangan.")
    hasil["register"] = kol_reg

    # --- teks -----------------------------------------------------------------
    kol_teks = peta.get("teks")
    lain = [c for c in df.columns if c not in kol_aspek and c != kol_reg]
    mirip_teks = [c for c in lain if df[c].str.len().mean() > 20
                  and df[c].str.contains(" ").mean() > 0.5]
    if kol_teks is None:
        calon = [c for n in NAMA_TEKS for c in lain if rendah[c] == n]
        if calon:
            kol_teks = calon[0]
        elif mirip_teks:
            kol_teks = max(mirip_teks, key=lambda c: df[c].str.len().mean())
        else:
            raise GalatData(f"[{nama}] kolom teks tidak ditemukan. Kolom: {list(df.columns)}")
    elif kol_teks not in df.columns:
        raise GalatData(f"[{nama}] kolom teks '{kol_teks}' (peta-kolom) tidak ada.")
    hasil["teks"] = kol_teks
    hasil["teks_lain"] = [c for c in mirip_teks if c != kol_teks]

    # --- pengenal ---------------------------------------------------------------
    def sah_sebagai_id(c):
        hitung = df[c].value_counts()
        if (df[c].str.strip() == "").any():
            return False
        if not berpasangan:
            return bool((hitung == 1).all())
        if not bool((hitung == 2).all()):
            return False
        reg = df[kol_reg].str.strip().str.upper()
        return bool((df.assign(_r=reg).groupby(c)["_r"].nunique() == 2).all())

    kol_id = peta.get("id")
    if kol_id is not None:
        if kol_id not in df.columns:
            raise GalatData(f"[{nama}] kolom pengenal '{kol_id}' (peta-kolom) tidak ada.")
        if not sah_sebagai_id(kol_id):
            raise GalatData(f"[{nama}] kolom '{kol_id}' tidak memenuhi syarat pengenal "
                            f"({'tepat dua baris, satu per register' if berpasangan else 'unik'}).")
    else:
        bukan = kol_aspek | {kol_reg, kol_teks} | set(hasil["teks_lain"])
        urut = [c for n in NAMA_ID for c in df.columns if rendah[c] == n]
        urut += [c for c in df.columns if c not in urut and c not in bukan]
        kol_id = next((c for c in urut if sah_sebagai_id(c)), None)
        if kol_id is None and berpasangan:
            raise GalatData(
                f"[{nama}] tidak ada kolom yang menghubungkan kedua versi sebuah pasangan "
                f"(tiap nilai harus muncul tepat dua kali, sekali per register). "
                f"Kolom: {list(df.columns)}. Tetapkan lewat --peta-kolom.")
    hasil["id"] = kol_id
    return hasil


def muat_himpunan(jalur: Path, nama: str, peta: dict) -> dict:
    berpasangan = nama == "uji_berpasangan"
    df = baca_csv(jalur)
    if len(df) != UKURAN_HARAPAN[nama]:
        raise GalatData(
            f"[{nama}] {len(df)} baris, diharapkan {UKURAN_HARAPAN[nama]}. Bila pembagian "
            f"data memang dibuat ulang, sunting UKURAN_HARAPAN; bila tidak, berkas ini keliru.")
    kol = deteksi_kolom(df, nama, berpasangan, peta)

    y = np.zeros((len(df), len(ASPEK)), dtype=np.int64)
    for j, a in enumerate(ASPEK):
        nilai = _nilai_label(df[kol["aspek"][a]])
        asing = sorted(set(nilai.unique()) - set(LABEL))
        if asing:
            raise GalatData(f"[{nama}] kolom '{kol['aspek'][a]}' memuat nilai di luar "
                            f"{LABEL}: {asing[:8]}")
        y[:, j] = nilai.map({l: i for i, l in enumerate(LABEL)}).to_numpy()

    teks = df[kol["teks"]].astype(str).str.strip().tolist()
    if any(t == "" for t in teks):
        raise GalatData(f"[{nama}] ada teks kosong pada kolom '{kol['teks']}'.")

    if kol["register"] is not None:
        register = df[kol["register"]].str.strip().str.upper().tolist()
        asing = sorted(set(register) - set(REGISTER))
        if asing:
            raise GalatData(f"[{nama}] nilai register tak dikenal: {asing[:8]}")
    else:
        register = [""] * len(df)

    id_asli = kol["id"] is not None
    ids = (df[kol["id"]].str.strip().tolist() if id_asli
           else [f"{nama}_{i:05d}" for i in range(len(df))])

    if berpasangan:   # kelengkapan pasangan dan pewarisan label
        s = pd.DataFrame({"id": ids, "reg": register, "pola": ["".join(map(str, r)) for r in y]})
        if not (s.groupby("id")["reg"].apply(lambda r: sorted(r) == REGISTER)).all():
            raise GalatData(f"[{nama}] ada pasangan yang tidak berisi tepat satu FORMAL dan "
                            f"satu INFORMAL.")
        beda = s.groupby("id")["pola"].nunique()
        if (beda > 1).any():
            raise GalatData(f"[{nama}] {int((beda > 1).sum())} pasangan berlabel TIDAK identik "
                            f"antara kedua versinya, mis. {list(beda[beda > 1].index[:5])}.")

    return {"nama": nama, "jalur": str(jalur), "sha256": sha256_berkas(jalur), "kolom": kol,
            "id": ids, "id_asli": id_asli, "teks": teks, "register": register, "y": y}


# =============================================================================
# GERBANG KEBOCORAN DATA (Subbab 3.5.3) -- dijalankan ulang sebelum tiap penalaan
# =============================================================================
def _sidik_teks(t: str) -> str:
    return hashlib.md5(re.sub(r"\s+", " ", t.lower()).strip().encode("utf-8")).hexdigest()


def gerbang_kebocoran(data: dict) -> dict:
    """Membatalkan lari bila ada kebocoran. Mengembalikan catatan pemeriksaan."""
    catatan, galat = {}, []
    nama = list(data)
    semua_id_asli = all(d["id_asli"] for d in data.values())

    # (a)+(b) pengenal tidak beririsan antarhimpunan; pasangan tidak ada di latih/pengembangan
    if semua_id_asli:
        for i in range(len(nama)):
            for j in range(i + 1, len(nama)):
                iris = set(data[nama[i]]["id"]) & set(data[nama[j]]["id"])
                catatan[f"irisan_id:{nama[i]}~{nama[j]}"] = len(iris)
                if iris:
                    galat.append(f"{len(iris)} pengenal muncul di {nama[i]} dan {nama[j]} "
                                 f"(mis. {sorted(iris)[:3]})")
    else:
        catatan["irisan_id"] = "DILEWATI: tidak semua berkas berkolom pengenal"
        cetak("  PERINGATAN: pemeriksaan irisan pengenal dilewati (ada berkas tanpa kolom "
              "pengenal); gerbang bersandar pada sidik teks saja.")

    # (c) teks identik setelah normalisasi tidak boleh lintas himpunan
    sidik = {n: {_sidik_teks(t) for t in d["teks"]} for n, d in data.items()}
    for i in range(len(nama)):
        for j in range(i + 1, len(nama)):
            iris = sidik[nama[i]] & sidik[nama[j]]
            catatan[f"irisan_teks:{nama[i]}~{nama[j]}"] = len(iris)
            if iris:
                contoh = next(t for t in data[nama[i]]["teks"] if _sidik_teks(t) in iris)
                galat.append(f"{len(iris)} teks identik (ternormalkan) muncul di {nama[i]} "
                             f"dan {nama[j]}, mis. \"{contoh[:70]}\"")
    if galat:
        raise GalatData("GERBANG KEBOCORAN GAGAL -- pelatihan dibatalkan:\n  - "
                        + "\n  - ".join(galat))
    return catatan


def cetak_sebaran(data: dict):
    for n, d in data.items():
        cetak(f"\n  [{n}] {len(d['teks'])} baris | kolom: teks='{d['kolom']['teks']}', "
              f"id='{d['kolom']['id']}', register='{d['kolom']['register']}'")
        if d["kolom"]["teks_lain"]:
            cetak(f"    PERINGATAN: ada kolom lain yang mirip teks {d['kolom']['teks_lain']}; "
                  f"yang dipakai '{d['kolom']['teks']}'. Pastikan ini versi yang dimaksud "
                  f"(mis. versi tersamar).")
        y = d["y"]
        if n == "uji_berpasangan":      # hitung sekali per pasangan
            y = y[np.array(d["register"]) == "INFORMAL"]
            cetak(f"    (sebaran dihitung per pasangan, n = {len(y)})")
        for j, a in enumerate(ASPEK):
            h = np.bincount(y[:, j], minlength=3)
            cetak(f"    {a:<15} kolom='{d['kolom']['aspek'][a]}'  "
                  + "  ".join(f"{LABEL[k]}={h[k]}" for k in range(3)))
        if n == "uji_berpasangan":
            for g, idx in (("keamanan", [0, 1, 2]), ("kontrol", [3, 4])):
                sub = y[:, idx]
                cetak(f"    kelompok {g:<9} butir emas ADA = {(sub != 0).sum()}, "
                      f"NEGATIF = {(sub == 1).sum()}, POSITIF = {(sub == 2).sum()}")


# =============================================================================
# TOKENISASI
# =============================================================================
def tokenisasi(tokenizer, teks: list, panjang_maks: int):
    penuh = tokenizer(teks, add_special_tokens=True, truncation=False)["input_ids"]
    panjang = np.array([len(x) for x in penuh])
    terpotong = panjang > panjang_maks
    ids = tokenizer(teks, add_special_tokens=True, truncation=True,
                    max_length=panjang_maks)["input_ids"]
    return ids, panjang, terpotong


def diagnostik_token(panjang, terpotong, register) -> dict:
    d = {"p95": float(np.percentile(panjang, 95)), "maks": int(panjang.max()),
         "persen_terpotong": round(100 * float(terpotong.mean()), 2)}
    reg = np.array(register)
    for r in REGISTER:
        if (reg == r).any():
            d[f"persen_terpotong_{r}"] = round(100 * float(terpotong[reg == r].mean()), 2)
            d[f"rerata_token_{r}"] = round(float(panjang[reg == r].mean()), 2)
    return d


# =============================================================================
# MODEL DAN PELATIHAN
# =============================================================================
def bangun_dan_latih(kunci: str, data: dict, args, dir_keluar: Path,
                     himpunan_prediksi=HIMPUNAN_PREDIKSI):
    """Melatih satu model lalu menulis prediksi mentah untuk `himpunan_prediksi`.

    `data` cukup memuat "latih", "pengembangan", dan himpunan yang diprediksi, sehingga
    pencarian hiperparameter dapat memanggil fungsi ini tanpa memuat himpunan uji.
    """
    import torch
    import torch.nn as nn
    import transformers
    from transformers import AutoModel, AutoTokenizer, get_linear_schedule_with_warmup

    nama_hf = MODEL[kunci]["hf"]
    panjang_maks = MODEL[kunci]["panjang_maks"]
    perangkat = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    def atur_benih(b):
        random.seed(b)
        np.random.seed(b)
        torch.manual_seed(b)
        torch.cuda.manual_seed_all(b)
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False
        try:
            torch.use_deterministic_algorithms(True, warn_only=True)
        except Exception:
            pass

    atur_benih(args.benih)   # diatur ulang per model: urutan tumpukan kedua model identik
    cetak(f"\n{'=' * 78}\n{kunci}  <-  {nama_hf}   (panjang maks {panjang_maks}, "
          f"benih {args.benih}, {perangkat})\n{'=' * 78}")

    tokenizer = AutoTokenizer.from_pretrained(nama_hf)
    tok, diag = {}, {}
    for n, d in data.items():
        ids, panjang, terpotong = tokenisasi(tokenizer, d["teks"], panjang_maks)
        tok[n] = {"ids": ids, "terpotong": terpotong}
        diag[n] = diagnostik_token(panjang, terpotong, d["register"])
        cetak(f"  token [{n:<19}] p95 = {diag[n]['p95']:.0f}, terpotong = "
              f"{diag[n]['persen_terpotong']:.2f}%"
              + "".join(f", {r} = {diag[n][f'persen_terpotong_{r}']:.2f}%"
                        for r in REGISTER if f"persen_terpotong_{r}" in diag[n]))
    if args.periksa:
        return {"tokenisasi": diag}

    class ModelMultiKepala(nn.Module):
        """Enkoder BERT + lima kepala linear bebas (masing-masing tiga kelas) di atas [CLS].

        Lapis pooler tidak dipakai: bobot pooler IndoBERTweet tidak dilatih pada
        prapelatihan (MLM saja), sehingga memakainya membuat kedua model berangkat
        dari keadaan yang tidak setara. Keduanya memakai vektor [CLS] lapis akhir.
        """

        def __init__(self):
            super().__init__()
            try:
                self.enkoder = AutoModel.from_pretrained(nama_hf, add_pooling_layer=False)
            except TypeError:
                self.enkoder = AutoModel.from_pretrained(nama_hf)
            h = self.enkoder.config.hidden_size
            self.dropout = nn.Dropout(DROPOUT_KEPALA)
            self.kepala = nn.ModuleList([nn.Linear(h, len(LABEL)) for _ in ASPEK])
            simpangan = getattr(self.enkoder.config, "initializer_range", 0.02)
            for k in self.kepala:
                nn.init.normal_(k.weight, std=simpangan)
                nn.init.zeros_(k.bias)

        def forward(self, input_ids, attention_mask):
            cls = self.enkoder(input_ids=input_ids,
                               attention_mask=attention_mask).last_hidden_state[:, 0]
            cls = self.dropout(cls)
            return torch.stack([k(cls) for k in self.kepala], dim=1)   # [B, 5, 3]

    model = ModelMultiKepala().to(perangkat)
    id_pad = tokenizer.pad_token_id

    def susun(butir):
        maks = max(len(b[0]) for b in butir)
        ids = torch.full((len(butir), maks), id_pad, dtype=torch.long)
        topeng = torch.zeros((len(butir), maks), dtype=torch.long)
        for i, (x, _) in enumerate(butir):
            ids[i, :len(x)] = torch.tensor(x)
            topeng[i, :len(x)] = 1
        return ids, topeng, torch.tensor(np.stack([b[1] for b in butir]), dtype=torch.long)

    def pemuat(n, acak):
        butir = list(zip(tok[n]["ids"], data[n]["y"]))
        g = torch.Generator().manual_seed(args.benih)
        return torch.utils.data.DataLoader(
            butir, batch_size=UKURAN_TUMPUKAN if acak else args.tumpukan_prediksi,
            shuffle=acak, generator=g if acak else None, collate_fn=susun, num_workers=0)

    rugi_fn = nn.CrossEntropyLoss()   # tanpa bobot kelas (tidak ada pada Tabel 12)

    @torch.no_grad()
    def prediksi(n):
        model.eval()
        logit, rugi, m = [], 0.0, 0
        for ids, topeng, y in pemuat(n, acak=False):
            z = model(ids.to(perangkat), topeng.to(perangkat))
            rugi += rugi_fn(z.reshape(-1, len(LABEL)), y.to(perangkat).reshape(-1)).item() * len(y)
            m += len(y)
            logit.append(z.float().cpu().numpy())
        return np.concatenate(logit), rugi / m

    def f1_mikro(tp, fp, fn):
        return 100 * 2 * tp / (2 * tp + fp + fn) if (2 * tp + fp + fn) else float("nan")

    def ringkas_pengembangan(logit, y):
        p = logit.argmax(-1)
        ada_e, ada_p = y != 0, p != 0
        acd = f1_mikro((ada_e & ada_p).sum(), (~ada_e & ada_p).sum(), (ada_e & ~ada_p).sum())
        psg = f1_mikro((ada_e & (p == y)).sum(), (ada_p & (p != y)).sum(), (ada_e & (p != y)).sum())
        return float(acd), float(psg)

    tanpa_peluruhan = ("bias", "LayerNorm.weight", "LayerNorm.bias")
    kelompok = [
        {"params": [p for n, p in model.named_parameters()
                    if not any(t in n for t in tanpa_peluruhan)], "weight_decay": PELURUHAN_BOBOT},
        {"params": [p for n, p in model.named_parameters()
                    if any(t in n for t in tanpa_peluruhan)], "weight_decay": 0.0},
    ]
    pengoptimal = torch.optim.AdamW(kelompok, lr=LAJU_BELAJAR)
    pemuat_latih = pemuat("latih", acak=True)
    langkah_total = len(pemuat_latih) * EPOCH
    langkah_pemanasan = int(round(PROPORSI_PEMANASAN * langkah_total))
    penjadwal = get_linear_schedule_with_warmup(pengoptimal, langkah_pemanasan, langkah_total)
    cetak(f"  {len(pemuat_latih)} langkah/epoch x {EPOCH} epoch = {langkah_total} langkah "
          f"(pemanasan {langkah_pemanasan}; laju belajar {LAJU_BELAJAR:g}, tumpukan {UKURAN_TUMPUKAN})")

    riwayat, mulai = [], time.time()
    for ep in range(1, EPOCH + 1):
        model.train()
        jumlah, m = 0.0, 0
        for ids, topeng, y in pemuat_latih:
            pengoptimal.zero_grad(set_to_none=True)
            z = model(ids.to(perangkat), topeng.to(perangkat))
            rugi = rugi_fn(z.reshape(-1, len(LABEL)), y.to(perangkat).reshape(-1))
            rugi.backward()
            nn.utils.clip_grad_norm_(model.parameters(), BATAS_NORMA_GRADIEN)
            pengoptimal.step()
            penjadwal.step()
            jumlah += rugi.item() * len(y)
            m += len(y)
        logit_bang, rugi_bang = prediksi("pengembangan")
        acd, psg = ringkas_pengembangan(logit_bang, data["pengembangan"]["y"])
        riwayat.append({"epoch": ep, "rugi_latih": round(jumlah / m, 5),
                        "rugi_pengembangan": round(rugi_bang, 5),
                        "f1_acd_pengembangan": round(acd, 2),
                        "f1_pasangan_pengembangan": round(psg, 2)})
        cetak(f"  epoch {ep}/{EPOCH}  rugi latih {jumlah / m:.4f} | pengembangan: rugi "
              f"{rugi_bang:.4f}, F1-ACD {acd:.2f}, F1-pasangan {psg:.2f}")
    lama = time.time() - mulai

    # ---- prediksi mentah per butir -------------------------------------------
    dir_pred = dir_keluar / "prediksi"
    dir_pred.mkdir(parents=True, exist_ok=True)
    for n in himpunan_prediksi:
        logit, _ = prediksi(n)                                  # [N, 5, 3]
        d = data[n]
        pred = logit.argmax(-1)                                 # keputusan tiga kelas
        pol = logit[:, :, 1:].argmax(-1) + 1                    # NEGATIF vs POSITIF saja
        baris = []
        for i in range(len(d["id"])):
            for j, a in enumerate(ASPEK):
                baris.append({
                    "model": kunci, "hf": nama_hf, "benih": args.benih, "himpunan": n,
                    "id_ulasan": d["id"][i], "register": d["register"][i], "aspek": a,
                    "emas": LABEL[d["y"][i, j]], "prediksi": LABEL[pred[i, j]],
                    "prediksi_polaritas": LABEL[pol[i, j]],
                    "logit_TIDAK_ADA": f"{logit[i, j, 0]:.6f}",
                    "logit_NEGATIF": f"{logit[i, j, 1]:.6f}",
                    "logit_POSITIF": f"{logit[i, j, 2]:.6f}",
                    "terpotong": int(tok[n]["terpotong"][i]),
                })
        tujuan = dir_pred / f"{kunci}_benih{args.benih}_{n}.csv"
        pd.DataFrame(baris).to_csv(tujuan, index=False, encoding="utf-8")
        cetak(f"  prediksi -> {tujuan}  ({len(baris)} butir)")

    if args.simpan_model:
        dir_model = dir_keluar / "model" / f"{kunci}_benih{args.benih}"
        dir_model.mkdir(parents=True, exist_ok=True)
        torch.save(model.state_dict(), dir_model / "bobot.pt")
        tokenizer.save_pretrained(dir_model)

    return {
        "tokenisasi": diag, "riwayat": riwayat, "detik_pelatihan": round(lama, 1),
        "langkah_total": langkah_total, "langkah_pemanasan": langkah_pemanasan,
        "perangkat": (torch.cuda.get_device_name(0) if perangkat.type == "cuda"
                      else f"CPU ({platform.processor() or platform.machine()})"),
        "versi": {"python": platform.python_version(), "torch": torch.__version__,
                  "transformers": transformers.__version__, "numpy": np.__version__,
                  "pandas": pd.__version__},
    }


# =============================================================================
# UTAMA
# =============================================================================
def main():
    ap = argparse.ArgumentParser(description=__doc__.split("Pemakaian")[0],
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--data-dir", required=True, type=Path)
    ap.add_argument("--keluaran-dir", required=True, type=Path)
    ap.add_argument("--periksa", action="store_true",
                    help="hanya memeriksa skema, gerbang, sebaran label, dan pemotongan token")
    ap.add_argument("--hanya", choices=list(MODEL), help="melatih satu model saja")
    ap.add_argument("--benih", type=int, default=BENIH)
    ap.add_argument("--laju-belajar", type=float, default=LAJU_BELAJAR)
    ap.add_argument("--ukuran-tumpukan", type=int, default=UKURAN_TUMPUKAN)
    ap.add_argument("--epoch", type=int, default=EPOCH)
    ap.add_argument("--model-indobert", default=None, help="mengganti pengenal/jalur IndoBERT")
    ap.add_argument("--model-indobertweet", default=None,
                    help="mengganti pengenal/jalur IndoBERTweet")
    ap.add_argument("--peta-kolom", type=Path, default=None,
                    help='JSON: {"teks": "...", "id": "...", "register": "...", '
                         '"aspek": {"keamanan_akun": "..."}}')
    ap.add_argument("--tumpukan-prediksi", type=int, default=64)
    ap.add_argument("--simpan-model", action="store_true")
    args = ap.parse_args()

    atur_hiperparameter(args.laju_belajar, args.ukuran_tumpukan, args.epoch)
    kini = (LAJU_BELAJAR, UKURAN_TUMPUKAN, EPOCH)
    beda_tabel_12 = kini != TABEL_12
    if not args.periksa:
        # Satu folder keluaran = satu konfigurasi. Benih lain dengan konfigurasi yang sama boleh
        # masuk folder yang sama; konfigurasi lain harus memakai folder tersendiri.
        for j in sorted(args.keluaran_dir.glob("catatan_lari_*.json")):
            hp = json.loads(j.read_text(encoding="utf-8"))["hiperparameter"]
            ada = (hp["laju_belajar"], hp["ukuran_tumpukan"], hp["epoch"])
            if ada != kini:
                cetak(f"GALAT: {args.keluaran_dir} sudah berisi lari dengan konfigurasi lain "
                      f"({j.name}: laju belajar {ada[0]:g}, tumpukan {ada[1]}, {ada[2]} epoch), "
                      f"sedangkan lari ini memakai laju belajar {kini[0]:g}, tumpukan {kini[1]}, "
                      f"{kini[2]} epoch. Pakai --keluaran-dir lain agar hasil dua konfigurasi "
                      f"tidak tercampur.")
                sys.exit(1)
    if args.model_indobert:
        MODEL["indobert"]["hf"] = args.model_indobert
    if args.model_indobertweet:
        MODEL["indobertweet"]["hf"] = args.model_indobertweet
    peta = json.loads(args.peta_kolom.read_text(encoding="utf-8")) if args.peta_kolom else {}

    try:
        cetak("Memuat keempat berkas pembagian ...")
        data = {}
        for n, berkas in BERKAS.items():
            jalur = args.data_dir / berkas
            if not jalur.exists():
                raise GalatData(f"Berkas tidak ditemukan: {jalur}")
            data[n] = muat_himpunan(jalur, n, peta)
        cetak_sebaran(data)
        cetak("\nMenjalankan gerbang kebocoran data ...")
        catatan_gerbang = gerbang_kebocoran(data)
        cetak("  LOLOS: tidak ada pengenal maupun teks ternormalkan yang lintas himpunan; "
              "tiap pasangan lengkap dan berlabel identik.")
    except GalatData as g:
        cetak(f"\nGALAT: {g}")
        sys.exit(1)

    args.keluaran_dir.mkdir(parents=True, exist_ok=True)
    for kunci in ([args.hanya] if args.hanya else list(MODEL)):
        hasil = bangun_dan_latih(kunci, data, args, args.keluaran_dir)
        if args.periksa:
            continue
        catatan = {
            "model": kunci, "hf": MODEL[kunci]["hf"], "benih": args.benih,
            "hiperparameter": {
                "laju_belajar": LAJU_BELAJAR, "ukuran_tumpukan": UKURAN_TUMPUKAN,
                "epoch": EPOCH, "pengoptimal": "AdamW", "peluruhan_bobot": PELURUHAN_BOBOT,
                "proporsi_pemanasan": PROPORSI_PEMANASAN, "jadwal": "linear",
                "panjang_maks": MODEL[kunci]["panjang_maks"],
                "sama_dengan_tabel_12": not beda_tabel_12,
                "di_luar_tabel_12": {"dropout_kepala": DROPOUT_KEPALA,
                                     "batas_norma_gradien": BATAS_NORMA_GRADIEN,
                                     "titik_simpan": "akhir epoch terakhir",
                                     "bobot_kelas": "tidak ada",
                                     "representasi": "[CLS] lapis akhir, tanpa pooler"},
            },
            "berkas": {n: {"jalur": d["jalur"], "sha256": d["sha256"], "baris": len(d["teks"]),
                           "kolom": {k: v for k, v in d["kolom"].items()}}
                       for n, d in data.items()},
            "gerbang_kebocoran": catatan_gerbang,
            **hasil,
        }
        tujuan = args.keluaran_dir / f"catatan_lari_{kunci}_benih{args.benih}.json"
        tujuan.write_text(json.dumps(catatan, indent=2, ensure_ascii=False), encoding="utf-8")
        cetak(f"  catatan  -> {tujuan}")

    cetak("\nSelesai." + ("" if args.periksa else
          f"  Lanjutkan: python evaluasi_statistik.py --prediksi-dir "
          f"{args.keluaran_dir / 'prediksi'} --hasil-dir {args.keluaran_dir / 'hasil'}"
          + (f" --benih {args.benih}" if args.benih != BENIH else "")))


if __name__ == "__main__":
    main()
