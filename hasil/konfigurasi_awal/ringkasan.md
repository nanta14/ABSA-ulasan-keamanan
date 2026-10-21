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
| indobert | F1-ACD | 72,57 | 70,78 | 1,79 | -0,24 s.d. 3,80 | 99/73 | 0,028 | 0,169 | TIDAK |
| indobert | F1-ACSA (NEGATIF) | 98,52 | 98,31 | 0,21 | -0,23 s.d. 0,66 | 6/3 | 0,254 | 0,580 | TIDAK |
| indobert | F1-pasangan | 71,24 | 69,60 | 1,64 | -0,42 s.d. 3,63 | 98/73 | 0,033 | 0,169 | TIDAK |
| indobertweet | F1-ACD | 78,04 | 76,92 | 1,11 | -0,42 s.d. 2,67 | 61/46 | 0,088 | 0,351 | TIDAK |
| indobertweet | F1-ACSA (NEGATIF) | 98,00 | 98,00 | 0,00 | -0,36 s.d. 0,36 | 3/3 | 0,656 | 0,656 | TIDAK |
| indobertweet | F1-pasangan | 75,84 | 75,46 | 0,38 | -1,26 s.d. 2,02 | 59/49 | 0,193 | 0,580 | TIDAK |

Uji penjaga: 0 dari 6 hipotesis nol ditolak. Bagi sel yang tidak ditolak, H2 dan H3 tetap dilaporkan tetapi ditafsirkan hati-hati.

### Delta-kuadrat (H2)

| Metrik | Delta-kuadrat (pp) | Selang 95% | p | p Holm | H0 ditolak |
|---|---|---|---|---|---|
| F1-ACD | 0,67 | -1,72 s.d. 3,01 | 0,607 | 0,993 | TIDAK |
| F1-ACSA (NEGATIF) | 0,21 | -0,30 s.d. 0,77 | 0,496 | 0,993 | TIDAK |
| F1-pasangan | 1,25 | -1,15 s.d. 3,64 | 0,325 | 0,976 | TIDAK |

### Selisih subtugas, Delta-F1-ACSA dikurangi Delta-F1-ACD (H3)

| Model | Selisih (pp) | Selang 95% | p | p Holm | H0 ditolak |
|---|---|---|---|---|---|
| indobert | -1,57 | -3,59 s.d. 0,52 | 0,930 | 1,000 | TIDAK |
| indobertweet | -1,11 | -2,74 s.d. 0,46 | 0,914 | 1,000 | TIDAK |

### Dua model dalam satu register (McNemar dua arah)

| Register | Metrik | b (indobert saja benar) | c (indobertweet saja benar) | p | p Holm | H0 ditolak |
|---|---|---|---|---|---|---|
| FORMAL | F1-ACD | 87 | 159 | < 0,001 | < 0,001 | YA |
| FORMAL | F1-ACSA (NEGATIF) | 12 | 5 | 0,143 | 0,287 | TIDAK |
| FORMAL | F1-pasangan | 86 | 152 | < 0,001 | < 0,001 | YA |
| INFORMAL | F1-ACD | 64 | 147 | < 0,001 | < 0,001 | YA |
| INFORMAL | F1-ACSA (NEGATIF) | 8 | 4 | 0,388 | 0,388 | TIDAK |
| INFORMAL | F1-pasangan | 63 | 144 | < 0,001 | < 0,001 | YA |

## Himpunan uji berpasangan - cakupan KEAMANAN (ANALISIS LANJUTAN: tidak dipakai untuk menerima atau menolak H1-H3)

### Kinerja dan penurunan (H1, uji penjaga)

