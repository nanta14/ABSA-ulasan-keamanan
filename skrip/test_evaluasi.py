# -*- coding: utf-8 -*-
"""
test_evaluasi.py -- pengujian unit atas fungsi penentu angka di evaluasi_statistik.py.
Jalankan:  python -m pytest -q test_evaluasi.py
Setiap nilai harapan dihitung dengan tangan dan ditulis di komentar.
Kode kelas: 0 = TIDAK_ADA, 1 = NEGATIF, 2 = POSITIF.
"""
import numpy as np
import pandas as pd
import pytest

import evaluasi_statistik as ev

A, M, R = len(ev.ASPEK), len(ev.MODEL), len(ev.REGISTER)


def jumlah(trio):
    return tuple(int(x.sum()) for x in trio)


# ----------------------------------------------------------------------------- metrik
def test_acd_hitungan_tangan():
    emas = np.array([[1, 0, 2, 0, 0]])
    pred = np.array([[1, 1, 0, 0, 0]])
    # aspek-0 terdeteksi (TP), aspek-1 muncul padahal tidak ada (FP), aspek-2 luput (FN)
    assert jumlah(ev.indikator(emas, pred, pred, "ACD")) == (1, 1, 1)
    assert ev.f1_dari(1, 1, 1) == pytest.approx(0.5)          # 2 / (2 + 1 + 1)


def test_acd_mengabaikan_polaritas():
    emas, pred = np.array([[1]]), np.array([[2]])             # aspek ketemu, polaritas keliru
    assert jumlah(ev.indikator(emas, pred, pred, "ACD")) == (1, 0, 0)


def test_pasangan_polaritas_keliru_dihitung_fp_dan_fn():
    emas, pred = np.array([[1]]), np.array([[2]])
    assert jumlah(ev.indikator(emas, pred, pred, "PASANGAN")) == (0, 1, 1)


def test_pasangan_benar_negatif_tidak_dihitung():
    emas, pred = np.array([[0, 0]]), np.array([[0, 0]])
    assert jumlah(ev.indikator(emas, pred, pred, "PASANGAN")) == (0, 0, 0)
    assert np.isnan(ev.f1_dari(0, 0, 0))                      # penyebut nol -> NaN, bukan 0


def test_acsa_hanya_butir_emas_ada_mode_terbatas():
    emas = np.array([[0, 1, 1, 2]])
    pred = np.array([[1, 0, 1, 2]])       # keputusan tiga kelas
    pol = np.array([[1, 1, 2, 1]])        # keputusan polaritas terbatas
    # butir-0 emas TIDAK_ADA -> di luar hitungan walau model memprediksi NEGATIF
    # butir-1 emas NEG, pol NEG -> TP (kekeliruan deteksi tidak ikut terhitung)
    # butir-2 emas NEG, pol POS -> FN ; butir-3 emas POS, pol NEG -> FP
    assert jumlah(ev.indikator(emas, pred, pol, "ACSA", "terbatas")) == (1, 1, 1)
    # kelas POSITIF: butir-3 luput (FN), butir-2 salah masuk (FP), tidak ada TP
    assert jumlah(ev.indikator(emas, pred, pol, "ACSA_POS", "terbatas")) == (0, 1, 1)


def test_acsa_mode_penuh_menghitung_luput_deteksi():
    emas = np.array([[0, 1, 1, 2]])
    pred = np.array([[1, 0, 1, 2]])
    pol = np.array([[1, 1, 2, 1]])
    # butir-1 diprediksi TIDAK_ADA -> FN ; butir-2 -> TP ; butir-3 benar POS -> bukan FP
    assert jumlah(ev.indikator(emas, pred, pol, "ACSA", "penuh")) == (1, 0, 1)


def test_galat_biner_sama_dengan_fp_plus_fn():
    """Dasar pemakaian McNemar untuk ACSA: butir salah = FP + FN kelas NEGATIF."""
    rng = np.random.default_rng(0)
    emas = rng.integers(0, 3, (200, A))
    pol = rng.integers(1, 3, (200, A))
    tp, fp, fn = ev.indikator(emas, emas, pol, "ACSA")
    benar, sah = ev.benar_per_butir(emas, emas, pol, "ACSA")
    assert int((sah & ~benar).sum()) == int(fp.sum() + fn.sum())


# ----------------------------------------------------------------------------- uji
def test_mcnemar_eksak():
    assert ev.mcnemar_eksak(8, 1, "dua") == pytest.approx(20 / 512)      # 2 * (1 + 9) / 2^9
    assert ev.mcnemar_eksak(8, 1, "lebih") == pytest.approx(10 / 512)    # P(X >= 8 | n = 9)
    assert ev.mcnemar_eksak(1, 8, "lebih") == pytest.approx(511 / 512)   # arah berlawanan
    assert ev.mcnemar_eksak(0, 0) == 1.0                                 # tanpa pasangan tak selaras
    assert ev.mcnemar_eksak(5, 5, "dua") == 1.0


