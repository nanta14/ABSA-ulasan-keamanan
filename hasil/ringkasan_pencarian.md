# Pencarian hiperparameter (Subbab 3.5.3)

Kisi: laju belajar {2, 3, 5} × 10⁻⁵, ukuran tumpukan {16, 32}, epoch {2, 3, 4}; benih 42; dilatih pada himpunan latih (1650 ulasan) dan dinilai pada himpunan pengembangan (291 ulasan).

Aturan pemilihan: skor = rerata F1-pasangan pengembangan IndoBERT dan IndoBERTweet pada akhir epoch terakhir; skor tertinggi terpilih; seri (selisih < 0,01 poin persentase) diputus menurut epoch paling sedikit, lalu laju belajar paling kecil, lalu ukuran tumpukan paling kecil.

| Peringkat | Laju belajar | Tumpukan | Epoch | F1-pasangan IndoBERT | F1-pasangan IndoBERTweet | Rerata | Keterangan |
|---|---|---|---|---|---|---|---|
| 1 | 5 × 10⁻⁵ | 16 | 3 | 75,32 | 78,38 | 76,85 | **terpilih** |
| 2 | 5 × 10⁻⁵ | 16 | 4 | 74,26 | 77,75 | 76,00 |  |
| 3 | 3 × 10⁻⁵ | 16 | 4 | 73,97 | 76,62 | 75,29 |  |
| 4 | 5 × 10⁻⁵ | 32 | 4 | 71,15 | 77,97 | 74,56 |  |
| 5 | 5 × 10⁻⁵ | 16 | 2 | 70,31 | 74,86 | 72,58 |  |
| 6 | 5 × 10⁻⁵ | 32 | 3 | 67,23 | 76,81 | 72,02 |  |
| 7 | 3 × 10⁻⁵ | 16 | 3 | 67,36 | 75,50 | 71,43 |  |
| 8 | 2 × 10⁻⁵ | 16 | 4 | 66,96 | 75,78 | 71,37 | Tabel 12 |
| 9 | 3 × 10⁻⁵ | 32 | 4 | 65,97 | 75,47 | 70,72 |  |
| 10 | 2 × 10⁻⁵ | 16 | 3 | 62,07 | 73,84 | 67,95 |  |
| 11 | 3 × 10⁻⁵ | 32 | 3 | 60,44 | 72,28 | 66,36 |  |
| 12 | 3 × 10⁻⁵ | 16 | 2 | 59,35 | 72,81 | 66,08 |  |
| 13 | 2 × 10⁻⁵ | 32 | 4 | 59,15 | 71,53 | 65,34 |  |
| 14 | 2 × 10⁻⁵ | 32 | 3 | 57,79 | 68,15 | 62,97 |  |
| 15 | 2 × 10⁻⁵ | 16 | 2 | 57,66 | 67,95 | 62,80 |  |
| 16 | 5 × 10⁻⁵ | 32 | 2 | 52,74 | 72,07 | 62,41 |  |
| 17 | 3 × 10⁻⁵ | 32 | 2 | 56,13 | 67,95 | 62,04 |  |
| 18 | 2 × 10⁻⁵ | 32 | 2 | 52,84 | 60,95 | 56,89 |  |

## Kombinasi terpilih

Laju belajar 5 × 10⁻⁵, ukuran tumpukan 16, 3 epoch (rerata F1-pasangan pengembangan 76,85). Rentang skor antara kombinasi terbaik dan terburuk 19,96 poin persentase.

Kombinasi terpilih **berbeda dari Tabel 12** (peringkat 8 dari 18, rerata 71,37). Selisih skor terpilih dikurangi Tabel 12 = 5,48 poin persentase; selang kepercayaan 95% bootstrap atas ulasan pengembangan (10000 ulangan) 3,18 sampai 7,83.

Selang ini hanya keterangan tentang seberapa menentukan pilihan tersebut. Ia tidak mengubah aturan: menurut Subbab 3.5.3 nilai akhir adalah hasil pencarian, sehingga analisis konfirmatori dijalankan dengan kombinasi terpilih dan hasil konfigurasi Tabel 12 dilaporkan sebagai analisis kepekaan.

Langkah lanjut (folder keluaran baru, agar hasil Tabel 12 tidak tertimpa):

```
python latih_prediksi.py --data-dir data --keluaran-dir keluaran_terpilih --laju-belajar 5e-05 --ukuran-tumpukan 16 --epoch 3
```

Perintah yang sama diulang dengan `--benih 43` sampai `--benih 46`, lalu `evaluasi_statistik.py`, `rangkum_benih.py`, dan `analisis_fertilitas.py` dijalankan ulang atas folder tersebut.

## Pemeriksaan reproduksi lari utama

- IndoBERT: **cocok persis** dengan catatan lari utama. F1-pasangan pengembangan per epoch, lari utama: 34,57, 62,10, 67,71, 66,96; pencarian ini: 34,57, 62,10, 67,71, 66,96.
- IndoBERTweet: **cocok persis** dengan catatan lari utama. F1-pasangan pengembangan per epoch, lari utama: 64,53, 72,14, 75,14, 75,78; pencarian ini: 64,53, 72,14, 75,14, 75,78.

## Berkas yang dibaca

- `latih.csv` (1650 baris), SHA-256 `a86acdbf5326f242500454593b0998161e11be82d474a41cdde1842b5aed3505`
- `pengembangan.csv` (291 baris), SHA-256 `3bb6cd1a8d9998d1dad77460ca770fdf321febf2b95b4b311c1b5ef9efeaeb15`

Himpunan uji takberpasangan dan uji berpasangan tidak dibuka oleh skrip ini.
