# Ringkasan evaluasi

Benih pelatihan 42 | 10000 penarikan bootstrap (benih 42) | polaritas mode terbatas | alfa 0,05 | koreksi Holm per keluarga

## Dukungan kelas pada himpunan uji berpasangan (per pasangan)

| Kelompok | Emas ADA | NEGATIF | POSITIF | Kelas POSITIF dilaporkan? |
|---|---|---|---|---|
| KEAMANAN | 259 | 246 | 13 | tidak (< 20) |
| KONTROL | 492 | 432 | 60 | ya, eksploratori |

## Pemotongan token pada himpunan uji berpasangan

| Model | FORMAL terpotong | INFORMAL terpotong | Pasangan yang hanya satu versinya terpotong |
|---|---|---|---|
| indobert | 7,16% | 9,42% | 17 |
| indobertweet | 8,90% | 8,55% | 14 |

## Himpunan uji berpasangan - cakupan SEMUA (KONFIRMATORI: dasar keputusan H1-H3)

### Kinerja dan penurunan (H1, uji penjaga)

| Model | Metrik | F1 FORMAL | F1 INFORMAL | Delta-F1 (pp) | Selang 95% | McNemar b/c | p | p Holm | H0 ditolak |
|---|---|---|---|---|---|---|---|---|---|
| indobert | F1-ACD | 77,22 | 77,51 | -0,29 | -2,13 s.d. 1,54 | 73/73 | 0,533 | 1,000 | TIDAK |
| indobert | F1-ACSA (NEGATIF) | 97,92 | 98,14 | -0,23 | -0,71 s.d. 0,23 | 5/8 | 0,867 | 1,000 | TIDAK |
| indobert | F1-pasangan | 75,36 | 75,53 | -0,17 | -2,02 s.d. 1,63 | 72/71 | 0,500 | 1,000 | TIDAK |
| indobertweet | F1-ACD | 80,90 | 79,54 | 1,36 | -0,17 s.d. 2,94 | 60/48 | 0,145 | 0,869 | TIDAK |
| indobertweet | F1-ACSA (NEGATIF) | 98,07 | 98,00 | 0,08 | -0,30 s.d. 0,46 | 4/3 | 0,500 | 1,000 | TIDAK |
| indobertweet | F1-pasangan | 78,66 | 77,67 | 0,98 | -0,56 s.d. 2,58 | 57/48 | 0,218 | 1,000 | TIDAK |

Uji penjaga: 0 dari 6 hipotesis nol ditolak. Bagi sel yang tidak ditolak, H2 dan H3 tetap dilaporkan tetapi ditafsirkan hati-hati.

### Delta-kuadrat (H2)

| Metrik | Delta-kuadrat (pp) | Selang 95% | p | p Holm | H0 ditolak |
|---|---|---|---|---|---|
| F1-ACD | -1,65 | -3,90 s.d. 0,64 | 0,150 | 0,449 | TIDAK |
| F1-ACSA (NEGATIF) | -0,30 | -0,83 s.d. 0,22 | 0,227 | 0,453 | TIDAK |
| F1-pasangan | -1,15 | -3,41 s.d. 1,09 | 0,312 | 0,453 | TIDAK |

### Selisih subtugas, Delta-F1-ACSA dikurangi Delta-F1-ACD (H3)

| Model | Selisih (pp) | Selang 95% | p | p Holm | H0 ditolak |
|---|---|---|---|---|---|
| indobert | 0,06 | -1,83 s.d. 2,00 | 0,475 | 0,950 | TIDAK |
| indobertweet | -1,28 | -2,88 s.d. 0,24 | 0,944 | 0,950 | TIDAK |

### Dua model dalam satu register (McNemar dua arah)

| Register | Metrik | b (indobert saja benar) | c (indobertweet saja benar) | p | p Holm | H0 ditolak |
|---|---|---|---|---|---|---|
| FORMAL | F1-ACD | 63 | 108 | < 0,001 | 0,004 | YA |
| FORMAL | F1-ACSA (NEGATIF) | 7 | 9 | 0,804 | 1,000 | TIDAK |
| FORMAL | F1-pasangan | 63 | 105 | 0,001 | 0,007 | YA |
| INFORMAL | F1-ACD | 63 | 96 | 0,011 | 0,034 | YA |
| INFORMAL | F1-ACSA (NEGATIF) | 7 | 5 | 0,774 | 1,000 | TIDAK |
| INFORMAL | F1-pasangan | 62 | 96 | 0,008 | 0,034 | YA |

