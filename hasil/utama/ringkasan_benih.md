# Analisis kepekaan terhadap benih pelatihan

Benih dievaluasi: 42, 43, 44, 45, 46 (N = 5). Benih utama 42 tetap menjadi dasar keputusan hipotesis; benih lain hanya menilai keragaman antarlari. Seluruh lari memakai himpunan latih, hiperparameter, dan panjang masukan yang sama (laju belajar 5e-05, ukuran tumpukan 16, 3 epoch); yang berubah hanya inisialisasi kepala klasifikasi, dropout, dan urutan tumpukan.

## Riwayat pelatihan: F1-pasangan himpunan pengembangan per epoch

| Model | Benih | Epoch 1 | Epoch 2 | Epoch 3 |
|---|---|---|---|---|
| indobert | 42 (utama) | 48,90 | 69,75 | 75,32 |
| indobert | 43 | 56,34 | 68,10 | 70,29 |
| indobert | 44 | 61,36 | 72,48 | 73,61 |
| indobert | 45 | 53,68 | 72,19 | 71,86 |
| indobert | 46 | 56,50 | 57,70 | 71,07 |
| indobertweet | 42 (utama) | 70,36 | 75,66 | 78,38 |
| indobertweet | 43 | 67,39 | 75,39 | 75,96 |
| indobertweet | 44 | 68,28 | 76,28 | 76,77 |
| indobertweet | 45 | 71,95 | 75,97 | 79,09 |
| indobertweet | 46 | 67,84 | 73,30 | 77,09 |

## F1 pada cakupan SEMUA (himpunan uji berpasangan)

| Model | Register | Metrik | Benih utama | Rerata | SB | Rentang |
|---|---|---|---|---|---|---|
| indobert | FORMAL | F1-ACD | 77,22 | 75,84 | 1,23 | 74,46 s.d. 77,22 |
| indobert | FORMAL | F1-ACSA (NEGATIF) | 97,92 | 97,86 | 0,36 | 97,39 s.d. 98,29 |
| indobert | FORMAL | F1-pasangan | 75,36 | 73,89 | 1,09 | 72,82 s.d. 75,36 |
| indobert | INFORMAL | F1-ACD | 77,51 | 75,12 | 1,75 | 73,06 s.d. 77,51 |
| indobert | INFORMAL | F1-ACSA (NEGATIF) | 98,14 | 98,08 | 0,25 | 97,70 s.d. 98,38 |
| indobert | INFORMAL | F1-pasangan | 75,53 | 73,32 | 1,56 | 71,60 s.d. 75,53 |
| indobertweet | FORMAL | F1-ACD | 80,90 | 80,33 | 0,60 | 79,41 s.d. 80,90 |
| indobertweet | FORMAL | F1-ACSA (NEGATIF) | 98,07 | 97,97 | 0,17 | 97,69 s.d. 98,08 |
| indobertweet | FORMAL | F1-pasangan | 78,66 | 77,91 | 0,81 | 76,62 s.d. 78,66 |
| indobertweet | INFORMAL | F1-ACD | 79,54 | 79,51 | 0,66 | 79,03 s.d. 80,62 |
| indobertweet | INFORMAL | F1-ACSA (NEGATIF) | 98,00 | 98,01 | 0,12 | 97,92 s.d. 98,22 |
| indobertweet | INFORMAL | F1-pasangan | 77,67 | 77,43 | 0,94 | 76,45 s.d. 78,93 |

## Keputusan uji per benih (koreksi Holm di dalam tiap benih)

Angka adalah jumlah benih yang menolak H0 dari N. Kolom benih utama harus sama dengan ringkasan utama evaluasi_statistik.py.