| Model | Metrik | F1 FORMAL | F1 INFORMAL | Delta-F1 (pp) | Selang 95% | McNemar b/c | p | p Holm | H0 ditolak |
|---|---|---|---|---|---|---|---|---|---|
| indobert | F1-ACD | 60,93 | 60,79 | 0,14 | -3,78 s.d. 4,08 | 35/25 | 0,123 | 0,490 | TIDAK |
| indobert | F1-ACSA (NEGATIF) | 98,58 | 98,59 | -0,01 | -0,61 s.d. 0,59 | 1/1 | 0,750 | 1,000 | TIDAK |
| indobert | F1-pasangan | 60,93 | 60,79 | 0,14 | -3,78 s.d. 4,08 | 35/25 | 0,123 | 0,490 | TIDAK |
| indobertweet | F1-ACD | 78,22 | 73,43 | 4,79 | 1,82 s.d. 7,98 | 34/14 | 0,003 | 0,017 | YA |
| indobertweet | F1-ACSA (NEGATIF) | 98,39 | 98,39 | 0,00 | 0,00 s.d. 0,00 | 0/0 | 1,000 | 1,000 | TIDAK |
| indobertweet | F1-pasangan | 76,11 | 71,71 | 4,40 | 1,48 s.d. 7,57 | 33/14 | 0,004 | 0,020 | YA |

Uji penjaga: 2 dari 6 hipotesis nol ditolak. Bagi sel yang tidak ditolak, H2 dan H3 tetap dilaporkan tetapi ditafsirkan hati-hati.

### Delta-kuadrat (H2)

| Metrik | Delta-kuadrat (pp) | Selang 95% | p | p Holm | H0 ditolak |
|---|---|---|---|---|---|
| F1-ACD | -4,65 | -9,12 s.d. -0,15 | 0,043 | 0,128 | TIDAK |
| F1-ACSA (NEGATIF) | -0,01 | -0,61 s.d. 0,59 | 0,951 | 0,951 | TIDAK |
| F1-pasangan | -4,26 | -8,71 s.d. 0,24 | 0,064 | 0,128 | TIDAK |

### Selisih subtugas, Delta-F1-ACSA dikurangi Delta-F1-ACD (H3)

| Model | Selisih (pp) | Selang 95% | p | p Holm | H0 ditolak |
|---|---|---|---|---|---|
| indobert | -0,15 | -4,12 s.d. 3,76 | 0,530 | 1,000 | TIDAK |
| indobertweet | -4,79 | -7,98 s.d. -1,82 | 1,000 | 1,000 | TIDAK |

### Dua model dalam satu register (McNemar dua arah)

| Register | Metrik | b (indobert saja benar) | c (indobertweet saja benar) | p | p Holm | H0 ditolak |
|---|---|---|---|---|---|---|
| FORMAL | F1-ACD | 24 | 80 | < 0,001 | < 0,001 | YA |
| FORMAL | F1-ACSA (NEGATIF) | 2 | 1 | 1,000 | 1,000 | TIDAK |
| FORMAL | F1-pasangan | 24 | 75 | < 0,001 | < 0,001 | YA |
| INFORMAL | F1-ACD | 26 | 72 | < 0,001 | < 0,001 | YA |
| INFORMAL | F1-ACSA (NEGATIF) | 1 | 0 | 1,000 | 1,000 | TIDAK |
| INFORMAL | F1-pasangan | 26 | 68 | < 0,001 | < 0,001 | YA |

## Himpunan uji berpasangan - cakupan KONTROL (ANALISIS LANJUTAN: tidak dipakai untuk menerima atau menolak H1-H3)

### Kinerja dan penurunan (H1, uji penjaga)

| Model | Metrik | F1 FORMAL | F1 INFORMAL | Delta-F1 (pp) | Selang 95% | McNemar b/c | p | p Holm | H0 ditolak |
|---|---|---|---|---|---|---|---|---|---|
| indobert | F1-ACD | 77,56 | 75,40 | 2,15 | -0,04 s.d. 4,29 | 64/48 | 0,078 | 0,468 | TIDAK |
| indobert | F1-ACSA (NEGATIF) | 98,48 | 98,14 | 0,34 | -0,25 s.d. 0,97 | 5/2 | 0,227 | 0,906 | TIDAK |
| indobert | F1-pasangan | 75,66 | 73,68 | 1,97 | -0,35 s.d. 4,20 | 63/48 | 0,092 | 0,468 | TIDAK |
| indobertweet | F1-ACD | 77,94 | 78,71 | -0,77 | -2,66 s.d. 1,08 | 27/32 | 0,783 | 1,000 | TIDAK |
| indobertweet | F1-ACSA (NEGATIF) | 97,78 | 97,78 | 0,00 | -0,57 s.d. 0,57 | 3/3 | 0,656 | 1,000 | TIDAK |
| indobertweet | F1-pasangan | 75,70 | 77,38 | -1,68 | -3,70 s.d. 0,31 | 26/35 | 0,900 | 1,000 | TIDAK |