## Himpunan uji berpasangan - cakupan KEAMANAN (ANALISIS LANJUTAN: tidak dipakai untuk menerima atau menolak H1-H3)

### Kinerja dan penurunan (H1, uji penjaga)

| Model | Metrik | F1 FORMAL | F1 INFORMAL | Delta-F1 (pp) | Selang 95% | McNemar b/c | p | p Holm | H0 ditolak |
|---|---|---|---|---|---|---|---|---|---|
| indobert | F1-ACD | 78,10 | 76,73 | 1,36 | -1,65 s.d. 4,43 | 32/24 | 0,175 | 0,543 | TIDAK |
| indobert | F1-ACSA (NEGATIF) | 98,58 | 98,59 | -0,01 | -0,61 s.d. 0,59 | 1/1 | 0,750 | 1,000 | TIDAK |
| indobert | F1-pasangan | 76,86 | 75,10 | 1,76 | -1,21 s.d. 4,72 | 31/22 | 0,136 | 0,543 | TIDAK |
| indobertweet | F1-ACD | 82,31 | 78,28 | 4,03 | 1,40 s.d. 6,87 | 31/14 | 0,008 | 0,048 | YA |
| indobertweet | F1-ACSA (NEGATIF) | 98,39 | 98,39 | 0,00 | 0,00 s.d. 0,00 | 0/0 | 1,000 | 1,000 | TIDAK |
| indobertweet | F1-pasangan | 79,92 | 75,82 | 4,10 | 1,46 s.d. 6,96 | 31/14 | 0,008 | 0,048 | YA |

Uji penjaga: 2 dari 6 hipotesis nol ditolak. Bagi sel yang tidak ditolak, H2 dan H3 tetap dilaporkan tetapi ditafsirkan hati-hati.

### Delta-kuadrat (H2)

| Metrik | Delta-kuadrat (pp) | Selang 95% | p | p Holm | H0 ditolak |
|---|---|---|---|---|---|
| F1-ACD | -2,66 | -6,47 s.d. 1,23 | 0,177 | 0,531 | TIDAK |
| F1-ACSA (NEGATIF) | -0,01 | -0,61 s.d. 0,59 | 0,965 | 0,965 | TIDAK |
| F1-pasangan | -2,34 | -6,20 s.d. 1,49 | 0,228 | 0,531 | TIDAK |

### Selisih subtugas, Delta-F1-ACSA dikurangi Delta-F1-ACD (H3)

| Model | Selisih (pp) | Selang 95% | p | p Holm | H0 ditolak |
|---|---|---|---|---|---|
| indobert | -1,37 | -4,53 s.d. 1,74 | 0,806 | 1,000 | TIDAK |
| indobertweet | -4,03 | -6,87 s.d. -1,40 | 0,999 | 1,000 | TIDAK |

### Dua model dalam satu register (McNemar dua arah)

| Register | Metrik | b (indobert saja benar) | c (indobertweet saja benar) | p | p Holm | H0 ditolak |
|---|---|---|---|---|---|---|
| FORMAL | F1-ACD | 26 | 43 | 0,053 | 0,320 | TIDAK |
| FORMAL | F1-ACSA (NEGATIF) | 2 | 1 | 1,000 | 1,000 | TIDAK |
| FORMAL | F1-pasangan | 25 | 39 | 0,103 | 0,517 | TIDAK |
| INFORMAL | F1-ACD | 27 | 35 | 0,374 | 1,000 | TIDAK |
| INFORMAL | F1-ACSA (NEGATIF) | 1 | 0 | 1,000 | 1,000 | TIDAK |
| INFORMAL | F1-pasangan | 27 | 33 | 0,519 | 1,000 | TIDAK |

## Himpunan uji berpasangan - cakupan KONTROL (ANALISIS LANJUTAN: tidak dipakai untuk menerima atau menolak H1-H3)

### Kinerja dan penurunan (H1, uji penjaga)

