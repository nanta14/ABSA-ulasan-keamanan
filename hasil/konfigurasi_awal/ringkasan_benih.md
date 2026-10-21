# Analisis kepekaan terhadap benih pelatihan

Benih dievaluasi: 42, 43, 44, 45, 46 (N = 5). Benih utama 42 tetap menjadi dasar keputusan hipotesis; benih lain hanya menilai keragaman antarlari. Seluruh lari memakai himpunan latih, hiperparameter, dan panjang masukan yang sama (Tabel 12); yang berubah hanya inisialisasi kepala klasifikasi, dropout, dan urutan tumpukan.

## Riwayat pelatihan: F1-pasangan himpunan pengembangan per epoch

| Model | Benih | Epoch 1 | Epoch 2 | Epoch 3 | Epoch 4 |
|---|---|---|---|---|---|
| indobert | 42 (utama) | 34,57 | 62,10 | 67,71 | 66,96 |
| indobert | 43 | 47,41 | 64,06 | 68,74 | 69,70 |
| indobert | 44 | 52,44 | 60,48 | 64,50 | 66,57 |
| indobert | 45 | 55,89 | 62,68 | 68,15 | 69,86 |
| indobert | 46 | 54,38 | 52,81 | 66,08 | 69,23 |
| indobertweet | 42 (utama) | 64,53 | 72,14 | 75,14 | 75,78 |
| indobertweet | 43 | 62,86 | 71,24 | 74,68 | 74,46 |
| indobertweet | 44 | 52,08 | 70,26 | 73,40 | 74,68 |
| indobertweet | 45 | 63,53 | 71,95 | 73,49 | 76,06 |
| indobertweet | 46 | 60,83 | 70,14 | 74,75 | 75,29 |

## F1 pada cakupan SEMUA (himpunan uji berpasangan)

| Model | Register | Metrik | Benih utama | Rerata | SB | Rentang |
|---|---|---|---|---|---|---|
| indobert | FORMAL | F1-ACD | 72,57 | 72,69 | 0,93 | 71,66 s.d. 74,01 |
| indobert | FORMAL | F1-ACSA (NEGATIF) | 98,52 | 97,83 | 0,41 | 97,47 s.d. 98,52 |
| indobert | FORMAL | F1-pasangan | 71,24 | 70,75 | 1,26 | 69,31 s.d. 72,39 |
| indobert | INFORMAL | F1-ACD | 70,78 | 71,96 | 0,86 | 70,78 s.d. 72,66 |
| indobert | INFORMAL | F1-ACSA (NEGATIF) | 98,31 | 98,05 | 0,24 | 97,79 s.d. 98,31 |
| indobert | INFORMAL | F1-pasangan | 69,60 | 70,60 | 0,88 | 69,60 s.d. 71,52 |
| indobertweet | FORMAL | F1-ACD | 78,04 | 78,50 | 0,36 | 78,04 s.d. 78,90 |
| indobertweet | FORMAL | F1-ACSA (NEGATIF) | 98,00 | 98,17 | 0,14 | 98,00 s.d. 98,38 |
| indobertweet | FORMAL | F1-pasangan | 75,84 | 76,40 | 0,37 | 75,84 s.d. 76,72 |
| indobertweet | INFORMAL | F1-ACD | 76,92 | 77,29 | 0,64 | 76,36 s.d. 77,94 |
| indobertweet | INFORMAL | F1-ACSA (NEGATIF) | 98,00 | 98,05 | 0,10 | 97,94 s.d. 98,16 |
| indobertweet | INFORMAL | F1-pasangan | 75,46 | 75,64 | 0,66 | 74,62 s.d. 76,36 |

## Keputusan uji per benih (koreksi Holm di dalam tiap benih)

Angka adalah jumlah benih yang menolak H0 dari N. Kolom benih utama harus sama dengan ringkasan utama evaluasi_statistik.py.