Uji penjaga: 0 dari 6 hipotesis nol ditolak. Bagi sel yang tidak ditolak, H2 dan H3 tetap dilaporkan tetapi ditafsirkan hati-hati.

### Delta-kuadrat (H2)

| Metrik | Delta-kuadrat (pp) | Selang 95% | p | p Holm | H0 ditolak |
|---|---|---|---|---|---|
| F1-ACD | 2,93 | 0,26 s.d. 5,51 | 0,031 | 0,062 | TIDAK |
| F1-ACSA (NEGATIF) | 0,34 | -0,36 s.d. 1,16 | 0,448 | 0,448 | TIDAK |
| F1-pasangan | 3,66 | 0,87 s.d. 6,38 | 0,010 | 0,030 | YA |

### Selisih subtugas, Delta-F1-ACSA dikurangi Delta-F1-ACD (H3)

| Model | Selisih (pp) | Selang 95% | p | p Holm | H0 ditolak |
|---|---|---|---|---|---|
| indobert | -1,81 | -4,00 s.d. 0,46 | 0,941 | 0,941 | TIDAK |
| indobertweet | 0,77 | -1,20 s.d. 2,72 | 0,221 | 0,442 | TIDAK |

### Dua model dalam satu register (McNemar dua arah)

| Register | Metrik | b (indobert saja benar) | c (indobertweet saja benar) | p | p Holm | H0 ditolak |
|---|---|---|---|---|---|---|
| FORMAL | F1-ACD | 63 | 79 | 0,208 | 0,718 | TIDAK |
| FORMAL | F1-ACSA (NEGATIF) | 10 | 4 | 0,180 | 0,718 | TIDAK |
| FORMAL | F1-pasangan | 62 | 77 | 0,235 | 0,718 | TIDAK |
| INFORMAL | F1-ACD | 38 | 75 | < 0,001 | 0,003 | YA |
| INFORMAL | F1-ACSA (NEGATIF) | 7 | 4 | 0,549 | 0,718 | TIDAK |
| INFORMAL | F1-pasangan | 37 | 76 | < 0,001 | 0,002 | YA |

### Kelas POSITIF (EKSPLORATORI, tanpa pengujian)

| Model | F1 FORMAL (selang 95%) | F1 INFORMAL (selang 95%) | Delta-F1 (selang 95%) |
|---|---|---|---|
| indobert | 89,76 (83,64 s.d. 94,74) | 86,89 (79,63 s.d. 92,78) | 2,88 (-1,24 s.d. 7,58) |
| indobertweet | 85,04 (77,04 s.d. 91,61) | 85,04 (77,36 s.d. 91,36) | 0,00 (-4,04 s.d. 4,07) |

## Per kategori aspek (EKSPLORATORI: selang kepercayaan, tanpa angka p)

| Aspek | Model | Delta-F1-ACD | Delta-F1-ACSA | Delta-F1-pasangan |
|---|---|---|---|---|
| keamanan_akun | indobert | 0,86 (-10,41 s.d. 12,22) | -0,05 (-2,43 s.d. 2,25) | 0,86 (-10,41 s.d. 12,22) |
| keamanan_akun | indobertweet | 10,99 (3,60 s.d. 19,31) | 0,00 (0,00 s.d. 0,00) | 9,47 (2,08 s.d. 17,62) |
| autentikasi | indobert | 0,71 (-3,92 s.d. 5,22) | 0,00 (0,00 s.d. 0,00) | 0,71 (-3,92 s.d. 5,22) |
| autentikasi | indobertweet | 2,28 (-0,74 s.d. 5,52) | 0,00 (0,00 s.d. 0,00) | 2,27 (-0,74 s.d. 5,51) |
| privasi_data | indobert | 0,00 (-12,38 s.d. 12,71) | 0,00 (0,00 s.d. 0,00) | 0,00 (-12,38 s.d. 12,71) |
| privasi_data | indobertweet | 11,44 (-0,54 s.d. 26,20) | 0,00 (0,00 s.d. 0,00) | 11,44 (-0,54 s.d. 26,20) |
| antarmuka | indobert | 5,13 (-0,34 s.d. 11,21) | 2,12 (-0,98 s.d. 5,74) | 5,86 (0,10 s.d. 12,41) |
| antarmuka | indobertweet | -0,98 (-6,66 s.d. 4,72) | 0,00 (-2,85 s.d. 2,92) | -4,58 (-11,30 s.d. 1,90) |
| keandalan | indobert | 2,04 (-0,46 s.d. 4,46) | 0,00 (-0,41 s.d. 0,42) | 1,79 (-0,76 s.d. 4,27) |
| keandalan | indobertweet | -0,49 (-2,35 s.d. 1,35) | 0,00 (-0,42 s.d. 0,42) | -0,77 (-2,71 s.d. 1,13) |

