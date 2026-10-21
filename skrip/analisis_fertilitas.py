#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
analisis_fertilitas.py
======================
Analisis mekanistik fertilitas tokenizer (Subbab 3.5.6) dan hipotesis keempat (H4).

Fertilitas = jumlah token subkata dibagi jumlah kata, dihitung pada kedua versi
(FORMAL dan INFORMAL) himpunan uji berpasangan untuk masing-masing tokenizer.
Kata = rangkaian huruf (angka, tanda baca, dan emotikon tidak dihitung), sama
dengan pemecahan kata pada skor ketakbakuan (Subbab 3.2.2). Setiap kata
ditokenisasi tersendiri tanpa token khusus; pada tokenizer WordPiece hasilnya sama
dengan tokenisasi di dalam kalimat karena pemecahan awal terjadi pada spasi dan
tanda baca.

Yang dihitung
-------------
1. Fertilitas per kelas kata: seluruh kata, kata takbaku (tercatat di leksikon
   kolokial), kata penanda aspek (daftar kata kunci Subbab 3.2.3), dan kata pembawa
   sentimen (leksikon sentimen, diperluas dengan bentuk takbaku padanannya).
2. Fertilitas per aspek: pada ulasan yang label emasnya menyatakan aspek itu hadir.
3. H4 (Subbab 3.5.5): Spearman antara selisih fertilitas antarmodel per aspek
   (IndoBERT dikurangi IndoBERTweet, versi takbaku) dan Delta-kuadrat per aspek,
   untuk tiap metrik. Lima titik, angka p eksak dua arah dari 120 permutasi.
   EKSPLORATORI, di luar koreksi Holm.
4. Diagram pencar (Subbab 3.5.6): fertilitas versi takbaku per aspek (sumbu datar)
   lawan Delta-F1 per aspek (sumbu tegak), sepuluh titik, tiga panel, Spearman
   per model atas lima titik sebagai penunjuk arah.

Pemakaian
---------
  pip install transformers matplotlib scipy pandas
  python analisis_fertilitas.py --pasangan uji_berpasangan.csv \
         --selisih keluaran/hasil/selisih.csv --hasil-dir keluaran/hasil_fertilitas \
         --leksikon-takbaku colloquial-indonesian-lexicon.csv \
         --kata-aspek kata_kunci_aspek.txt \
         --leksikon-sentimen positif.txt negatif.txt

  Ketiga berkas leksikon bersifat pilihan; kelas yang berkasnya tidak diberikan
  dilewati dan dicatat di ringkasan. Format yang diterima: .txt (satu entri per
  baris) atau .csv/.tsv (kolom slang/kata/word/keyword bila ada, selain itu kolom
  pertama). Leksikon kolokial yang berkolom `formal` dipakai juga untuk memperluas
  leksikon sentimen dengan bentuk takbaku padanannya.

Keluaran (di --hasil-dir)
-------------------------
  fertilitas_kelas_kata.csv, fertilitas_aspek.csv, korelasi_h4.csv,
  gambar_h4_pencar.png, gambar_fertilitas_kelas_kata.png, ringkasan_h4.md