| Model | Metrik | F1 FORMAL | F1 INFORMAL | Delta-F1 (pp) | Selang 95% | McNemar b/c | p | p Holm | H0 ditolak |
|---|---|---|---|---|---|---|---|---|---|
| indobert | F1-ACD | 76,75 | 77,92 | -1,17 | -3,31 s.d. 0,91 | 41/49 | 0,829 | 1,000 | TIDAK |
| indobert | F1-ACSA (NEGATIF) | 97,53 | 97,89 | -0,36 | -1,07 s.d. 0,36 | 4/7 | 0,887 | 1,000 | TIDAK |
| indobert | F1-pasangan | 74,56 | 75,76 | -1,20 | -3,35 s.d. 0,86 | 41/49 | 0,829 | 1,000 | TIDAK |
| indobertweet | F1-ACD | 80,13 | 80,22 | -0,09 | -1,93 s.d. 1,68 | 29/34 | 0,775 | 1,000 | TIDAK |
| indobertweet | F1-ACSA (NEGATIF) | 97,89 | 97,77 | 0,12 | -0,48 s.d. 0,73 | 4/3 | 0,500 | 1,000 | TIDAK |
| indobertweet | F1-pasangan | 77,97 | 78,67 | -0,70 | -2,52 s.d. 1,07 | 26/34 | 0,877 | 1,000 | TIDAK |

Uji penjaga: 0 dari 6 hipotesis nol ditolak. Bagi sel yang tidak ditolak, H2 dan H3 tetap dilaporkan tetapi ditafsirkan hati-hati.

### Delta-kuadrat (H2)

| Metrik | Delta-kuadrat (pp) | Selang 95% | p | p Holm | H0 ditolak |
|---|---|---|---|---|---|
| F1-ACD | -1,08 | -3,70 s.d. 1,52 | 0,421 | 0,842 | TIDAK |
| F1-ACSA (NEGATIF) | -0,48 | -1,22 s.d. 0,24 | 0,215 | 0,644 | TIDAK |
| F1-pasangan | -0,49 | -3,11 s.d. 2,08 | 0,714 | 0,842 | TIDAK |

### Selisih subtugas, Delta-F1-ACSA dikurangi Delta-F1-ACD (H3)

| Model | Selisih (pp) | Selang 95% | p | p Holm | H0 ditolak |
|---|---|---|---|---|---|
| indobert | 0,81 | -1,41 s.d. 3,10 | 0,237 | 0,474 | TIDAK |
| indobertweet | 0,21 | -1,69 s.d. 2,11 | 0,416 | 0,474 | TIDAK |

### Dua model dalam satu register (McNemar dua arah)

| Register | Metrik | b (indobert saja benar) | c (indobertweet saja benar) | p | p Holm | H0 ditolak |
|---|---|---|---|---|---|---|
| FORMAL | F1-ACD | 37 | 65 | 0,007 | 0,037 | YA |
| FORMAL | F1-ACSA (NEGATIF) | 5 | 8 | 0,581 | 1,000 | TIDAK |
| FORMAL | F1-pasangan | 38 | 66 | 0,008 | 0,037 | YA |
| INFORMAL | F1-ACD | 36 | 61 | 0,014 | 0,043 | YA |
| INFORMAL | F1-ACSA (NEGATIF) | 6 | 5 | 1,000 | 1,000 | TIDAK |
| INFORMAL | F1-pasangan | 35 | 63 | 0,006 | 0,037 | YA |

### Kelas POSITIF (EKSPLORATORI, tanpa pengujian)

| Model | F1 FORMAL (selang 95%) | F1 INFORMAL (selang 95%) | Delta-F1 (selang 95%) |
|---|---|---|---|
| indobert | 84,21 (76,92 s.d. 90,28) | 86,36 (79,14 s.d. 92,20) | -2,15 (-6,34 s.d. 1,74) |
| indobertweet | 86,36 (79,59 s.d. 92,00) | 85,71 (78,26 s.d. 91,78) | 0,65 (-3,13 s.d. 4,47) |

## Per kategori aspek (EKSPLORATORI: selang kepercayaan, tanpa angka p)