## Recall kelas NEGATIF dan sebaran kekeliruan (himpunan uji berpasangan)

Recall NEGATIF = proporsi butir emas NEGATIF yang diprediksi NEGATIF oleh keputusan tiga kelas, yaitu keluhan yang tertangkap sistem dengan polaritas tepat. Selang 95% Wilson. Luput = aspek hadir tetapi diprediksi TIDAK_ADA; muncul palsu = aspek tidak hadir tetapi diprediksi hadir; terbalik = aspek tertangkap dengan polaritas keliru.

| Cakupan | Model | Register | Emas NEGATIF | Recall NEGATIF (selang 95%) | Recall deteksi | Luput | Muncul palsu | Terbalik |
|---|---|---|---|---|---|---|---|---|
| keamanan_akun | indobert | FORMAL | 63 | 17,5 (10,0 s.d. 28,6) | 15,1 | 62 | 2 | 0 |
| keamanan_akun | indobert | INFORMAL | 63 | 15,9 (8,9 s.d. 26,8) | 15,1 | 62 | 5 | 0 |
| keamanan_akun | indobertweet | FORMAL | 63 | 57,1 (44,9 s.d. 68,6) | 61,6 | 28 | 5 | 3 |
| keamanan_akun | indobertweet | INFORMAL | 63 | 46,0 (34,3 s.d. 58,2) | 50,7 | 36 | 9 | 2 |
| autentikasi | indobert | FORMAL | 148 | 73,0 (65,3 s.d. 79,5) | 71,5 | 43 | 22 | 0 |
| autentikasi | indobert | INFORMAL | 148 | 77,7 (70,3 s.d. 83,7) | 76,2 | 36 | 36 | 0 |
| autentikasi | indobertweet | FORMAL | 148 | 85,8 (79,3 s.d. 90,5) | 85,4 | 22 | 20 | 2 |
| autentikasi | indobertweet | INFORMAL | 148 | 83,8 (77,0 s.d. 88,9) | 83,4 | 25 | 24 | 2 |
| privasi_data | indobert | FORMAL | 35 | 14,3 (6,3 s.d. 29,4) | 14,3 | 30 | 0 | 0 |
| privasi_data | indobert | INFORMAL | 35 | 14,3 (6,3 s.d. 29,4) | 14,3 | 30 | 0 | 0 |
| privasi_data | indobertweet | FORMAL | 35 | 31,4 (18,6 s.d. 48,0) | 31,4 | 24 | 4 | 0 |
| privasi_data | indobertweet | INFORMAL | 35 | 20,0 (10,0 s.d. 35,9) | 20,0 | 28 | 1 | 0 |
| KEAMANAN | indobert | FORMAL | 246 | 50,4 (44,2 s.d. 56,6) | 47,9 | 135 | 24 | 0 |
| KEAMANAN | indobert | INFORMAL | 246 | 52,8 (46,6 s.d. 59,0) | 50,6 | 128 | 41 | 0 |
| KEAMANAN | indobertweet | FORMAL | 246 | 70,7 (64,8 s.d. 76,1) | 71,4 | 74 | 29 | 5 |
| KEAMANAN | indobertweet | INFORMAL | 246 | 65,0 (58,9 s.d. 70,7) | 65,6 | 89 | 34 | 4 |
| KONTROL | indobert | FORMAL | 432 | 70,8 (66,4 s.d. 74,9) | 74,8 | 124 | 89 | 9 |
| KONTROL | indobert | INFORMAL | 432 | 69,0 (64,5 s.d. 73,2) | 71,3 | 141 | 88 | 8 |
| KONTROL | indobertweet | FORMAL | 432 | 67,6 (63,0 s.d. 71,8) | 70,7 | 144 | 53 | 10 |
| KONTROL | indobertweet | INFORMAL | 432 | 70,1 (65,7 s.d. 74,3) | 72,2 | 137 | 55 | 6 |
| SEMUA | indobert | FORMAL | 678 | 63,4 (59,7 s.d. 67,0) | 65,5 | 259 | 113 | 9 |
| SEMUA | indobert | INFORMAL | 678 | 63,1 (59,4 s.d. 66,7) | 64,2 | 269 | 129 | 8 |
| SEMUA | indobertweet | FORMAL | 678 | 68,7 (65,1 s.d. 72,1) | 71,0 | 218 | 82 | 15 |
| SEMUA | indobertweet | INFORMAL | 678 | 68,3 (64,7 s.d. 71,7) | 69,9 | 226 | 89 | 10 |