"""
import argparse
import itertools
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import rankdata

MODEL = {"indobert": "indolem/indobert-base-uncased",
         "indobertweet": "indolem/indobertweet-base-uncased"}
NAMA_TAMPIL = {"indobert": "IndoBERT", "indobertweet": "IndoBERTweet"}
REGISTER = ["FORMAL", "INFORMAL"]
ASPEK = ["keamanan_akun", "autentikasi", "privasi_data", "antarmuka", "keandalan"]
KODE_ASPEK = {"keamanan_akun": "KA", "autentikasi": "AU", "privasi_data": "PD",
              "antarmuka": "AM", "keandalan": "KD"}
METRIK = ["ACD", "ACSA", "PASANGAN"]
JUDUL_METRIK = {"ACD": "ΔF1-ACD", "ACSA": "ΔF1-ACSA (NEGATIF)", "PASANGAN": "ΔF1-pasangan"}
KELAS = ["SEMUA", "TAKBAKU", "PENANDA_ASPEK", "PENANDA_ASPEK_NETRAL", "PEMBAWA_SENTIMEN"]
NAMA_KELAS = {"SEMUA": "Seluruh kata", "TAKBAKU": "Kata takbaku",
              "PENANDA_ASPEK": "Penanda aspek", "PENANDA_ASPEK_NETRAL": "Penanda aspek netral",
              "PEMBAWA_SENTIMEN": "Pembawa sentimen"}
WARNA = {"indobert": "#2a78d6", "indobertweet": "#eb6834"}   # lolos validator palet (CVD, kontras)
PENANDA = {"indobert": "o", "indobertweet": "^"}
POLA_KATA = re.compile(r"[^\W\d_]+")
AMBANG_UNK = 1.0      # persen kemunculan kata; di atasnya tokenizer kemungkinan salah muat


# =============================================================================
# FUNGSI PENENTU ANGKA (diuji di test_fertilitas.py)
# =============================================================================
def pecah_kata(teks: str) -> list:
    """Rangkaian huruf, huruf kecil. Angka, tanda baca, emotikon dibuang."""
    return POLA_KATA.findall(str(teks).lower())


def fertilitas(daftar_kata, jumlah_token) -> tuple:
    """(jumlah kata, jumlah token, token per kata). jumlah_token: fungsi kata -> int."""
    n_kata = len(daftar_kata)
    n_token = sum(jumlah_token(w) for w in daftar_kata)
    return n_kata, n_token, (n_token / n_kata if n_kata else float("nan"))


def spearman_eksak(x, y):
    """Spearman (peringkat rata-rata untuk nilai seri) dan angka p dua arah eksak.

    Angka p = proporsi permutasi y yang |rho| >= |rho teramati| (seluruh n! permutasi,
    n <= 8). Mengembalikan (nan, nan) bila salah satu peubah konstan.
    """
    x, y = np.asarray(x, float), np.asarray(y, float)
    ok = ~(np.isnan(x) | np.isnan(y))
    x, y = x[ok], y[ok]
    if len(x) < 3 or np.ptp(x) == 0 or np.ptp(y) == 0:
        return float("nan"), float("nan")
    rx, ry = rankdata(x), rankdata(y)

    def rho(a, b):
        a, b = a - a.mean(), b - b.mean()
        return float((a * b).sum() / np.sqrt((a * a).sum() * (b * b).sum()))

    r = rho(rx, ry)
    if len(x) > 8:
        raise ValueError("angka p eksak hanya untuk n <= 8")
    perm = [rho(rx, ry[list(p)]) for p in itertools.permutations(range(len(x)))]
    p = float(np.mean([abs(v) >= abs(r) - 1e-12 for v in perm]))
    return r, p


# =============================================================================
# LEKSIKON
# =============================================================================
def baca_daftar(jalur: Path):
    """Mengembalikan (daftar entri huruf kecil, peta slang->formal atau None)."""
    if jalur.suffix.lower() == ".txt":
        # satu entri per baris; format "kata:skor" atau "kata<TAB>skor" (mis. SentiStrength-ID)
        # dibaca sebagai kata saja
        entri = [re.split(r"[:\t]", b, maxsplit=1)[0].strip().lower()
                 for b in jalur.read_text(encoding="utf-8-sig", errors="replace").splitlines()]
        return [e for e in entri if e and not e.startswith("#")], None
    with open(jalur, encoding="utf-8-sig") as f:
        judul = f.readline()
    pemisah = "\t" if jalur.suffix.lower() == ".tsv" else max([",", ";", "\t"], key=judul.count)
    df = pd.read_csv(jalur, dtype=str, keep_default_na=False, sep=pemisah, encoding="utf-8-sig")
    kol = {c.lower().strip(): c for c in df.columns}
    utama = next((kol[k] for k in ("slang", "kata", "word", "keyword", "kata_kunci", "term", "token")
                  if k in kol), df.columns[0])
    entri = [e.strip().lower() for e in df[utama] if e.strip()]
    peta = None
    if "formal" in kol:
        peta = {s.strip().lower(): f.strip().lower() for s, f in zip(df[utama], df[kol["formal"]])
                if s.strip()}
    return entri, peta


def siapkan_kelas(args):
    kelas, catatan = {}, []
    peta_takbaku = None
    if args.leksikon_takbaku:
        entri, peta_takbaku = baca_daftar(args.leksikon_takbaku)
        kelas["TAKBAKU"] = {e for e in entri if POLA_KATA.fullmatch(e)}
        catatan.append(f"Kata takbaku: {len(kelas['TAKBAKU'])} bentuk tunggal dari {args.leksikon_takbaku.name}.")
    else:
        catatan.append("Kata takbaku: DILEWATI (--leksikon-takbaku tidak diberikan).")
    if args.kata_aspek:
        entri, _ = baca_daftar(args.kata_aspek)
        tunggal = {e for e in entri if POLA_KATA.fullmatch(e)}
        frasa = len(set(entri)) - len(tunggal)
        kelas["PENANDA_ASPEK"] = tunggal
        catatan.append(f"Penanda aspek: {len(tunggal)} kata tunggal dari {args.kata_aspek.name}"
                       + (f"; {frasa} entri berupa frasa tidak dipakai" if frasa else "") + ".")
    else:
        catatan.append("Penanda aspek: DILEWATI (--kata-aspek tidak diberikan).")
    if args.leksikon_sentimen:
        dasar = set()
        for j in args.leksikon_sentimen:
            entri, _ = baca_daftar(j)
            dasar |= {e for e in entri if POLA_KATA.fullmatch(e)}
        perluasan = set()
        if peta_takbaku:
            perluasan = {s for s, f in peta_takbaku.items()
                         if POLA_KATA.fullmatch(s) and f in dasar and s not in dasar}
        kelas["PEMBAWA_SENTIMEN"] = dasar | perluasan
        catatan.append(f"Pembawa sentimen: {len(dasar)} kata dari "
                       f"{', '.join(j.name for j in args.leksikon_sentimen)}, diperluas {len(perluasan)} "
                       f"bentuk takbaku padanan" + ("" if peta_takbaku else
                                                    " (tanpa perluasan: leksikon kolokial berkolom "
                                                    "`formal` tidak diberikan)") + ".")
    else:
        catatan.append("Pembawa sentimen: DILEWATI (--leksikon-sentimen tidak diberikan).")
    if "PENANDA_ASPEK" in kelas and "PEMBAWA_SENTIMEN" in kelas:
        irisan = kelas["PENANDA_ASPEK"] & kelas["PEMBAWA_SENTIMEN"]
        kelas["PENANDA_ASPEK_NETRAL"] = kelas["PENANDA_ASPEK"] - kelas["PEMBAWA_SENTIMEN"]
        catatan.append(f"Penanda aspek netral: {len(kelas['PENANDA_ASPEK_NETRAL'])} kata, yaitu penanda aspek "
                       f"yang tidak tercatat sebagai pembawa sentimen. Irisan kedua kelas {len(irisan)} kata: "
                       + ", ".join(sorted(irisan)) + ".")
    return kelas, catatan


# =============================================================================
# PERHITUNGAN
# =============================================================================
def muat_pasangan(jalur: Path) -> pd.DataFrame:
    df = pd.read_csv(jalur, dtype=str, keep_default_na=False, encoding="utf-8-sig")
    perlu = {"id_ulasan", "register", "teks"} | {f"asp_{a}" for a in ASPEK}
    kurang = perlu - set(df.columns)
    if kurang:
        sys.exit(f"GALAT: {jalur.name} tidak berkolom {sorted(kurang)}.")
    df["register"] = df["register"].str.strip().str.upper()
    if not df.groupby("id_ulasan")["register"].apply(lambda r: sorted(r) == REGISTER).all():
        sys.exit("GALAT: tiap id_ulasan harus punya tepat satu versi FORMAL dan satu INFORMAL.")
    df["kata"] = df["teks"].map(pecah_kata)
    return df


def hitung(df, tokenizer_per_model, kelas):
    """Mengembalikan (fertilitas per kelas kata, fertilitas per aspek, persen kata [UNK] per model)."""
    baris_kelas, baris_aspek, unk = [], [], {}
    for model, tok in tokenizer_per_model.items():
        cache, ber_unk = {}, set()

        def jt(w):
            if w not in cache:
                potong = tok.tokenize(w)
                cache[w] = max(1, len(potong))
                if tok.unk_token is not None and tok.unk_token in potong:
                    ber_unk.add(w)
            return cache[w]

        for reg in REGISTER:
            sub = df[df.register == reg]
            semua = [w for ks in sub.kata for w in ks]
            for k in KELAS:
                if k != "SEMUA" and k not in kelas:
                    continue
                daftar = semua if k == "SEMUA" else [w for w in semua if w in kelas[k]]
                n_kata, n_tok, f = fertilitas(daftar, jt)
                baris_kelas.append({"model": model, "register": reg, "kelas_kata": k, "n_kata": n_kata,
                                    "n_jenis_kata": len(set(daftar)), "n_token": n_tok, "fertilitas": f})
            for a in ASPEK:
                pilih = sub[sub[f"asp_{a}"].str.strip().str.upper() != "TIDAK_ADA"]
                n_kata, n_tok, f = fertilitas([w for ks in pilih.kata for w in ks], jt)
                baris_aspek.append({"model": model, "register": reg, "aspek": a, "n_ulasan": len(pilih),
                                    "n_kata": n_kata, "n_token": n_tok, "fertilitas": f})
        semua = [w for ks in df.kata for w in ks]
        unk[model] = 100 * sum(w in ber_unk for w in semua) / max(1, len(semua))
    return pd.DataFrame(baris_kelas), pd.DataFrame(baris_aspek), unk


def ambil_selisih(jalur: Path) -> pd.DataFrame:
    s = pd.read_csv(jalur)
    s = s[(s.himpunan == "uji_berpasangan") & (s.jenis_cakupan == "ASPEK")
          & s.besaran.isin(["DELTA_F1", "DELTA_KUADRAT"]) & s.metrik.isin(METRIK)]
    if s.empty:
        sys.exit(f"GALAT: {jalur} tidak memuat Delta-F1 per aspek himpunan uji berpasangan.")
    return s[["besaran", "cakupan", "model", "metrik", "estimasi_pp"]]


def korelasi(fa, sel):
    inf = fa[fa.register == "INFORMAL"].pivot(index="aspek", columns="model", values="fertilitas").loc[ASPEK]
    d_fert = inf["indobert"] - inf["indobertweet"]
    baris = []
    for met in METRIK:
        d2 = sel[(sel.besaran == "DELTA_KUADRAT") & (sel.metrik == met)].set_index("cakupan")["estimasi_pp"]
        d2 = d2.reindex(ASPEK)
        r, p = spearman_eksak(d_fert.values, d2.values)
        baris.append({"analisis": "H4: selisih fertilitas antarmodel lawan Delta-kuadrat", "model":
                      "indobert - indobertweet", "metrik": met, "n_titik": int(d2.notna().sum()),
                      "rho_spearman": r, "p_eksak_dua_arah": p,
                      "keterangan": "tidak terdefinisi: salah satu peubah konstan" if np.isnan(r) else "",
                      "urutan_aspek_fertilitas": " > ".join(d_fert.sort_values(ascending=False).index),
                      "urutan_aspek_selisih": " > ".join(d2.sort_values(ascending=False).index)})
        for model in MODEL:
            y = sel[(sel.besaran == "DELTA_F1") & (sel.metrik == met) & (sel.model == model)]
            y = y.set_index("cakupan")["estimasi_pp"].reindex(ASPEK)
            r, p = spearman_eksak(inf[model].values, y.values)
            baris.append({"analisis": "Diagram pencar: fertilitas versi takbaku lawan Delta-F1",
                          "model": model, "metrik": met, "n_titik": int(y.notna().sum()),
                          "rho_spearman": r, "p_eksak_dua_arah": p,
                          "keterangan": "tidak terdefinisi: salah satu peubah konstan" if np.isnan(r) else "",
                          "urutan_aspek_fertilitas": " > ".join(inf[model].sort_values(ascending=False).index),
                          "urutan_aspek_selisih": " > ".join(y.sort_values(ascending=False).index)})
    return pd.DataFrame(baris), d_fert


# =============================================================================
# GAMBAR
# =============================================================================
def koma(x, _=None, d=2):
    return f"{x:.{d}f}".replace(".", ",")


def gaya_dasar():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib import font_manager
    serif = "Times New Roman" if any("Times New Roman" in f.name for f in font_manager.fontManager.ttflist) \
        else "DejaVu Serif"
    plt.rcParams.update({"font.family": "serif", "font.serif": [serif], "font.size": 10,
                         "axes.edgecolor": "#52514e", "axes.linewidth": 0.8,
                         "axes.spines.top": False, "axes.spines.right": False,
                         "xtick.color": "#52514e", "ytick.color": "#52514e",
                         "axes.labelcolor": "#0b0b0b", "axes.titleweight": "bold",
                         "axes.titlesize": 11, "legend.frameon": False})
    return plt


def kelompok_label(titik, rentang_x, rentang_y, ambang=0.04):
    """Menggabungkan label titik yang berdekatan (jarak ternormalkan < ambang) menjadi satu label.

    titik: daftar (kode, x, y). Mengembalikan daftar (label gabungan, x, y) pada titik pertama tiap kelompok.
    """
    sisa, hasil = list(titik), []
    while sisa:
        kode, x0, y0 = sisa.pop(0)
        anggota = [kode]
        for t in list(sisa):
            if np.hypot((t[1] - x0) / rentang_x, (t[2] - y0) / rentang_y) < ambang:
                anggota.append(t[0])
                sisa.remove(t)
        hasil.append(("/".join(anggota), x0, y0))
    return hasil


def hindari_tumpang(fig, annots, langkah=9, batas=8):
    """Menggeser label yang bertabrakan (kotak teks beririsan) naik-turun sampai bebas."""
    fig.canvas.draw()
    pengenal = fig.canvas.get_renderer()
    terpasang = []
    for an in annots:
        dx, dy = an.xyann
        for i in range(batas):
            kotak = an.get_window_extent(pengenal).expanded(1.05, 1.15)
            if not any(kotak.overlaps(k) for k in terpasang):
                break
            geser = langkah * (i // 2 + 1) * (1 if i % 2 == 0 else -1)
            an.xyann = (dx, dy + geser)
        terpasang.append(an.get_window_extent(pengenal))


def gambar_pencar(fa, sel, kor, jalur: Path):
    plt = gaya_dasar()
    from matplotlib import patheffects
    from matplotlib.ticker import FuncFormatter
    inf = fa[fa.register == "INFORMAL"].pivot(index="aspek", columns="model", values="fertilitas")
    ys = sel[sel.besaran == "DELTA_F1"]["estimasi_pp"]
    lo, hi = float(ys.min()), float(ys.max())
    pad = max(1.0, 0.12 * (hi - lo))
    fig, axes = plt.subplots(1, 3, figsize=(12, 4.6), sharey=True, constrained_layout=True)
    xs_semua = inf[list(MODEL)].values.ravel()
    rx = max(np.ptp(xs_semua), 1e-6) * 1.2
    ry = (hi - lo) + 2 * pad
    for ax, met in zip(axes, METRIK):
        annots, teks_rho = [], []
        ax.axhline(0, color="#b5b4ad", linewidth=0.8, zorder=0)
        ax.grid(axis="y", color="#e6e5e0", linewidth=0.6, zorder=0)
        for model in MODEL:
            y = sel[(sel.besaran == "DELTA_F1") & (sel.metrik == met) & (sel.model == model)]
            y = y.set_index("cakupan")["estimasi_pp"].reindex(ASPEK)
            x = inf[model].reindex(ASPEK)
            r = kor[(kor.analisis.str.startswith("Diagram")) & (kor.model == model) & (kor.metrik == met)]
            rho = r.rho_spearman.iloc[0]
            teks_rho.append(f"{NAMA_TAMPIL[model]} ρ = {'tak terdefinisi' if np.isnan(rho) else koma(rho)}")
            ax.scatter(x, y, s=55, marker=PENANDA[model], color=WARNA[model], edgecolor="white",
                       linewidth=1.5, zorder=3, label=NAMA_TAMPIL[model])
            if np.ptp(x.values) > 0 and np.ptp(y.values) > 0:
                k, c = np.polyfit(x.values, y.values, 1)
                xx = np.linspace(x.min(), x.max(), 20)
                ax.plot(xx, k * xx + c, color=WARNA[model], linewidth=1.5,
                        linestyle="-" if model == "indobert" else "--", zorder=2)
            for teks, tx, ty in kelompok_label([(KODE_ASPEK[a], x[a], y[a]) for a in ASPEK], rx, ry):
                annots.append(ax.annotate(teks, (tx, ty), textcoords="offset points",
                                          xytext=(6, 4 if model == "indobert" else -11), fontsize=8,
                                          color="#52514e", zorder=2.5,
                                          path_effects=[patheffects.withStroke(linewidth=3, foreground="white")]))
        ax.set_title(f"{JUDUL_METRIK[met]}\n", loc="center")
        ax.text(0.5, 1.02, "   ·   ".join(teks_rho), transform=ax.transAxes, ha="center", va="bottom",
                fontsize=8.5, color="#52514e")
        ax._annots_label = annots
        ax.set_xlabel("Fertilitas versi takbaku (token per kata)")
        ax.xaxis.set_major_formatter(FuncFormatter(koma))
        ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:g}".replace(".", ",")))
        ax.set_ylim(lo - pad, hi + pad)
    axes[0].set_ylabel("ΔF1 (poin persen)")
    pegangan, label = axes[0].get_legend_handles_labels()
    fig.legend(pegangan, label, loc="outside lower center", ncol=2, fontsize=9,
               title="Garis: regresi per model atas lima aspek. ρ: Spearman atas lima titik (penunjuk arah)",
               title_fontsize=8.5)
    for ax in axes:
        hindari_tumpang(fig, ax._annots_label)
    fig.savefig(jalur, dpi=200)
    plt.close(fig)


def gambar_batang(fk, jalur: Path):
    plt = gaya_dasar()
    from matplotlib.ticker import FuncFormatter
    kelas_ada = [k for k in KELAS if k in set(fk.kelas_kata)]
    # Dua panel bersusun tegak: pada lebar halaman tesis (14 cm) huruf tetap terbaca.
    fig, axes = plt.subplots(2, 1, figsize=(7.2, 7.4), sharey=True, constrained_layout=True)
    lebar = 0.36
    puncak = fk.fertilitas.max()
    for ax, reg in zip(axes, REGISTER):
        ax.grid(axis="y", color="#e6e5e0", linewidth=0.6, zorder=0)
        for i, model in enumerate(MODEL):
            v = (fk[(fk.register == reg) & (fk.model == model)].set_index("kelas_kata")
                 .reindex(kelas_ada)["fertilitas"])
            xs = np.arange(len(kelas_ada)) + (i - 0.5) * (lebar + 0.02)
            bar = ax.bar(xs, v.values, width=lebar, color=WARNA[model], edgecolor="white", linewidth=2,
                         hatch=None if model == "indobert" else "///", label=NAMA_TAMPIL[model], zorder=2)
            for b, val in zip(bar, v.values):
                if not np.isnan(val):
                    ax.text(b.get_x() + b.get_width() / 2, val + 0.02 * puncak, koma(val), ha="center",
                            va="bottom", fontsize=8, color="#0b0b0b")
        for j, k in enumerate(kelas_ada):
            n = fk[(fk.register == reg) & (fk.kelas_kata == k)]["n_kata"]
            if len(n) and int(n.iloc[0]) == 0:
                ax.text(j, 0.04 * puncak, "tidak\nmuncul", ha="center", va="bottom", fontsize=8,
                        color="#52514e", style="italic")
        ax.set_xticks(np.arange(len(kelas_ada)))
        ax.set_xticklabels([NAMA_KELAS[k].replace(" ", "\n") for k in kelas_ada])
        ax.set_title(f"Versi {'baku' if reg == 'FORMAL' else 'takbaku'} ({reg})")
        ax.set_ylim(0, puncak * 1.15)
        ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: koma(v, d=1)))
    for ax in axes:
        ax.set_ylabel("Fertilitas (token per kata)")
    axes[0].legend(loc="upper right", fontsize=9, ncol=2)
    fig.savefig(jalur, dpi=200)
    plt.close(fig)


# =============================================================================
# RINGKASAN
# =============================================================================
def a(x, d=3):
    return "-" if x is None or (isinstance(x, float) and np.isnan(x)) else f"{x:.{d}f}".replace(".", ",")


def tulis_ringkasan(fk, fa, kor, d_fert, catatan, nama_hf, unk, jalur: Path):
    L = ["# Analisis fertilitas tokenizer dan H4", "",
         "Himpunan uji berpasangan. Fertilitas = jumlah token subkata dibagi jumlah kata (rangkaian huruf). "
         f"Tokenizer: {', '.join(f'{NAMA_TAMPIL[m]} = `{h}`' for m, h in nama_hf.items())}.", ""]
    L += ["Kemunculan kata yang tokenisasinya memuat [UNK]: "
          + ", ".join(f"{NAMA_TAMPIL[m]} {a(v, 2)}%" for m, v in unk.items())
          + (". PERINGATAN: di atas ambang; periksa tokenizer yang dimuat." if max(unk.values()) > AMBANG_UNK
             else "."), ""]
    L += ["Sumber kelas kata:", ""] + [f"- {c}" for c in catatan] + [""]

    L += ["## Fertilitas per kelas kata", "",
          "| Kelas kata | Register | IndoBERT | IndoBERTweet | Selisih (IndoBERT - IndoBERTweet) | Kemunculan kata |",
          "|---|---|---|---|---|---|"]
    for k in KELAS:
        for reg in REGISTER:
            s = fk[(fk.kelas_kata == k) & (fk.register == reg)].set_index("model")
            if s.empty:
                continue
            L.append(f"| {NAMA_KELAS[k]} | {reg} | {a(s.loc['indobert', 'fertilitas'])} | "
                     f"{a(s.loc['indobertweet', 'fertilitas'])} | "
                     f"{a(s.loc['indobert', 'fertilitas'] - s.loc['indobertweet', 'fertilitas'])} | "
                     f"{int(s.loc['indobert', 'n_kata'])} |")
    L += ["", "Bila selisih antarmodel terpusat pada pembawa sentimen dan tidak pada penanda aspek, H3 dan H4 "
          "menunjuk ke penjelasan yang sama (Subbab 3.5.6). Karena sebagian kata kunci aspek juga kata "
          "evaluatif, perbandingan yang bersih adalah pembawa sentimen lawan penanda aspek netral.", ""]

    L += ["## Fertilitas per aspek (ulasan yang aspeknya hadir)", "",
          "| Aspek | Kode | Ulasan | IndoBERT baku | IndoBERT takbaku | IndoBERTweet baku | IndoBERTweet takbaku | "
          "Selisih antarmodel (takbaku) |", "|---|---|---|---|---|---|---|---|"]
    for asp in ASPEK:
        s = fa[fa.aspek == asp].set_index(["model", "register"])
        L.append(f"| {asp} | {KODE_ASPEK[asp]} | {int(s.loc[('indobert', 'INFORMAL'), 'n_ulasan'])} | "
                 f"{a(s.loc[('indobert', 'FORMAL'), 'fertilitas'])} | {a(s.loc[('indobert', 'INFORMAL'), 'fertilitas'])} | "
                 f"{a(s.loc[('indobertweet', 'FORMAL'), 'fertilitas'])} | "
                 f"{a(s.loc[('indobertweet', 'INFORMAL'), 'fertilitas'])} | {a(d_fert[asp])} |")
    L.append("")

    L += ["## Korelasi Spearman (EKSPLORATORI, di luar koreksi Holm)", "",
          "Lima titik per korelasi; angka p eksak dari 120 permutasi. Dengan lima titik, angka p dua arah "
          "terkecil yang mungkin adalah 0,017 (urutan sempurna), sehingga koefisien diperlakukan sebagai "
          "penunjuk arah, bukan bukti sebab-akibat (Subbab 3.5.5 dan 3.5.6).", "",
          "| Analisis | Model | Metrik | rho | p eksak | Keterangan |", "|---|---|---|---|---|---|"]
    for _, r in kor.iterrows():
        L.append(f"| {r.analisis} | {r.model} | {r.metrik} | {a(r.rho_spearman, 2)} | "
                 f"{a(r.p_eksak_dua_arah)} | {r.keterangan} |")
    L += ["", "### Urutan aspek (H4)", "",
          "| Metrik | Urutan menurut selisih fertilitas | Urutan menurut Delta-kuadrat |", "|---|---|---|"]
    for _, r in kor[kor.analisis.str.startswith("H4")].iterrows():
        L.append(f"| {r.metrik} | {r.urutan_aspek_fertilitas} | {r.urutan_aspek_selisih} |")
    L += ["", "Gambar: `gambar_h4_pencar.png` (tiga panel, sumbu tegak disamakan) dan "
          "`gambar_fertilitas_kelas_kata.png` (diagram batang berkelompok). Kode aspek: "
          + ", ".join(f"{v} = {k}" for k, v in KODE_ASPEK.items()) + ".", ""]
    jalur.write_text("\n".join(L), encoding="utf-8")


# =============================================================================
# UTAMA
# =============================================================================
def main():
    ap = argparse.ArgumentParser(description="Analisis fertilitas tokenizer dan H4 (Subbab 3.5.6).")
    ap.add_argument("--pasangan", required=True, type=Path)
    ap.add_argument("--selisih", required=True, type=Path, help="selisih.csv hasil UTAMA evaluasi_statistik.py")
    ap.add_argument("--hasil-dir", required=True, type=Path)
    ap.add_argument("--leksikon-takbaku", type=Path, default=None)
    ap.add_argument("--kata-aspek", type=Path, default=None)
    ap.add_argument("--leksikon-sentimen", type=Path, nargs="+", default=None)
    ap.add_argument("--model-indobert", default=MODEL["indobert"])
    ap.add_argument("--model-indobertweet", default=MODEL["indobertweet"])
    args = ap.parse_args()
    for j in [args.pasangan, args.selisih, args.leksikon_takbaku, args.kata_aspek, *(args.leksikon_sentimen or [])]:
        if j is not None and not j.exists():
            sys.exit(f"GALAT: berkas tidak ditemukan: {j}")

    from transformers import AutoTokenizer
    nama_hf = {"indobert": args.model_indobert, "indobertweet": args.model_indobertweet}
    tok = {m: AutoTokenizer.from_pretrained(h) for m, h in nama_hf.items()}

    df = muat_pasangan(args.pasangan)
    kelas, catatan = siapkan_kelas(args)
    fk, fa, unk = hitung(df, tok, kelas)
    for m, v in unk.items():
        if v > AMBANG_UNK:
            print(f"PERINGATAN: {v:.1f}% kemunculan kata pada {m} memuat [UNK]. Periksa bahwa tokenizer "
                  f"yang dimuat benar; fertilitas pada kata [UNK] tercatat terlalu rendah.")
    sel = ambil_selisih(args.selisih)
    kor, d_fert = korelasi(fa, sel)

    args.hasil_dir.mkdir(parents=True, exist_ok=True)
    fk.to_csv(args.hasil_dir / "fertilitas_kelas_kata.csv", index=False, float_format="%.4f")
    fa.to_csv(args.hasil_dir / "fertilitas_aspek.csv", index=False, float_format="%.4f")
    kor.to_csv(args.hasil_dir / "korelasi_h4.csv", index=False, float_format="%.4f")
    gambar_pencar(fa, sel, kor, args.hasil_dir / "gambar_h4_pencar.png")
    gambar_batang(fk, args.hasil_dir / "gambar_fertilitas_kelas_kata.png")
    tulis_ringkasan(fk, fa, kor, d_fert, catatan, nama_hf, unk, args.hasil_dir / "ringkasan_h4.md")
    for c in catatan:
        print(c)
    print(f"Selesai. Lihat {args.hasil_dir / 'ringkasan_h4.md'}")


if __name__ == "__main__":
    main()