| Cakupan | Keluarga | Perbandingan | Metrik | Benih utama | Benih yang menolak H0 |
|---|---|---|---|---|---|
| SEMUA | H1 penjaga | indobert | F1-ACD | TIDAK | 0 dari 5 |
| SEMUA | H1 penjaga | indobertweet | F1-ACD | TIDAK | 0 dari 5 |
| SEMUA | Antarmodel per register | indobert vs indobertweet, FORMAL | F1-ACD | YA | 5 dari 5 |
| SEMUA | Antarmodel per register | indobert vs indobertweet, INFORMAL | F1-ACD | YA | 5 dari 5 |
| SEMUA | H2 | indobert - indobertweet | F1-ACD | TIDAK | 0 dari 5 |
| SEMUA | H1 penjaga | indobert | F1-ACSA (NEGATIF) | TIDAK | 0 dari 5 |
| SEMUA | H1 penjaga | indobertweet | F1-ACSA (NEGATIF) | TIDAK | 0 dari 5 |
| SEMUA | Antarmodel per register | indobert vs indobertweet, FORMAL | F1-ACSA (NEGATIF) | TIDAK | 0 dari 5 |
| SEMUA | Antarmodel per register | indobert vs indobertweet, INFORMAL | F1-ACSA (NEGATIF) | TIDAK | 0 dari 5 |
| SEMUA | H2 | indobert - indobertweet | F1-ACSA (NEGATIF) | TIDAK | 0 dari 5 |
| SEMUA | H1 penjaga | indobert | F1-pasangan | TIDAK | 0 dari 5 |
| SEMUA | H1 penjaga | indobertweet | F1-pasangan | TIDAK | 0 dari 5 |
| SEMUA | Antarmodel per register | indobert vs indobertweet, FORMAL | F1-pasangan | YA | 5 dari 5 |
| SEMUA | Antarmodel per register | indobert vs indobertweet, INFORMAL | F1-pasangan | YA | 5 dari 5 |
| SEMUA | H2 | indobert - indobertweet | F1-pasangan | TIDAK | 0 dari 5 |
| SEMUA | H3 | indobert | ACSA - ACD | TIDAK | 0 dari 5 |
| SEMUA | H3 | indobertweet | ACSA - ACD | TIDAK | 0 dari 5 |
| KEAMANAN | H1 penjaga | indobert | F1-ACD | TIDAK | 0 dari 5 |
| KEAMANAN | H1 penjaga | indobertweet | F1-ACD | YA | 1 dari 5 |
| KEAMANAN | Antarmodel per register | indobert vs indobertweet, FORMAL | F1-ACD | YA | 5 dari 5 |
| KEAMANAN | Antarmodel per register | indobert vs indobertweet, INFORMAL | F1-ACD | YA | 5 dari 5 |
| KEAMANAN | H2 | indobert - indobertweet | F1-ACD | TIDAK | 0 dari 5 |
| KEAMANAN | H1 penjaga | indobert | F1-ACSA (NEGATIF) | TIDAK | 0 dari 5 |
| KEAMANAN | H1 penjaga | indobertweet | F1-ACSA (NEGATIF) | TIDAK | 0 dari 5 |
| KEAMANAN | Antarmodel per register | indobert vs indobertweet, FORMAL | F1-ACSA (NEGATIF) | TIDAK | 0 dari 5 |
| KEAMANAN | Antarmodel per register | indobert vs indobertweet, INFORMAL | F1-ACSA (NEGATIF) | TIDAK | 0 dari 5 |
| KEAMANAN | H2 | indobert - indobertweet | F1-ACSA (NEGATIF) | TIDAK | 0 dari 5 |
| KEAMANAN | H1 penjaga | indobert | F1-pasangan | TIDAK | 0 dari 5 |
| KEAMANAN | H1 penjaga | indobertweet | F1-pasangan | YA | 1 dari 5 |
| KEAMANAN | Antarmodel per register | indobert vs indobertweet, FORMAL | F1-pasangan | YA | 5 dari 5 |
| KEAMANAN | Antarmodel per register | indobert vs indobertweet, INFORMAL | F1-pasangan | YA | 5 dari 5 |
| KEAMANAN | H2 | indobert - indobertweet | F1-pasangan | TIDAK | 0 dari 5 |
| KEAMANAN | H3 | indobert | ACSA - ACD | TIDAK | 0 dari 5 |
| KEAMANAN | H3 | indobertweet | ACSA - ACD | TIDAK | 0 dari 5 |
| KONTROL | H1 penjaga | indobert | F1-ACD | TIDAK | 0 dari 5 |
| KONTROL | H1 penjaga | indobertweet | F1-ACD | TIDAK | 0 dari 5 |
| KONTROL | Antarmodel per register | indobert vs indobertweet, FORMAL | F1-ACD | TIDAK | 2 dari 5 |
| KONTROL | Antarmodel per register | indobert vs indobertweet, INFORMAL | F1-ACD | YA | 3 dari 5 |
| KONTROL | H2 | indobert - indobertweet | F1-ACD | TIDAK | 0 dari 5 |
| KONTROL | H1 penjaga | indobert | F1-ACSA (NEGATIF) | TIDAK | 0 dari 5 |
| KONTROL | H1 penjaga | indobertweet | F1-ACSA (NEGATIF) | TIDAK | 0 dari 5 |
| KONTROL | Antarmodel per register | indobert vs indobertweet, FORMAL | F1-ACSA (NEGATIF) | TIDAK | 0 dari 5 |
| KONTROL | Antarmodel per register | indobert vs indobertweet, INFORMAL | F1-ACSA (NEGATIF) | TIDAK | 0 dari 5 |
| KONTROL | H2 | indobert - indobertweet | F1-ACSA (NEGATIF) | TIDAK | 0 dari 5 |
| KONTROL | H1 penjaga | indobert | F1-pasangan | TIDAK | 0 dari 5 |
| KONTROL | H1 penjaga | indobertweet | F1-pasangan | TIDAK | 0 dari 5 |
| KONTROL | Antarmodel per register | indobert vs indobertweet, FORMAL | F1-pasangan | TIDAK | 2 dari 5 |
| KONTROL | Antarmodel per register | indobert vs indobertweet, INFORMAL | F1-pasangan | YA | 4 dari 5 |
| KONTROL | H2 | indobert - indobertweet | F1-pasangan | YA | 1 dari 5 |
| KONTROL | H3 | indobert | ACSA - ACD | TIDAK | 0 dari 5 |
| KONTROL | H3 | indobertweet | ACSA - ACD | TIDAK | 0 dari 5 |