## Himpunan uji tak berpasangan (pemeriksaan KETAHANAN, tidak mengikat)

Kedua register berisi ulasan yang berbeda, sehingga selisih di bawah ini memuat pengaruh isi di samping pengaruh register. Yang diperiksa hanyalah apakah ARAH dan urutan besarnya sejalan dengan himpunan berpasangan. Angka p tidak dikoreksi.

### Cakupan SEMUA

| Model | Metrik | F1 seluruhnya | F1 FORMAL | F1 INFORMAL | Delta-F1 (pp) | Selang 95% |
|---|---|---|---|---|---|---|
| indobert | F1-ACD | 67,82 | 68,98 | 66,02 | 2,96 | -2,19 s.d. 8,12 |
| indobert | F1-ACSA (NEGATIF) | 96,61 | 95,86 | 97,49 | -1,64 | -3,63 s.d. 0,35 |
| indobert | F1-pasangan | 66,09 | 67,02 | 64,64 | 2,38 | -2,87 s.d. 7,72 |
| indobertweet | F1-ACD | 75,13 | 76,30 | 73,32 | 2,98 | -1,65 s.d. 7,63 |
| indobertweet | F1-ACSA (NEGATIF) | 97,44 | 96,90 | 98,06 | -1,15 | -2,97 s.d. 0,57 |
| indobertweet | F1-pasangan | 73,42 | 74,19 | 72,23 | 1,96 | -2,93 s.d. 6,89 |

| Register | Metrik | b (indobert saja benar) | c (indobertweet saja benar) | p McNemar dua arah (tak dikoreksi) |
|---|---|---|---|---|
| FORMAL | F1-ACD | 62 | 142 | < 0,001 |
| INFORMAL | F1-ACD | 39 | 90 | < 0,001 |
| SEMUA | F1-ACD | 101 | 232 | < 0,001 |
| FORMAL | F1-ACSA (NEGATIF) | 7 | 16 | 0,093 |
| INFORMAL | F1-ACSA (NEGATIF) | 3 | 7 | 0,344 |
| SEMUA | F1-ACSA (NEGATIF) | 10 | 23 | 0,035 |
| FORMAL | F1-pasangan | 59 | 138 | < 0,001 |
| INFORMAL | F1-pasangan | 36 | 88 | < 0,001 |
| SEMUA | F1-pasangan | 95 | 226 | < 0,001 |

| Metrik | Delta-kuadrat (pp) | Selang 95% | p (tak dikoreksi) |
|---|---|---|---|
| F1-ACD | -0,02 | -4,19 s.d. 4,16 | 0,980 |
| F1-ACSA (NEGATIF) | -0,48 | -1,85 s.d. 0,92 | 0,492 |
| F1-pasangan | 0,43 | -3,89 s.d. 4,67 | 0,850 |

### Cakupan KEAMANAN