def test_holm():
    # urut: 0,01 x3 = 0,03 ; 0,03 x2 = 0,06 ; 0,04 x1 = 0,04 -> dinaikkan ke 0,06 (monoton)
    assert ev.holm([0.01, 0.04, 0.03]) == pytest.approx([0.03, 0.06, 0.06])
    assert ev.holm([0.5]) == pytest.approx([0.5])
    assert ev.holm([0.6, 0.7]).max() <= 1.0


def test_p_bootstrap():
    assert ev.p_bootstrap(np.zeros(999), "dua") == 1.0
    assert ev.p_bootstrap(np.zeros(999), "lebih") == 1.0
    assert ev.p_bootstrap(np.ones(999), "lebih") == pytest.approx(1 / 1000)
    assert ev.p_bootstrap(np.ones(999), "dua") == pytest.approx(2 / 1000)
    assert ev.p_bootstrap(-np.ones(999), "lebih") == 1.0                 # arah berlawanan


def test_wilson_nilai_pustaka():
    # 8 dari 10, selang skor Wilson 95%: 0,4902 s.d. 0,9433 (Newcombe 1998, metode 3)
    p, bw, at = ev.wilson(8, 10)
    assert p == pytest.approx(80.0)
    assert bw == pytest.approx(49.02, abs=0.01) and at == pytest.approx(94.33, abs=0.01)
    assert all(np.isnan(ev.wilson(0, 0)))
    assert ev.wilson(0, 20)[1] == 0.0                       # batas bawah tidak negatif


# ----------------------------------------------------------------------------- rancangan
def data_tiruan(n=400, galat_informal=(0.30, 0.0), benih=1):
    """Kedua model sempurna pada FORMAL; model ke-m keliru pada INFORMAL sebesar galat[m]."""
    rng = np.random.default_rng(benih)
    emas = rng.choice(3, size=(n, A), p=[0.6, 0.3, 0.1])
    pred = np.broadcast_to(emas, (M, R, n, A)).copy()
    for m, g in enumerate(galat_informal):
        rusak = rng.random((n, A)) < g
        pred[m, 1] = np.where(rusak, (emas + 1) % 3, emas)
    pol = np.where(pred == 0, 1, pred)
    hadir = np.ones((R, n), dtype=bool)
    return emas, pred, pol, hadir


def test_tanda_delta_dan_delta_kuadrat():
    emas, pred, pol, hadir = data_tiruan()
    t = ev.turunan(ev.hitung_cacah(emas, pred, pol, hadir).sum(axis=0))
    k = ev.METRIK.index("PASANGAN")
    assert t["f1"][0, 0, 0, k] == pytest.approx(100.0)        # indobert, FORMAL
    assert t["delta"][0, 0, k] > 10                           # turun pada INFORMAL -> positif
    assert t["delta"][1, 0, k] == pytest.approx(0.0)          # indobertweet tidak turun
    assert t["delta2"][0, k] == pytest.approx(t["delta"][0, 0, k])   # indobert lebih rapuh -> positif


def test_bootstrap_menarik_pasangan_utuh():
    """Bila prediksi kedua versi identik, Delta-F1 harus tepat nol pada SETIAP penarikan.
    Ini gagal bila kedua register ditarik ulang secara terpisah."""
    emas, pred, pol, hadir = data_tiruan(galat_informal=(0.0, 0.0))
    rusak = np.random.default_rng(3).random(emas.shape) < 0.25
    pred[:, :] = np.where(rusak, (emas + 1) % 3, emas)        # galat sama pada kedua register
    pol = np.where(pred == 0, 1, pred)
    ulang = ev.bootstrap_kluster(ev.hitung_cacah(emas, pred, pol, hadir), 500,
                                 np.random.default_rng(0))
    assert np.nanmax(np.abs(ulang["delta"])) == pytest.approx(0.0, abs=1e-9)
    assert ev.p_bootstrap(ulang["delta2"][:, 0, 0], "dua") == 1.0


def test_bootstrap_mendeteksi_selisih_nyata():
    emas, pred, pol, hadir = data_tiruan()
    ulang = ev.bootstrap_kluster(ev.hitung_cacah(emas, pred, pol, hadir), 2000,
                                 np.random.default_rng(0))
    k = ev.METRIK.index("PASANGAN")
    assert ev.p_bootstrap(ulang["delta2"][:, 0, k], "dua") < 0.01
    bawah, atas = ev.selang(ulang["delta2"][:, 0, k])
    assert bawah > 0 and atas > bawah