## Besaran selisih pada cakupan SEMUA

| Besaran | Model | Metrik | Benih utama | Rerata | SB antarbenih | SE bootstrap benih utama | Rentang | Searah benih utama |
|---|---|---|---|---|---|---|---|---|
| DELTA_F1 | indobert | F1-ACD | 1,79 | 0,73 | 1,05 | 1,03 | -0,90 s.d. 1,79 | 4 dari 5 |
| DELTA_F1 | indobertweet | F1-ACD | 1,11 | 1,21 | 0,45 | 0,79 | 0,61 s.d. 1,88 | 5 dari 5 |
| DELTA_F1 | indobert | F1-ACSA (NEGATIF) | 0,21 | -0,22 | 0,33 | 0,23 | -0,62 s.d. 0,21 | 1 dari 5 |
| DELTA_F1 | indobertweet | F1-ACSA (NEGATIF) | 0,00 | 0,12 | 0,20 | 0,19 | -0,08 s.d. 0,44 | - dari 5 |
| DELTA_F1 | indobert | F1-pasangan | 1,64 | 0,16 | 1,09 | 1,03 | -1,09 s.d. 1,64 | 2 dari 5 |
| DELTA_F1 | indobertweet | F1-pasangan | 0,38 | 0,77 | 0,51 | 0,84 | 0,31 s.d. 1,59 | 5 dari 5 |
| DELTA_KUADRAT | indobert - indobertweet | F1-ACD | 0,67 | -0,48 | 1,28 | 1,21 | -2,07 s.d. 0,89 | 2 dari 5 |
| DELTA_KUADRAT | indobert - indobertweet | F1-ACSA (NEGATIF) | 0,21 | -0,34 | 0,42 | 0,27 | -0,90 s.d. 0,21 | 1 dari 5 |
| DELTA_KUADRAT | indobert - indobertweet | F1-pasangan | 1,25 | -0,61 | 1,46 | 1,22 | -1,96 s.d. 1,25 | 2 dari 5 |
| SELISIH_SUBTUGAS | indobert | ACSA - ACD | -1,57 | -0,95 | 0,76 | 1,05 | -1,59 s.d. 0,28 | 4 dari 5 |
| SELISIH_SUBTUGAS | indobertweet | ACSA - ACD | -1,11 | -1,10 | 0,34 | 0,82 | -1,44 s.d. -0,54 | 5 dari 5 |

