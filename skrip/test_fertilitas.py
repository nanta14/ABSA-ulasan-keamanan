# -*- coding: utf-8 -*-
"""
test_fertilitas.py -- pengujian unit atas fungsi penentu angka di analisis_fertilitas.py.
Jalankan:  python -m pytest -q test_fertilitas.py
"""
import itertools

import numpy as np
import pytest
from scipy.stats import spearmanr

import analisis_fertilitas as af


def test_pecah_kata_hanya_rangkaian_huruf():
    # angka, tanda baca, emotikon dibuang; huruf kecil; kata berulang dengan angka terpisah
    assert af.pecah_kata("Gk bisa LOGIN!!! 3x, otp2 😡 kecewa-banget") == \
        ["gk", "bisa", "login", "x", "otp", "kecewa", "banget"]
    assert af.pecah_kata("123 ... 😡") == []


def test_fertilitas_hitungan_tangan():
    panjang = {"aplikasi": 1, "ngelag": 3, "parah": 2}
    n_kata, n_token, f = af.fertilitas(["aplikasi", "ngelag", "parah", "ngelag"], panjang.get)
    assert (n_kata, n_token) == (4, 9) and f == pytest.approx(2.25)    # 1 + 3 + 2 + 3 = 9 token
    assert np.isnan(af.fertilitas([], panjang.get)[2])                 # penyebut nol -> NaN


def test_spearman_eksak_sama_dengan_scipy_dan_tabel():
    x, y = [1.2, 1.5, 1.1, 1.9, 1.4], [3.0, 1.0, 2.0, 5.0, 4.0]
    r, p = af.spearman_eksak(x, y)
    assert r == pytest.approx(spearmanr(x, y).statistic)
    # urutan sempurna, lima titik: p dua arah eksak = 2/120
    r, p = af.spearman_eksak([1, 2, 3, 4, 5], [2, 4, 6, 8, 10])
    assert r == pytest.approx(1.0) and p == pytest.approx(2 / 120)
    # rho = 0,5 dengan n = 5: 54 dari 120 permutasi |rho| >= 0,5
    r, p = af.spearman_eksak([1, 2, 3, 4, 5], [1, 4, 2, 5, 3])
    hit = sum(abs(spearmanr([1, 2, 3, 4, 5], q).statistic) >= abs(r) - 1e-12
              for q in itertools.permutations([1, 4, 2, 5, 3]))
    assert p == pytest.approx(hit / 120)


def test_spearman_konstan_tak_terdefinisi():
    r, p = af.spearman_eksak([1.3, 1.4, 1.5, 1.6, 1.7], [0, 0, 0, 0, 0])   # mis. Delta-F1-ACSA semua nol
    assert np.isnan(r) and np.isnan(p)


def test_baca_daftar_dan_perluasan_sentimen(tmp_path):
    (tmp_path / "kamus.csv").write_text("slang,formal,category\ngk,tidak,x\nmantul,mantap,x\nyg,yang,x\n",
                                        encoding="utf-8")
    (tmp_path / "pos.txt").write_text("# komentar\nmantap\n\nBagus\n", encoding="utf-8")
    (tmp_path / "aspek.txt").write_text("otp\nverifikasi wajah\n", encoding="utf-8")
    entri, peta = af.baca_daftar(tmp_path / "kamus.csv")
    assert entri == ["gk", "mantul", "yg"] and peta["mantul"] == "mantap"

    class Arg:
        leksikon_takbaku = tmp_path / "kamus.csv"
        kata_aspek = tmp_path / "aspek.txt"
        leksikon_sentimen = [tmp_path / "pos.txt"]
    kelas, catatan = af.siapkan_kelas(Arg)
    assert kelas["PEMBAWA_SENTIMEN"] == {"mantap", "bagus", "mantul"}   # mantul ditambahkan lewat padanan
    assert kelas["PENANDA_ASPEK"] == {"otp"}                            # frasa tidak dipakai
    assert any("1 entri berupa frasa" in c for c in catatan)


def test_penanda_aspek_netral_tanpa_irisan_sentimen(tmp_path):
    (tmp_path / "aspek.txt").write_text("otp\npin\ntakut\nlemot\n", encoding="utf-8")
    (tmp_path / "neg.txt").write_text("takut\nlambat\n", encoding="utf-8")
    (tmp_path / "kamus.csv").write_text("slang,formal\nlemot,lambat\n", encoding="utf-8")

    class Arg:
        leksikon_takbaku = tmp_path / "kamus.csv"
        kata_aspek = tmp_path / "aspek.txt"
        leksikon_sentimen = [tmp_path / "neg.txt"]
    kelas, catatan = af.siapkan_kelas(Arg)
    # takut ada di leksikon; lemot masuk sentimen lewat padanan bakunya (lambat)
    assert kelas["PEMBAWA_SENTIMEN"] == {"takut", "lambat", "lemot"}
    assert kelas["PENANDA_ASPEK_NETRAL"] == {"otp", "pin"}
    assert any("Irisan kedua kelas 2 kata: lemot, takut" in c for c in catatan)


def test_kelompok_label_menggabungkan_titik_berimpit():
    hasil = af.kelompok_label([("AU", 1.40, 0.0), ("PD", 1.401, 0.0), ("KA", 2.0, 5.0)], 1.0, 10.0)
    assert [h[0] for h in hasil] == ["AU/PD", "KA"]


def test_baca_daftar_format_kata_skor(tmp_path):
    (tmp_path / "sentiwords_id.txt").write_text("abadi:5\nburuk:-4\nabu-abu:-1\nkecewa\t-4\n", encoding="utf-8")
    entri, peta = af.baca_daftar(tmp_path / "sentiwords_id.txt")
    assert entri == ["abadi", "buruk", "abu-abu", "kecewa"] and peta is None