def test_cacah_gabungan_sama_dengan_jumlah_per_aspek():
    emas, pred, pol, hadir = data_tiruan(n=100)
    C = ev.hitung_cacah(emas, pred, pol, hadir).sum(axis=0)   # [m, r, s, k, 3]
    nama = [c[0] for c in ev.CAKUPAN]
    per_aspek = sum(C[:, :, nama.index(a)] for a in ev.ASPEK)
    assert np.array_equal(C[:, :, nama.index("SEMUA")], per_aspek)
    kelompok = C[:, :, nama.index("KEAMANAN")] + C[:, :, nama.index("KONTROL")]
    assert np.array_equal(C[:, :, nama.index("SEMUA")], kelompok)


# ----------------------------------------------------------------------------- fitur tambahan
def test_saring_terpotong_membuang_pasangan_utuh():
    emas, pred, pol, hadir = data_tiruan(n=10)
    terpotong = np.zeros((M, R, 10), dtype=bool)
    terpotong[0, 1, 2] = True        # indobert, INFORMAL, ulasan 2
    terpotong[1, 0, 7] = True        # indobertweet, FORMAL, ulasan 7
    S = {"ids": [f"u{i}" for i in range(10)], "emas": emas, "pred": pred, "pol": pol,
         "hadir": hadir, "terpotong": terpotong, "ada_register": True}
    S2, n_buang = ev.saring_terpotong(S)
    assert n_buang == 2
    assert S2["ids"] == [f"u{i}" for i in range(10) if i not in (2, 7)]
    assert S2["emas"].shape == (8, A) and S2["pred"].shape == (M, R, 8, A)
    assert S2["hadir"].shape == (R, 8) and not S2["terpotong"].any()
    assert np.array_equal(S2["emas"], np.delete(emas, [2, 7], axis=0))


def test_kekeliruan_hitungan_tangan():
    # satu ulasan, lima aspek; hanya model pertama, register FORMAL yang diperiksa
    emas = np.array([[1, 1, 0, 2, 0]])
    pred = np.zeros((M, R, 1, A), dtype=int)
    pred[0, 0, 0] = [1, 0, 1, 1, 0]
    # aspek-0 NEG -> NEG tepat ; aspek-1 NEG -> TIDAK_ADA luput ; aspek-2 tidak ada -> NEG palsu ;
    # aspek-3 POS -> NEG terbalik ; aspek-4 benar TIDAK_ADA
    S = {"emas": emas, "pred": pred, "hadir": np.ones((R, 1), dtype=bool), "ada_register": True}
    baris = pd.DataFrame(ev.kekeliruan("uji", S))
    r = baris[(baris.cakupan == "SEMUA") & (baris.model == ev.MODEL[0])
              & (baris.register == "FORMAL")].iloc[0]
    assert (r.emas_ada, r.emas_negatif, r.luput, r.muncul_palsu, r.polaritas_terbalik) == (3, 2, 1, 1, 1)
    assert r.recall_negatif_persen == pytest.approx(50.0)      # 1 dari 2 emas NEGATIF tertangkap
    assert r.recall_deteksi_persen == pytest.approx(200 / 3)   # 2 dari 3 aspek hadir terdeteksi


# ----------------------------------------------------------------------------- pemuatan
def ke_tabel_panjang(model, emas, pred, pol, ids, register):
    baris = []
    for r, reg in enumerate(register):
        for i, u in enumerate(ids):
            for j, asp in enumerate(ev.ASPEK):
                baris.append({"model": model, "id_ulasan": u, "register": reg, "aspek": asp,
                              "emas": ev.LABEL[emas[i, j]], "prediksi": ev.LABEL[pred[r, i, j]],
                              "prediksi_polaritas": ev.LABEL[pol[r, i, j]], "terpotong": "0"})
    return pd.DataFrame(baris).sample(frac=1, random_state=0)  # urutan baris tidak boleh berpengaruh


def test_susun_bolak_balik_dan_penolakan_label_tak_identik():
    emas, pred, pol, _ = data_tiruan(n=30)
    ids = [f"u{i:03d}" for i in range(30)]
    tabel = {m: ke_tabel_panjang(m, emas, pred[mi], pol[mi], ids, ev.REGISTER)
             for mi, m in enumerate(ev.MODEL)}
    S = ev.susun(tabel, berpasangan=True)
    assert np.array_equal(S["emas"], emas)
    assert np.array_equal(S["pred"], pred) and np.array_equal(S["pol"], pol)
    assert S["hadir"].all()

    rusak = tabel[ev.MODEL[0]].copy()
    baris = rusak.index[(rusak.register == "FORMAL") & (rusak.emas == "NEGATIF")][0]
    rusak.loc[baris, "emas"] = "POSITIF"                       # label versi baku digeser
    with pytest.raises(ev.GalatData):
        ev.susun({ev.MODEL[0]: rusak, ev.MODEL[1]: tabel[ev.MODEL[1]]}, berpasangan=True)