## Besaran selisih pada cakupan KEAMANAN

| Besaran | Model | Metrik | Benih utama | Rerata | SB antarbenih | SE bootstrap benih utama | Rentang | Searah benih utama |
|---|---|---|---|---|---|---|---|---|
| DELTA_F1 | indobert | F1-ACD | 0,14 | -0,47 | 1,02 | 2,00 | -1,76 s.d. 0,89 | 2 dari 5 |
| DELTA_F1 | indobertweet | F1-ACD | 4,79 | 3,51 | 0,81 | 1,57 | 2,53 s.d. 4,79 | 5 dari 5 |
| DELTA_F1 | indobert | F1-ACSA (NEGATIF) | -0,01 | -0,09 | 0,19 | 0,31 | -0,43 s.d. 0,00 | 3 dari 5 |
| DELTA_F1 | indobertweet | F1-ACSA (NEGATIF) | 0,00 | -0,08 | 0,11 | 0,00 | -0,21 s.d. 0,00 | - dari 5 |
| DELTA_F1 | indobert | F1-pasangan | 0,14 | -0,29 | 0,87 | 2,00 | -1,31 s.d. 0,88 | 2 dari 5 |
| DELTA_F1 | indobertweet | F1-pasangan | 4,40 | 3,26 | 0,70 | 1,55 | 2,51 s.d. 4,40 | 5 dari 5 |
| DELTA_KUADRAT | indobert - indobertweet | F1-ACD | -4,65 | -3,98 | 1,36 | 2,29 | -5,08 s.d. -1,64 | 5 dari 5 |
| DELTA_KUADRAT | indobert - indobertweet | F1-ACSA (NEGATIF) | -0,01 | -0,01 | 0,15 | 0,31 | -0,23 s.d. 0,20 | 2 dari 5 |
| DELTA_KUADRAT | indobert - indobertweet | F1-pasangan | -4,26 | -3,55 | 1,20 | 2,28 | -4,60 s.d. -1,63 | 5 dari 5 |
| SELISIH_SUBTUGAS | indobert | ACSA - ACD | -0,15 | 0,38 | 1,02 | 2,01 | -0,90 s.d. 1,76 | 2 dari 5 |
| SELISIH_SUBTUGAS | indobertweet | ACSA - ACD | -4,79 | -3,60 | 0,75 | 1,57 | -4,79 s.d. -2,74 | 5 dari 5 |

## Besaran selisih pada cakupan KONTROL

| Besaran | Model | Metrik | Benih utama | Rerata | SB antarbenih | SE bootstrap benih utama | Rentang | Searah benih utama |
|---|---|---|---|---|---|---|---|---|
| DELTA_F1 | indobert | F1-ACD | 2,15 | 0,98 | 1,34 | 1,10 | -1,26 s.d. 2,15 | 4 dari 5 |
| DELTA_F1 | indobertweet | F1-ACD | -0,77 | 0,03 | 0,67 | 0,96 | -0,77 s.d. 1,01 | 2 dari 5 |
| DELTA_F1 | indobert | F1-ACSA (NEGATIF) | 0,34 | -0,30 | 0,45 | 0,31 | -0,73 s.d. 0,34 | 1 dari 5 |
| DELTA_F1 | indobertweet | F1-ACSA (NEGATIF) | 0,00 | 0,23 | 0,29 | 0,29 | -0,01 s.d. 0,70 | - dari 5 |
| DELTA_F1 | indobert | F1-pasangan | 1,97 | 0,11 | 1,37 | 1,16 | -1,70 s.d. 1,97 | 2 dari 5 |
| DELTA_F1 | indobertweet | F1-pasangan | -1,68 | -0,52 | 0,89 | 1,02 | -1,68 s.d. 0,78 | 4 dari 5 |
| DELTA_KUADRAT | indobert - indobertweet | F1-ACD | 2,93 | 0,95 | 1,71 | 1,34 | -1,30 s.d. 2,93 | 3 dari 5 |
| DELTA_KUADRAT | indobert - indobertweet | F1-ACSA (NEGATIF) | 0,34 | -0,53 | 0,64 | 0,39 | -1,42 s.d. 0,34 | 1 dari 5 |
| DELTA_KUADRAT | indobert - indobertweet | F1-pasangan | 3,66 | 0,63 | 2,08 | 1,40 | -1,29 s.d. 3,66 | 3 dari 5 |
| SELISIH_SUBTUGAS | indobert | ACSA - ACD | -1,81 | -1,28 | 1,02 | 1,14 | -1,81 s.d. 0,54 | 4 dari 5 |
| SELISIH_SUBTUGAS | indobertweet | ACSA - ACD | 0,77 | 0,21 | 0,46 | 1,00 | -0,31 s.d. 0,77 | 3 dari 5 |