| Cakupan | Keluarga | Perbandingan | Metrik | Benih utama | Benih yang menolak H0 |
|---|---|---|---|---|---|
| SEMUA | H1 penjaga | indobert | F1-ACD | TIDAK | 0 dari 5 |
| SEMUA | H1 penjaga | indobertweet | F1-ACD | TIDAK | 0 dari 5 |
| SEMUA | Antarmodel per register | indobert vs indobertweet, FORMAL | F1-ACD | YA | 4 dari 5 |
| SEMUA | Antarmodel per register | indobert vs indobertweet, INFORMAL | F1-ACD | YA | 5 dari 5 |
| SEMUA | H2 | indobert - indobertweet | F1-ACD | TIDAK | 0 dari 5 |
| SEMUA | H1 penjaga | indobert | F1-ACSA (NEGATIF) | TIDAK | 0 dari 5 |
| SEMUA | H1 penjaga | indobertweet | F1-ACSA (NEGATIF) | TIDAK | 0 dari 5 |
| SEMUA | Antarmodel per register | indobert vs indobertweet, FORMAL | F1-ACSA (NEGATIF) | TIDAK | 0 dari 5 |
| SEMUA | Antarmodel per register | indobert vs indobertweet, INFORMAL | F1-ACSA (NEGATIF) | TIDAK | 0 dari 5 |
| SEMUA | H2 | indobert - indobertweet | F1-ACSA (NEGATIF) | TIDAK | 0 dari 5 |
| SEMUA | H1 penjaga | indobert | F1-pasangan | TIDAK | 0 dari 5 |
| SEMUA | H1 penjaga | indobertweet | F1-pasangan | TIDAK | 0 dari 5 |
| SEMUA | Antarmodel per register | indobert vs indobertweet, FORMAL | F1-pasangan | YA | 4 dari 5 |
| SEMUA | Antarmodel per register | indobert vs indobertweet, INFORMAL | F1-pasangan | YA | 5 dari 5 |
| SEMUA | H2 | indobert - indobertweet | F1-pasangan | TIDAK | 0 dari 5 |
| SEMUA | H3 | indobert | ACSA - ACD | TIDAK | 0 dari 5 |
| SEMUA | H3 | indobertweet | ACSA - ACD | TIDAK | 0 dari 5 |
| KEAMANAN | H1 penjaga | indobert | F1-ACD | TIDAK | 0 dari 5 |
| KEAMANAN | H1 penjaga | indobertweet | F1-ACD | YA | 1 dari 5 |
| KEAMANAN | Antarmodel per register | indobert vs indobertweet, FORMAL | F1-ACD | TIDAK | 2 dari 5 |
| KEAMANAN | Antarmodel per register | indobert vs indobertweet, INFORMAL | F1-ACD | TIDAK | 3 dari 5 |
| KEAMANAN | H2 | indobert - indobertweet | F1-ACD | TIDAK | 0 dari 5 |
| KEAMANAN | H1 penjaga | indobert | F1-ACSA (NEGATIF) | TIDAK | 0 dari 5 |
| KEAMANAN | H1 penjaga | indobertweet | F1-ACSA (NEGATIF) | TIDAK | 0 dari 5 |
| KEAMANAN | Antarmodel per register | indobert vs indobertweet, FORMAL | F1-ACSA (NEGATIF) | TIDAK | 0 dari 5 |
| KEAMANAN | Antarmodel per register | indobert vs indobertweet, INFORMAL | F1-ACSA (NEGATIF) | TIDAK | 0 dari 5 |
| KEAMANAN | H2 | indobert - indobertweet | F1-ACSA (NEGATIF) | TIDAK | 0 dari 5 |
| KEAMANAN | H1 penjaga | indobert | F1-pasangan | TIDAK | 0 dari 5 |
| KEAMANAN | H1 penjaga | indobertweet | F1-pasangan | YA | 1 dari 5 |
| KEAMANAN | Antarmodel per register | indobert vs indobertweet, FORMAL | F1-pasangan | TIDAK | 1 dari 5 |
| KEAMANAN | Antarmodel per register | indobert vs indobertweet, INFORMAL | F1-pasangan | TIDAK | 3 dari 5 |
| KEAMANAN | H2 | indobert - indobertweet | F1-pasangan | TIDAK | 0 dari 5 |
| KEAMANAN | H3 | indobert | ACSA - ACD | TIDAK | 0 dari 5 |
| KEAMANAN | H3 | indobertweet | ACSA - ACD | TIDAK | 0 dari 5 |
| KONTROL | H1 penjaga | indobert | F1-ACD | TIDAK | 0 dari 5 |
| KONTROL | H1 penjaga | indobertweet | F1-ACD | TIDAK | 0 dari 5 |
| KONTROL | Antarmodel per register | indobert vs indobertweet, FORMAL | F1-ACD | YA | 4 dari 5 |
| KONTROL | Antarmodel per register | indobert vs indobertweet, INFORMAL | F1-ACD | YA | 4 dari 5 |
| KONTROL | H2 | indobert - indobertweet | F1-ACD | TIDAK | 0 dari 5 |
| KONTROL | H1 penjaga | indobert | F1-ACSA (NEGATIF) | TIDAK | 0 dari 5 |
| KONTROL | H1 penjaga | indobertweet | F1-ACSA (NEGATIF) | TIDAK | 0 dari 5 |
| KONTROL | Antarmodel per register | indobert vs indobertweet, FORMAL | F1-ACSA (NEGATIF) | TIDAK | 0 dari 5 |
| KONTROL | Antarmodel per register | indobert vs indobertweet, INFORMAL | F1-ACSA (NEGATIF) | TIDAK | 0 dari 5 |
| KONTROL | H2 | indobert - indobertweet | F1-ACSA (NEGATIF) | TIDAK | 0 dari 5 |
| KONTROL | H1 penjaga | indobert | F1-pasangan | TIDAK | 0 dari 5 |
| KONTROL | H1 penjaga | indobertweet | F1-pasangan | TIDAK | 0 dari 5 |
| KONTROL | Antarmodel per register | indobert vs indobertweet, FORMAL | F1-pasangan | YA | 4 dari 5 |
| KONTROL | Antarmodel per register | indobert vs indobertweet, INFORMAL | F1-pasangan | YA | 4 dari 5 |
| KONTROL | H2 | indobert - indobertweet | F1-pasangan | TIDAK | 0 dari 5 |
| KONTROL | H3 | indobert | ACSA - ACD | TIDAK | 0 dari 5 |
| KONTROL | H3 | indobertweet | ACSA - ACD | TIDAK | 0 dari 5 |