| Aspek | Model | Delta-F1-ACD | Delta-F1-ACSA | Delta-F1-pasangan |
|---|---|---|---|---|
| keamanan_akun | indobert | -4,41 (-12,90 s.d. 3,88) | -0,83 (-2,80 s.d. 0,00) | -6,18 (-14,58 s.d. 1,87) |
| keamanan_akun | indobertweet | 7,49 (1,62 s.d. 14,06) | 0,00 (0,00 s.d. 0,00) | 7,76 (1,76 s.d. 14,53) |
| autentikasi | indobert | 1,66 (-1,55 s.d. 4,97) | 0,33 (0,00 s.d. 1,10) | 2,94 (-0,18 s.d. 6,21) |
| autentikasi | indobertweet | 3,26 (0,52 s.d. 6,17) | 0,00 (0,00 s.d. 0,00) | 3,26 (0,52 s.d. 6,17) |
| privasi_data | indobert | 13,67 (3,47 s.d. 25,91) | 0,00 (0,00 s.d. 0,00) | 13,67 (3,47 s.d. 25,91) |
| privasi_data | indobertweet | 4,19 (-8,16 s.d. 17,77) | 0,00 (0,00 s.d. 0,00) | 4,19 (-8,16 s.d. 17,77) |
| antarmuka | indobert | 2,03 (-2,95 s.d. 7,32) | 0,84 (-1,91 s.d. 3,91) | 3,72 (-1,04 s.d. 8,87) |
| antarmuka | indobertweet | 2,73 (-2,27 s.d. 8,07) | 0,82 (-1,61 s.d. 3,61) | 0,84 (-4,73 s.d. 6,60) |
| keandalan | indobert | -1,61 (-3,92 s.d. 0,60) | -0,56 (-1,38 s.d. 0,15) | -1,91 (-4,30 s.d. 0,38) |
| keandalan | indobertweet | -0,51 (-2,44 s.d. 1,32) | 0,00 (-0,56 s.d. 0,57) | -0,77 (-2,64 s.d. 1,06) |

## Recall kelas NEGATIF dan sebaran kekeliruan (himpunan uji berpasangan)

Recall NEGATIF = proporsi butir emas NEGATIF yang diprediksi NEGATIF oleh keputusan tiga kelas, yaitu keluhan yang tertangkap sistem dengan polaritas tepat. Selang 95% Wilson. Luput = aspek hadir tetapi diprediksi TIDAK_ADA; muncul palsu = aspek tidak hadir tetapi diprediksi hadir; terbalik = aspek tertangkap dengan polaritas keliru.

| Cakupan | Model | Register | Emas NEGATIF | Recall NEGATIF (selang 95%) | Recall deteksi | Luput | Muncul palsu | Terbalik |
|---|---|---|---|---|---|---|---|---|
| keamanan_akun | indobert | FORMAL | 63 | 46,0 (34,3 s.d. 58,2) | 52,1 | 35 | 9 | 3 |
| keamanan_akun | indobert | INFORMAL | 63 | 52,4 (40,3 s.d. 64,2) | 57,5 | 31 | 9 | 2 |
| keamanan_akun | indobertweet | FORMAL | 63 | 69,8 (57,6 s.d. 79,8) | 74,0 | 19 | 11 | 3 |
| keamanan_akun | indobertweet | INFORMAL | 63 | 57,1 (44,9 s.d. 68,6) | 63,0 | 27 | 11 | 3 |
| autentikasi | indobert | FORMAL | 148 | 89,2 (83,2 s.d. 93,2) | 87,4 | 19 | 23 | 0 |
| autentikasi | indobert | INFORMAL | 148 | 87,8 (81,6 s.d. 92,2) | 87,4 | 19 | 29 | 2 |
| autentikasi | indobertweet | FORMAL | 148 | 90,5 (84,7 s.d. 94,3) | 90,7 | 14 | 19 | 3 |
| autentikasi | indobertweet | INFORMAL | 148 | 87,2 (80,8 s.d. 91,6) | 87,4 | 19 | 24 | 3 |
| privasi_data | indobert | FORMAL | 35 | 54,3 (38,2 s.d. 69,5) | 54,3 | 16 | 4 | 0 |
| privasi_data | indobert | INFORMAL | 35 | 40,0 (25,6 s.d. 56,4) | 40,0 | 21 | 5 | 0 |
| privasi_data | indobertweet | FORMAL | 35 | 45,7 (30,5 s.d. 61,8) | 45,7 | 19 | 7 | 0 |
| privasi_data | indobertweet | INFORMAL | 35 | 37,1 (23,2 s.d. 53,7) | 37,1 | 22 | 3 | 0 |
| KEAMANAN | indobert | FORMAL | 246 | 73,2 (67,3 s.d. 78,3) | 73,0 | 70 | 36 | 3 |
| KEAMANAN | indobert | INFORMAL | 246 | 72,0 (66,0 s.d. 77,2) | 72,6 | 71 | 43 | 4 |
| KEAMANAN | indobertweet | FORMAL | 246 | 78,9 (73,3 s.d. 83,5) | 79,9 | 52 | 37 | 6 |
| KEAMANAN | indobertweet | INFORMAL | 246 | 72,4 (66,5 s.d. 77,6) | 73,7 | 68 | 38 | 6 |
| KONTROL | indobert | FORMAL | 432 | 66,9 (62,3 s.d. 71,2) | 71,1 | 142 | 70 | 10 |
| KONTROL | indobert | INFORMAL | 432 | 69,2 (64,7 s.d. 73,4) | 73,2 | 132 | 72 | 10 |
| KONTROL | indobertweet | FORMAL | 432 | 72,0 (67,6 s.d. 76,0) | 75,4 | 121 | 63 | 10 |
| KONTROL | indobertweet | INFORMAL | 432 | 70,8 (66,4 s.d. 74,9) | 73,8 | 129 | 50 | 7 |
| SEMUA | indobert | FORMAL | 678 | 69,2 (65,6 s.d. 72,5) | 71,8 | 212 | 106 | 13 |
| SEMUA | indobert | INFORMAL | 678 | 70,2 (66,7 s.d. 73,5) | 73,0 | 203 | 115 | 14 |
| SEMUA | indobertweet | FORMAL | 678 | 74,5 (71,1 s.d. 77,6) | 77,0 | 173 | 100 | 16 |
| SEMUA | indobertweet | INFORMAL | 678 | 71,4 (67,9 s.d. 74,7) | 73,8 | 197 | 88 | 13 |