## Recall deteksi per aspek (himpunan uji berpasangan)

Dipakai untuk memeriksa efek lantai: aspek yang recall-nya rendah pada kedua register tidak dapat menunjukkan penurunan.

| Aspek | Model | Register | Benih utama | Rerata | Rentang |
|---|---|---|---|---|---|
| keamanan_akun | indobert | FORMAL | 15,1 | 22,5 | 15,1 s.d. 31,5 |
| keamanan_akun | indobert | INFORMAL | 15,1 | 25,8 | 15,1 s.d. 34,2 |
| keamanan_akun | indobertweet | FORMAL | 61,6 | 55,6 | 49,3 s.d. 61,6 |
| keamanan_akun | indobertweet | INFORMAL | 50,7 | 51,8 | 50,7 s.d. 53,4 |
| autentikasi | indobert | FORMAL | 71,5 | 70,9 | 65,6 s.d. 76,8 |
| autentikasi | indobert | INFORMAL | 76,2 | 75,2 | 70,2 s.d. 79,5 |
| autentikasi | indobertweet | FORMAL | 85,4 | 86,4 | 84,1 s.d. 89,4 |
| autentikasi | indobertweet | INFORMAL | 83,4 | 85,3 | 83,4 s.d. 88,7 |
| privasi_data | indobert | FORMAL | 14,3 | 15,4 | 11,4 s.d. 20,0 |
| privasi_data | indobert | INFORMAL | 14,3 | 14,3 | 11,4 s.d. 17,1 |
| privasi_data | indobertweet | FORMAL | 31,4 | 37,7 | 31,4 s.d. 45,7 |
| privasi_data | indobertweet | INFORMAL | 20,0 | 25,1 | 20,0 s.d. 28,6 |
| antarmuka | indobert | FORMAL | 46,6 | 46,0 | 43,7 s.d. 48,5 |
| antarmuka | indobert | INFORMAL | 37,9 | 39,6 | 35,9 s.d. 42,7 |
| antarmuka | indobertweet | FORMAL | 44,7 | 48,2 | 44,7 s.d. 51,5 |
| antarmuka | indobertweet | INFORMAL | 43,7 | 44,3 | 41,7 s.d. 45,6 |
| keandalan | indobert | FORMAL | 82,3 | 82,1 | 79,9 s.d. 86,4 |
| keandalan | indobert | INFORMAL | 80,2 | 81,6 | 77,4 s.d. 85,3 |
| keandalan | indobertweet | FORMAL | 77,6 | 78,6 | 77,6 s.d. 79,7 |
| keandalan | indobertweet | INFORMAL | 79,7 | 80,4 | 78,4 s.d. 82,5 |

## Cara membaca

- **SB antarbenih dibanding SE bootstrap.** SE bootstrap mengukur ketidakpastian akibat himpunan uji; SB antarbenih mengukur ketidakpastian akibat lari pelatihan. Bila SB antarbenih sebanding atau lebih besar daripada SE bootstrap, selang kepercayaan benih utama terlalu sempit sebagai gambaran ketidakpastian total, dan hal itu dinyatakan sebagai keterbatasan.
- **Searah benih utama.** Temuan arah yang hanya muncul pada sebagian benih tidak dapat dilaporkan sebagai pola yang stabil, berapa pun angka p-nya pada benih utama.
- **Keputusan uji.** Kolom benih utama adalah keputusan yang mengikat. Kolom jumlah benih hanya menunjukkan apakah keputusan itu bergantung pada benih; tidak ada penggabungan angka p antarbenih.