## Besaran selisih pada cakupan SEMUA

| Besaran | Model | Metrik | Benih utama | Rerata | SB antarbenih | SE bootstrap benih utama | Rentang | Searah benih utama |
|---|---|---|---|---|---|---|---|---|
| DELTA_F1 | indobert | F1-ACD | -0,29 | 0,72 | 0,86 | 0,94 | -0,29 s.d. 1,92 | 1 dari 5 |
| DELTA_F1 | indobertweet | F1-ACD | 1,36 | 0,82 | 0,56 | 0,79 | 0,09 s.d. 1,36 | 5 dari 5 |
| DELTA_F1 | indobert | F1-ACSA (NEGATIF) | -0,23 | -0,22 | 0,14 | 0,24 | -0,39 s.d. -0,08 | 5 dari 5 |
| DELTA_F1 | indobertweet | F1-ACSA (NEGATIF) | 0,08 | -0,05 | 0,20 | 0,19 | -0,30 s.d. 0,15 | 3 dari 5 |
| DELTA_F1 | indobert | F1-pasangan | -0,17 | 0,57 | 0,72 | 0,93 | -0,17 s.d. 1,46 | 1 dari 5 |
| DELTA_F1 | indobertweet | F1-pasangan | 0,98 | 0,47 | 0,87 | 0,80 | -0,63 s.d. 1,19 | 3 dari 5 |
| DELTA_KUADRAT | indobert - indobertweet | F1-ACD | -1,65 | -0,10 | 0,91 | 1,16 | -1,65 s.d. 0,67 | 1 dari 5 |
| DELTA_KUADRAT | indobert - indobertweet | F1-ACSA (NEGATIF) | -0,30 | -0,18 | 0,33 | 0,27 | -0,47 s.d. 0,21 | 3 dari 5 |
| DELTA_KUADRAT | indobert - indobertweet | F1-pasangan | -1,15 | 0,10 | 0,74 | 1,15 | -1,15 s.d. 0,75 | 1 dari 5 |
| SELISIH_SUBTUGAS | indobert | ACSA - ACD | 0,06 | -0,94 | 0,93 | 0,98 | -2,32 s.d. 0,06 | 1 dari 5 |
| SELISIH_SUBTUGAS | indobertweet | ACSA - ACD | -1,28 | -0,86 | 0,52 | 0,80 | -1,28 s.d. -0,23 | 5 dari 5 |