## Himpunan uji tak berpasangan (pemeriksaan KETAHANAN, tidak mengikat)

Kedua register berisi ulasan yang berbeda, sehingga selisih di bawah ini memuat pengaruh isi di samping pengaruh register. Yang diperiksa hanyalah apakah ARAH dan urutan besarnya sejalan dengan himpunan berpasangan. Angka p tidak dikoreksi.

### Cakupan SEMUA

| Model | Metrik | F1 seluruhnya | F1 FORMAL | F1 INFORMAL | Delta-F1 (pp) | Selang 95% |
|---|---|---|---|---|---|---|
| indobert | F1-ACD | 75,77 | 76,80 | 74,15 | 2,65 | -1,74 s.d. 7,12 |
| indobert | F1-ACSA (NEGATIF) | 96,95 | 96,25 | 97,76 | -1,51 | -3,37 s.d. 0,36 |
| indobert | F1-pasangan | 73,76 | 74,37 | 72,80 | 1,57 | -3,03 s.d. 6,37 |
| indobertweet | F1-ACD | 78,11 | 79,38 | 76,17 | 3,21 | -0,97 s.d. 7,40 |
| indobertweet | F1-ACSA (NEGATIF) | 97,73 | 97,35 | 98,18 | -0,83 | -2,44 s.d. 0,76 |
| indobertweet | F1-pasangan | 76,12 | 76,95 | 74,83 | 2,12 | -2,35 s.d. 6,61 |

| Register | Metrik | b (indobert saja benar) | c (indobertweet saja benar) | p McNemar dua arah (tak dikoreksi) |
|---|---|---|---|---|
| FORMAL | F1-ACD | 58 | 87 | 0,020 |
| INFORMAL | F1-ACD | 43 | 55 | 0,266 |
| SEMUA | F1-ACD | 101 | 142 | 0,010 |
| FORMAL | F1-ACSA (NEGATIF) | 6 | 15 | 0,078 |
| INFORMAL | F1-ACSA (NEGATIF) | 5 | 8 | 0,581 |
| SEMUA | F1-ACSA (NEGATIF) | 11 | 23 | 0,058 |
| FORMAL | F1-pasangan | 60 | 89 | 0,021 |
| INFORMAL | F1-pasangan | 42 | 54 | 0,261 |
| SEMUA | F1-pasangan | 102 | 143 | 0,010 |

| Metrik | Delta-kuadrat (pp) | Selang 95% | p (tak dikoreksi) |
|---|---|---|---|
| F1-ACD | -0,56 | -4,11 s.d. 3,05 | 0,768 |
| F1-ACSA (NEGATIF) | -0,68 | -2,21 s.d. 0,89 | 0,389 |
| F1-pasangan | -0,55 | -4,41 s.d. 3,34 | 0,791 |

### Cakupan KEAMANAN