| Model | Metrik | F1 seluruhnya | F1 FORMAL | F1 INFORMAL | Delta-F1 (pp) | Selang 95% |
|---|---|---|---|---|---|---|
| indobert | F1-ACD | 59,08 | 56,80 | 62,15 | -5,35 | -14,89 s.d. 4,49 |
| indobert | F1-ACSA (NEGATIF) | 97,26 | 96,25 | 98,54 | -2,29 | -5,10 s.d. 0,36 |
| indobert | F1-pasangan | 58,74 | 56,21 | 62,15 | -5,94 | -15,51 s.d. 3,91 |
| indobertweet | F1-ACD | 75,53 | 76,44 | 74,29 | 2,15 | -5,79 s.d. 10,17 |
| indobertweet | F1-ACSA (NEGATIF) | 98,22 | 97,97 | 98,54 | -0,57 | -2,72 s.d. 1,51 |
| indobertweet | F1-pasangan | 73,41 | 74,35 | 72,14 | 2,20 | -6,13 s.d. 10,84 |

| Register | Metrik | b (indobert saja benar) | c (indobertweet saja benar) | p McNemar dua arah (tak dikoreksi) |
|---|---|---|---|---|
| FORMAL | F1-ACD | 17 | 73 | < 0,001 |
| INFORMAL | F1-ACD | 18 | 41 | 0,004 |
| SEMUA | F1-ACD | 35 | 114 | < 0,001 |
| FORMAL | F1-ACSA (NEGATIF) | 0 | 6 | 0,031 |
| INFORMAL | F1-ACSA (NEGATIF) | 1 | 1 | 1,000 |
| SEMUA | F1-ACSA (NEGATIF) | 1 | 7 | 0,070 |
| FORMAL | F1-pasangan | 17 | 70 | < 0,001 |
| INFORMAL | F1-pasangan | 18 | 38 | 0,010 |
| SEMUA | F1-pasangan | 35 | 108 | < 0,001 |

| Metrik | Delta-kuadrat (pp) | Selang 95% | p (tak dikoreksi) |
|---|---|---|---|
| F1-ACD | -7,50 | -16,04 s.d. 1,15 | 0,089 |
| F1-ACSA (NEGATIF) | -1,72 | -3,51 s.d. -0,15 | 0,038 |
| F1-pasangan | -8,14 | -16,64 s.d. 0,41 | 0,061 |

### Cakupan KONTROL

| Model | Metrik | F1 seluruhnya | F1 FORMAL | F1 INFORMAL | Delta-F1 (pp) | Selang 95% |
|---|---|---|---|---|---|---|
| indobert | F1-ACD | 71,90 | 74,21 | 68,08 | 6,13 | 0,20 s.d. 12,11 |
| indobert | F1-ACSA (NEGATIF) | 96,18 | 95,58 | 96,85 | -1,26 | -3,93 s.d. 1,44 |
| indobert | F1-pasangan | 69,52 | 71,66 | 65,96 | 5,70 | -0,60 s.d. 11,90 |
| indobertweet | F1-ACD | 74,92 | 76,23 | 72,73 | 3,50 | -2,21 s.d. 9,27 |
| indobertweet | F1-ACSA (NEGATIF) | 96,92 | 96,16 | 97,76 | -1,60 | -4,10 s.d. 0,89 |
| indobertweet | F1-pasangan | 73,42 | 74,10 | 72,28 | 1,82 | -4,19 s.d. 7,89 |

| Register | Metrik | b (indobert saja benar) | c (indobertweet saja benar) | p McNemar dua arah (tak dikoreksi) |
|---|---|---|---|---|
| FORMAL | F1-ACD | 45 | 69 | 0,031 |
| INFORMAL | F1-ACD | 21 | 49 | 0,001 |
| SEMUA | F1-ACD | 66 | 118 | < 0,001 |
| FORMAL | F1-ACSA (NEGATIF) | 7 | 10 | 0,629 |
| INFORMAL | F1-ACSA (NEGATIF) | 2 | 6 | 0,289 |
| SEMUA | F1-ACSA (NEGATIF) | 9 | 16 | 0,230 |
| FORMAL | F1-pasangan | 42 | 68 | 0,017 |
| INFORMAL | F1-pasangan | 18 | 50 | < 0,001 |
| SEMUA | F1-pasangan | 60 | 118 | < 0,001 |

| Metrik | Delta-kuadrat (pp) | Selang 95% | p (tak dikoreksi) |
|---|---|---|---|
| F1-ACD | 2,63 | -1,93 s.d. 7,22 | 0,263 |
| F1-ACSA (NEGATIF) | 0,33 | -1,72 s.d. 2,42 | 0,749 |
| F1-pasangan | 3,88 | -0,96 s.d. 8,71 | 0,114 |