## Besaran selisih pada cakupan KEAMANAN

| Besaran | Model | Metrik | Benih utama | Rerata | SB antarbenih | SE bootstrap benih utama | Rentang | Searah benih utama |
|---|---|---|---|---|---|---|---|---|
| DELTA_F1 | indobert | F1-ACD | 1,36 | 1,86 | 0,92 | 1,55 | 0,58 s.d. 2,98 | 5 dari 5 |
| DELTA_F1 | indobertweet | F1-ACD | 4,03 | 2,11 | 1,14 | 1,40 | 1,14 s.d. 4,03 | 5 dari 5 |
| DELTA_F1 | indobert | F1-ACSA (NEGATIF) | -0,01 | 0,07 | 0,11 | 0,31 | -0,02 s.d. 0,20 | 2 dari 5 |
| DELTA_F1 | indobertweet | F1-ACSA (NEGATIF) | 0,00 | -0,04 | 0,27 | 0,00 | -0,41 s.d. 0,20 | - dari 5 |
| DELTA_F1 | indobert | F1-pasangan | 1,76 | 2,27 | 1,35 | 1,51 | 0,13 s.d. 3,40 | 5 dari 5 |
| DELTA_F1 | indobertweet | F1-pasangan | 4,10 | 2,15 | 1,14 | 1,40 | 1,23 s.d. 4,10 | 5 dari 5 |
| DELTA_KUADRAT | indobert - indobertweet | F1-ACD | -2,66 | -0,26 | 1,82 | 1,96 | -2,66 s.d. 1,52 | 2 dari 5 |
| DELTA_KUADRAT | indobert - indobertweet | F1-ACSA (NEGATIF) | -0,01 | 0,12 | 0,28 | 0,31 | -0,22 s.d. 0,41 | 3 dari 5 |
| DELTA_KUADRAT | indobert - indobertweet | F1-pasangan | -2,34 | 0,12 | 2,01 | 1,96 | -2,34 s.d. 1,91 | 2 dari 5 |
| SELISIH_SUBTUGAS | indobert | ACSA - ACD | -1,37 | -1,78 | 0,83 | 1,60 | -2,78 s.d. -0,59 | 5 dari 5 |
| SELISIH_SUBTUGAS | indobertweet | ACSA - ACD | -4,03 | -2,15 | 1,12 | 1,40 | -4,03 s.d. -1,25 | 5 dari 5 |

## Besaran selisih pada cakupan KONTROL

| Besaran | Model | Metrik | Benih utama | Rerata | SB antarbenih | SE bootstrap benih utama | Rentang | Searah benih utama |
|---|---|---|---|---|---|---|---|---|
| DELTA_F1 | indobert | F1-ACD | -1,17 | 0,12 | 0,92 | 1,08 | -1,17 s.d. 1,36 | 2 dari 5 |
| DELTA_F1 | indobertweet | F1-ACD | -0,09 | 0,13 | 0,83 | 0,92 | -1,03 s.d. 1,16 | 3 dari 5 |
| DELTA_F1 | indobert | F1-ACSA (NEGATIF) | -0,36 | -0,39 | 0,28 | 0,36 | -0,74 s.d. -0,12 | 5 dari 5 |
| DELTA_F1 | indobertweet | F1-ACSA (NEGATIF) | 0,12 | -0,05 | 0,35 | 0,31 | -0,59 s.d. 0,35 | 2 dari 5 |
| DELTA_F1 | indobert | F1-pasangan | -1,20 | -0,31 | 0,86 | 1,07 | -1,22 s.d. 0,70 | 2 dari 5 |
| DELTA_F1 | indobertweet | F1-pasangan | -0,70 | -0,42 | 1,22 | 0,91 | -1,89 s.d. 0,95 | 3 dari 5 |
| DELTA_KUADRAT | indobert - indobertweet | F1-ACD | -1,08 | -0,01 | 0,71 | 1,33 | -1,08 s.d. 0,89 | 2 dari 5 |
| DELTA_KUADRAT | indobert - indobertweet | F1-ACSA (NEGATIF) | -0,48 | -0,34 | 0,58 | 0,37 | -0,97 s.d. 0,46 | 4 dari 5 |
| DELTA_KUADRAT | indobert - indobertweet | F1-pasangan | -0,49 | 0,11 | 1,10 | 1,32 | -0,86 s.d. 1,97 | 3 dari 5 |
| SELISIH_SUBTUGAS | indobert | ACSA - ACD | 0,81 | -0,52 | 1,07 | 1,15 | -2,09 s.d. 0,81 | 2 dari 5 |
| SELISIH_SUBTUGAS | indobertweet | ACSA - ACD | 0,21 | -0,18 | 0,74 | 0,97 | -1,16 s.d. 0,44 | 3 dari 5 |

