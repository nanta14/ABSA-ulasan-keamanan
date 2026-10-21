# -*- coding: utf-8 -*-
"""Uji unit aturan pencarian hiperparameter (tanpa melatih; tidak memerlukan torch).

  python -m pytest test_pencarian.py -q
"""
import json

import numpy as np
import pandas as pd
import pytest

import cari_hiperparameter as ch
from latih_prediksi import TABEL_12


def tabel(baris):
    return pd.DataFrame(baris, columns=["laju_belajar", "ukuran_tumpukan", "epoch", "f1_pasangan_rerata"])


def test_kisi_delapan_belas_kombinasi_dan_tabel_12_paling_dahulu():
    k = ch.daftar_kombinasi()
    assert len(k) == 18 and len(set(k)) == 18
    assert k[0] == TABEL_12 == (2e-5, 16, 4)
    assert {x[0] for x in k} == {2e-5, 3e-5, 5e-5}
    assert {x[1] for x in k} == {16, 32} and {x[2] for x in k} == {2, 3, 4}


def test_pilih_skor_tertinggi():
    t = tabel([(2e-5, 16, 4, 70.0), (3e-5, 16, 3, 71.5), (5e-5, 32, 2, 71.4)])
    assert ch.pilih(t) == 1


def test_seri_diputus_epoch_lalu_laju_lalu_tumpukan():
    # selisih 0,005 < 0,01 -> seri; epoch paling sedikit menang walau skornya sedikit lebih rendah
    t = tabel([(2e-5, 16, 4, 71.500), (5e-5, 32, 3, 71.495), (3e-5, 32, 3, 71.495),
               (3e-5, 16, 3, 71.495)])
    assert ch.pilih(t) == 3
    # selisih 0,02 >= 0,01 -> bukan seri; skor tertinggi tetap menang walau epoch lebih banyak
    t = tabel([(2e-5, 16, 4, 71.50), (2e-5, 16, 2, 71.48)])
    assert ch.pilih(t) == 0


def test_urutkan_terpilih_peringkat_satu_dan_penanda_tabel_12():
    t = ch.urutkan(tabel([(2e-5, 16, 4, 70.0), (3e-5, 16, 4, 72.0), (3e-5, 16, 3, 71.995)]))
    assert t.peringkat.tolist() == [1, 2, 3]
    assert (t.loc[0, "epoch"], bool(t.loc[0, "terpilih"])) == (3, True)      # seri -> epoch 3
    assert t.terpilih.sum() == 1
    assert t[t.tabel_12].epoch.tolist() == [4] and t[t.tabel_12].peringkat.tolist() == [3]


def test_f1_pasangan_polaritas_keliru_dihitung_fp_dan_fn():
    #            TIDAK_ADA=0, NEGATIF=1, POSITIF=2
    emas = np.array([[1, 0, 0, 2, 0],
                     [0, 1, 0, 0, 0]])
    pred = np.array([[1, 0, 0, 1, 1],      # benar | polaritas keliru (FP+FN) | deteksi palsu (FP)
                     [0, 0, 0, 0, 0]])     # terlewat (FN)
    c = ch.cacah_per_ulasan(emas, pred)
    assert c["pasangan"].tolist() == [[1, 2, 1], [0, 0, 1]]
    assert c["acd"].tolist() == [[2, 1, 0], [0, 0, 1]]
    assert ch.f1_mikro(c["pasangan"]) == pytest.approx(100 * 2 * 1 / (2 * 1 + 2 + 2))
    assert ch.f1_mikro(c["acd"]) == pytest.approx(100 * 2 * 2 / (2 * 2 + 1 + 1))


def test_bootstrap_selisih_nol_bila_identik_dan_bertanda_benar():
    rng = np.random.default_rng(0)
    dasar = {m: rng.integers(0, 3, size=(200, 3)) for m in ("indobert", "indobertweet")}
    s = ch.bootstrap_selisih(dasar, dasar, 500, 42)
    assert s["selisih"] == 0 and s["bawah"] == 0 and s["atas"] == 0
    lebih = {m: c + np.array([1, 0, 0]) for m, c in dasar.items()}          # TP bertambah
    s = ch.bootstrap_selisih(lebih, dasar, 500, 42)
    assert s["selisih"] > 0 and s["bawah"] > 0 and s["bawah"] < s["selisih"] < s["atas"]
    assert ch.bootstrap_selisih(lebih, dasar, 500, 42) == s                  # berbenih tetap


def test_pemeriksaan_acuan_cocok_setara_beda(tmp_path):
    riw = [{"epoch": e, "rugi_latih": 0.5 / e, "rugi_pengembangan": 0.4 / e,
            "f1_acd_pengembangan": 60.0 + e, "f1_pasangan_pengembangan": 58.0 + e} for e in (1, 2, 3, 4)]
    data = {n: {"sha256": "x"} for n in ch.HIMPUNAN}
    for m in ch.MODEL:
        (tmp_path / f"catatan_lari_{m}_benih42.json").write_text(json.dumps({
            "hiperparameter": {"laju_belajar": 2e-5, "ukuran_tumpukan": 16, "epoch": 4},
            "berkas": {n: {"sha256": "x"} for n in ch.HIMPUNAN}, "riwayat": riw}))
    derau = [{**e, "rugi_latih": e["rugi_latih"] + 1e-5} for e in riw]
    geser = [{**e, "f1_pasangan_pengembangan": e["f1_pasangan_pengembangan"] + 0.34} for e in riw]
    for kini, harapan in ((riw, "COCOK"), (derau, "SETARA"), (geser, "BEDA")):
        hasil = ch.periksa_acuan(tmp_path, {m: {"riwayat": kini} for m in ch.MODEL}, data)
        assert {r["status"] for r in hasil.values()} == {harapan}
    assert hasil["indobert"]["selisih_maks_f1_pasangan"] == pytest.approx(0.34)
    (tmp_path / "catatan_lari_indobert_benih42.json").unlink()
    hasil = ch.periksa_acuan(tmp_path, {m: {"riwayat": riw} for m in ch.MODEL}, data)
    assert hasil["indobert"]["status"] == "TIDAK_ADA" and hasil["indobertweet"]["status"] == "COCOK"