| Model | Metrik | F1 seluruhnya | F1 FORMAL | F1 INFORMAL | Delta-F1 (pp) | Selang 95% |
|---|---|---|---|---|---|---|
| indobert | F1-ACD | 75,44 | 75,57 | 75,26 | 0,31 | -7,17 s.d. 8,17 |
| indobert | F1-ACSA (NEGATIF) | 98,04 | 97,06 | 99,26 | -2,21 | -4,35 s.d. -0,22 |
| indobert | F1-pasangan | 72,81 | 72,04 | 73,87 | -1,83 | -9,84 s.d. 6,57 |
| indobertweet | F1-ACD | 79,77 | 80,30 | 79,05 | 1,25 | -5,80 s.d. 8,61 |
| indobertweet | F1-ACSA (NEGATIF) | 98,37 | 98,25 | 98,53 | -0,28 | -2,29 s.d. 1,73 |
| indobertweet | F1-pasangan | 77,46 | 78,28 | 76,35 | 1,93 | -5,60 s.d. 9,93 |

| Register | Metrik | b (indobert saja benar) | c (indobertweet saja benar) | p McNemar dua arah (tak dikoreksi) |
|---|---|---|---|---|
| FORMAL | F1-ACD | 11 | 30 | 0,004 |
| INFORMAL | F1-ACD | 14 | 23 | 0,188 |
| SEMUA | F1-ACD | 25 | 53 | 0,002 |
| FORMAL | F1-ACSA (NEGATIF) | 1 | 5 | 0,219 |
| INFORMAL | F1-ACSA (NEGATIF) | 2 | 0 | 0,500 |
| SEMUA | F1-ACSA (NEGATIF) | 3 | 5 | 0,727 |
| FORMAL | F1-pasangan | 11 | 33 | 0,001 |
| INFORMAL | F1-pasangan | 14 | 21 | 0,311 |
| SEMUA | F1-pasangan | 25 | 54 | 0,001 |

| Metrik | Delta-kuadrat (pp) | Selang 95% | p (tak dikoreksi) |
|---|---|---|---|
| F1-ACD | -0,94 | -6,25 s.d. 4,69 | 0,749 |
| F1-ACSA (NEGATIF) | -1,92 | -3,78 s.d. -0,31 | 0,020 |
| F1-pasangan | -3,76 | -9,25 s.d. 1,95 | 0,199 |

### Cakupan KONTROL

| Model | Metrik | F1 seluruhnya | F1 FORMAL | F1 INFORMAL | Delta-F1 (pp) | Selang 95% |
|---|---|---|---|---|---|---|
| indobert | F1-ACD | 75,95 | 77,45 | 73,45 | 4,00 | -1,55 s.d. 9,69 |
| indobert | F1-ACSA (NEGATIF) | 96,23 | 95,69 | 96,83 | -1,14 | -3,85 s.d. 1,59 |
| indobert | F1-pasangan | 74,30 | 75,60 | 72,12 | 3,47 | -2,37 s.d. 9,44 |
| indobertweet | F1-ACD | 77,16 | 78,89 | 74,29 | 4,61 | -0,75 s.d. 10,10 |
| indobertweet | F1-ACSA (NEGATIF) | 97,31 | 96,72 | 97,97 | -1,25 | -3,41 s.d. 0,90 |
| indobertweet | F1-pasangan | 75,35 | 76,25 | 73,85 | 2,41 | -3,27 s.d. 8,11 |

| Register | Metrik | b (indobert saja benar) | c (indobertweet saja benar) | p McNemar dua arah (tak dikoreksi) |
|---|---|---|---|---|
| FORMAL | F1-ACD | 47 | 57 | 0,378 |
| INFORMAL | F1-ACD | 29 | 32 | 0,798 |
| SEMUA | F1-ACD | 76 | 89 | 0,350 |
| FORMAL | F1-ACSA (NEGATIF) | 5 | 10 | 0,302 |
| INFORMAL | F1-ACSA (NEGATIF) | 3 | 8 | 0,227 |
| SEMUA | F1-ACSA (NEGATIF) | 8 | 18 | 0,076 |
| FORMAL | F1-pasangan | 49 | 56 | 0,558 |
| INFORMAL | F1-pasangan | 28 | 33 | 0,609 |
| SEMUA | F1-pasangan | 77 | 89 | 0,393 |

| Metrik | Delta-kuadrat (pp) | Selang 95% | p (tak dikoreksi) |
|---|---|---|---|
| F1-ACD | -0,60 | -5,31 s.d. 4,12 | 0,803 |
| F1-ACSA (NEGATIF) | 0,10 | -2,15 s.d. 2,45 | 0,923 |
| F1-pasangan | 1,07 | -4,00 s.d. 6,14 | 0,699 |