## Recall deteksi per aspek (himpunan uji berpasangan)

Dipakai untuk memeriksa efek lantai: aspek yang recall-nya rendah pada kedua register tidak dapat menunjukkan penurunan.

| Aspek | Model | Register | Benih utama | Rerata | Rentang |
|---|---|---|---|---|---|
| keamanan_akun | indobert | FORMAL | 52,1 | 44,1 | 30,1 s.d. 52,1 |
| keamanan_akun | indobert | INFORMAL | 57,5 | 44,1 | 30,1 s.d. 57,5 |
| keamanan_akun | indobertweet | FORMAL | 74,0 | 64,9 | 57,5 s.d. 74,0 |
| keamanan_akun | indobertweet | INFORMAL | 63,0 | 60,3 | 56,2 s.d. 64,4 |
| autentikasi | indobert | FORMAL | 87,4 | 84,9 | 78,8 s.d. 88,7 |
| autentikasi | indobert | INFORMAL | 87,4 | 84,9 | 82,1 s.d. 87,4 |
| autentikasi | indobertweet | FORMAL | 90,7 | 88,9 | 86,1 s.d. 90,7 |
| autentikasi | indobertweet | INFORMAL | 87,4 | 87,5 | 84,8 s.d. 90,1 |
| privasi_data | indobert | FORMAL | 54,3 | 39,4 | 25,7 s.d. 54,3 |
| privasi_data | indobert | INFORMAL | 40,0 | 34,9 | 25,7 s.d. 45,7 |
| privasi_data | indobertweet | FORMAL | 45,7 | 49,7 | 45,7 s.d. 54,3 |
| privasi_data | indobertweet | INFORMAL | 37,1 | 41,7 | 37,1 s.d. 45,7 |
| antarmuka | indobert | FORMAL | 58,3 | 59,4 | 55,3 s.d. 63,1 |
| antarmuka | indobert | INFORMAL | 52,4 | 52,4 | 50,5 s.d. 54,4 |
| antarmuka | indobertweet | FORMAL | 58,3 | 58,8 | 55,3 s.d. 61,2 |
| antarmuka | indobertweet | INFORMAL | 51,5 | 52,4 | 49,5 s.d. 56,3 |
| keandalan | indobert | FORMAL | 74,6 | 75,1 | 73,3 s.d. 78,4 |
| keandalan | indobert | INFORMAL | 78,7 | 76,9 | 73,0 s.d. 80,2 |
| keandalan | indobertweet | FORMAL | 79,9 | 79,6 | 77,4 s.d. 81,2 |
| keandalan | indobertweet | INFORMAL | 79,7 | 80,6 | 78,7 s.d. 83,0 |

## Cara membaca

- **SB antarbenih dibanding SE bootstrap.** SE bootstrap mengukur ketidakpastian akibat himpunan uji; SB antarbenih mengukur ketidakpastian akibat lari pelatihan. Bila SB antarbenih sebanding atau lebih besar daripada SE bootstrap, selang kepercayaan benih utama terlalu sempit sebagai gambaran ketidakpastian total, dan hal itu dinyatakan sebagai keterbatasan.
- **Searah benih utama.** Temuan arah yang hanya muncul pada sebagian benih tidak dapat dilaporkan sebagai pola yang stabil, berapa pun angka p-nya pada benih utama.
- **Keputusan uji.** Kolom benih utama adalah keputusan yang mengikat. Kolom jumlah benih hanya menunjukkan apakah keputusan itu bergantung pada benih; tidak ada penggabungan angka p antarbenih.
