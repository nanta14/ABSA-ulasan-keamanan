# Ringkasan evaluasi (ANALISIS KEPEKAAN: tanpa teks terpotong)

Benih pelatihan 42 | 10000 penarikan bootstrap (benih 42) | polaritas mode terbatas | alfa 0,05 | koreksi Holm per keluarga

Dibuang karena terpotong pada salah satu versi atau salah satu model: 62 dari 573 pasangan, 31 dari 744 ulasan tak berpasangan. Seluruh hasil di bawah berstatus KEPEKAAN dan tidak dipakai untuk menerima atau menolak hipotesis; bandingkan arah dan besarnya dengan ringkasan utama.

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

## Himpunan uji berpasangan - cakupan SEMUA (KEPEKAAN: tidak dipakai untuk menerima atau menolak H1-H3)

### Kinerja dan penurunan (H1, uji penjaga)

| Model | Metrik | F1 FORMAL | F1 INFORMAL | Delta-F1 (pp) | Selang 95% | McNemar b/c | p | p Holm | H0 ditolak |
|---|---|---|---|---|---|---|---|---|---|
| indobert | F1-ACD | 72,33 | 70,75 | 1,58 | -0,61 s.d. 3,79 | 91/71 | 0,068 | 0,406 | TIDAK |
| indobert | F1-ACSA (NEGATIF) | 98,30 | 98,14 | 0,16 | -0,28 s.d. 0,66 | 5/3 | 0,363 | 1,000 | TIDAK |
| indobert | F1-pasangan | 70,82 | 69,40 | 1,41 | -0,82 s.d. 3,65 | 90/71 | 0,078 | 0,406 | TIDAK |
| indobertweet | F1-ACD | 78,09 | 77,48 | 0,61 | -1,07 s.d. 2,30 | 49/42 | 0,265 | 1,000 | TIDAK |
| indobertweet | F1-ACSA (NEGATIF) | 97,88 | 97,88 | 0,00 | -0,42 s.d. 0,42 | 3/3 | 0,656 | 1,000 | TIDAK |
| indobertweet | F1-pasangan | 75,57 | 75,80 | -0,23 | -2,04 s.d. 1,52 | 47/45 | 0,459 | 1,000 | TIDAK |

Uji penjaga: 0 dari 6 hipotesis nol ditolak. Bagi sel yang tidak ditolak, H2 dan H3 tetap dilaporkan tetapi ditafsirkan hati-hati.

### Delta-kuadrat (H2)

| Metrik | Delta-kuadrat (pp) | Selang 95% | p | p Holm | H0 ditolak |
|---|---|---|---|---|---|
| F1-ACD | 0,98 | -1,61 s.d. 3,54 | 0,469 | 0,938 | TIDAK |
| F1-ACSA (NEGATIF) | 0,16 | -0,42 s.d. 0,78 | 0,670 | 0,938 | TIDAK |
| F1-pasangan | 1,64 | -0,96 s.d. 4,27 | 0,221 | 0,664 | TIDAK |

### Selisih subtugas, Delta-F1-ACSA dikurangi Delta-F1-ACD (H3)

| Model | Selisih (pp) | Selang 95% | p | p Holm | H0 ditolak |
|---|---|---|---|---|---|
| indobert | -1,42 | -3,65 s.d. 0,81 | 0,890 | 1,000 | TIDAK |
| indobertweet | -0,61 | -2,34 s.d. 1,13 | 0,755 | 1,000 | TIDAK |

### Dua model dalam satu register (McNemar dua arah)

| Register | Metrik | b (indobert saja benar) | c (indobertweet saja benar) | p | p Holm | H0 ditolak |
|---|---|---|---|---|---|---|
| FORMAL | F1-ACD | 75 | 143 | < 0,001 | < 0,001 | YA |
| FORMAL | F1-ACSA (NEGATIF) | 10 | 5 | 0,302 | 0,604 | TIDAK |
| FORMAL | F1-pasangan | 74 | 136 | < 0,001 | < 0,001 | YA |
| INFORMAL | F1-ACD | 52 | 133 | < 0,001 | < 0,001 | YA |
| INFORMAL | F1-ACSA (NEGATIF) | 7 | 4 | 0,549 | 0,604 | TIDAK |
| INFORMAL | F1-pasangan | 51 | 130 | < 0,001 | < 0,001 | YA |

## Himpunan uji berpasangan - cakupan KEAMANAN (KEPEKAAN: tidak dipakai untuk menerima atau menolak H1-H3)

### Kinerja dan penurunan (H1, uji penjaga)

| Model | Metrik | F1 FORMAL | F1 INFORMAL | Delta-F1 (pp) | Selang 95% | McNemar b/c | p | p Holm | H0 ditolak |
|---|---|---|---|---|---|---|---|---|---|
| indobert | F1-ACD | 61,41 | 61,21 | 0,19 | -4,24 s.d. 4,51 | 35/25 | 0,123 | 0,490 | TIDAK |
| indobert | F1-ACSA (NEGATIF) | 98,36 | 98,37 | -0,01 | -0,71 s.d. 0,67 | 1/1 | 0,750 | 1,000 | TIDAK |
| indobert | F1-pasangan | 61,41 | 61,21 | 0,19 | -4,24 s.d. 4,51 | 35/25 | 0,123 | 0,490 | TIDAK |
| indobertweet | F1-ACD | 78,83 | 74,26 | 4,57 | 1,31 s.d. 7,92 | 30/13 | 0,007 | 0,041 | YA |
| indobertweet | F1-ACSA (NEGATIF) | 98,14 | 98,14 | 0,00 | 0,00 s.d. 0,00 | 0/0 | 1,000 | 1,000 | TIDAK |
| indobertweet | F1-pasangan | 76,40 | 72,28 | 4,12 | 0,91 s.d. 7,45 | 29/13 | 0,010 | 0,049 | YA |

Uji penjaga: 2 dari 6 hipotesis nol ditolak. Bagi sel yang tidak ditolak, H2 dan H3 tetap dilaporkan tetapi ditafsirkan hati-hati.

### Delta-kuadrat (H2)

| Metrik | Delta-kuadrat (pp) | Selang 95% | p | p Holm | H0 ditolak |
|---|---|---|---|---|---|
| F1-ACD | -4,38 | -9,36 s.d. 0,56 | 0,082 | 0,247 | TIDAK |
| F1-ACSA (NEGATIF) | -0,01 | -0,71 s.d. 0,67 | 0,976 | 0,976 | TIDAK |
| F1-pasangan | -3,93 | -8,91 s.d. 0,99 | 0,119 | 0,247 | TIDAK |

### Selisih subtugas, Delta-F1-ACSA dikurangi Delta-F1-ACD (H3)

| Model | Selisih (pp) | Selang 95% | p | p Holm | H0 ditolak |
|---|---|---|---|---|---|
| indobert | -0,20 | -4,55 s.d. 4,27 | 0,536 | 1,000 | TIDAK |
| indobertweet | -4,57 | -7,92 s.d. -1,31 | 0,998 | 1,000 | TIDAK |

### Dua model dalam satu register (McNemar dua arah)

| Register | Metrik | b (indobert saja benar) | c (indobertweet saja benar) | p | p Holm | H0 ditolak |
|---|---|---|---|---|---|---|
| FORMAL | F1-ACD | 21 | 71 | < 0,001 | < 0,001 | YA |
| FORMAL | F1-ACSA (NEGATIF) | 2 | 1 | 1,000 | 1,000 | TIDAK |
| FORMAL | F1-pasangan | 21 | 66 | < 0,001 | < 0,001 | YA |
| INFORMAL | F1-ACD | 23 | 66 | < 0,001 | < 0,001 | YA |
| INFORMAL | F1-ACSA (NEGATIF) | 1 | 0 | 1,000 | 1,000 | TIDAK |
| INFORMAL | F1-pasangan | 23 | 62 | < 0,001 | < 0,001 | YA |

## Himpunan uji berpasangan - cakupan KONTROL (KEPEKAAN: tidak dipakai untuk menerima atau menolak H1-H3)

### Kinerja dan penurunan (H1, uji penjaga)

| Model | Metrik | F1 FORMAL | F1 INFORMAL | Delta-F1 (pp) | Selang 95% | McNemar b/c | p | p Holm | H0 ditolak |
|---|---|---|---|---|---|---|---|---|---|
| indobert | F1-ACD | 76,98 | 75,18 | 1,79 | -0,61 s.d. 4,16 | 56/46 | 0,186 | 1,000 | TIDAK |
| indobert | F1-ACSA (NEGATIF) | 98,27 | 98,01 | 0,26 | -0,40 s.d. 0,92 | 4/2 | 0,344 | 1,000 | TIDAK |
| indobert | F1-pasangan | 74,82 | 73,22 | 1,60 | -0,89 s.d. 4,09 | 55/46 | 0,213 | 1,000 | TIDAK |
| indobertweet | F1-ACD | 77,69 | 79,13 | -1,44 | -3,37 s.d. 0,51 | 19/29 | 0,944 | 1,000 | TIDAK |
| indobertweet | F1-ACSA (NEGATIF) | 97,74 | 97,74 | 0,00 | -0,65 s.d. 0,65 | 3/3 | 0,656 | 1,000 | TIDAK |
| indobertweet | F1-pasangan | 75,13 | 77,61 | -2,48 | -4,66 s.d. -0,38 | 18/32 | 0,984 | 1,000 | TIDAK |

Uji penjaga: 0 dari 6 hipotesis nol ditolak. Bagi sel yang tidak ditolak, H2 dan H3 tetap dilaporkan tetapi ditafsirkan hati-hati.

### Delta-kuadrat (H2)

| Metrik | Delta-kuadrat (pp) | Selang 95% | p | p Holm | H0 ditolak |
|---|---|---|---|---|---|
| F1-ACD | 3,24 | 0,40 s.d. 6,10 | 0,026 | 0,051 | TIDAK |
| F1-ACSA (NEGATIF) | 0,26 | -0,55 s.d. 1,16 | 0,629 | 0,629 | TIDAK |
| F1-pasangan | 4,08 | 1,16 s.d. 7,05 | 0,007 | 0,020 | YA |

### Selisih subtugas, Delta-F1-ACSA dikurangi Delta-F1-ACD (H3)

| Model | Selisih (pp) | Selang 95% | p | p Holm | H0 ditolak |
|---|---|---|---|---|---|
| indobert | -1,54 | -3,97 s.d. 0,89 | 0,889 | 0,889 | TIDAK |
| indobertweet | 1,44 | -0,66 s.d. 3,48 | 0,086 | 0,172 | TIDAK |

### Dua model dalam satu register (McNemar dua arah)

| Register | Metrik | b (indobert saja benar) | c (indobertweet saja benar) | p | p Holm | H0 ditolak |
|---|---|---|---|---|---|---|
| FORMAL | F1-ACD | 54 | 72 | 0,130 | 0,518 | TIDAK |
| FORMAL | F1-ACSA (NEGATIF) | 8 | 4 | 0,388 | 0,775 | TIDAK |
| FORMAL | F1-pasangan | 53 | 70 | 0,149 | 0,518 | TIDAK |
| INFORMAL | F1-ACD | 29 | 67 | < 0,001 | < 0,001 | YA |
| INFORMAL | F1-ACSA (NEGATIF) | 6 | 4 | 0,754 | 0,775 | TIDAK |
| INFORMAL | F1-pasangan | 28 | 68 | < 0,001 | < 0,001 | YA |

### Kelas POSITIF (EKSPLORATORI, tanpa pengujian)

| Model | F1 FORMAL (selang 95%) | F1 INFORMAL (selang 95%) | Delta-F1 (selang 95%) |
|---|---|---|---|
| indobert | 88,07 (80,81 s.d. 93,88) | 85,71 (77,61 s.d. 92,31) | 2,36 (-1,96 s.d. 7,43) |
| indobertweet | 84,40 (75,00 s.d. 91,59) | 84,40 (75,73 s.d. 91,28) | 0,00 (-4,83 s.d. 4,88) |

## Per kategori aspek (EKSPLORATORI: selang kepercayaan, tanpa angka p)

| Aspek | Model | Delta-F1-ACD | Delta-F1-ACSA | Delta-F1-pasangan |
|---|---|---|---|---|
| keamanan_akun | indobert | 1,13 (-11,21 s.d. 13,65) | -0,07 (-2,93 s.d. 2,70) | 1,13 (-11,21 s.d. 13,65) |
| keamanan_akun | indobertweet | 9,38 (1,52 s.d. 17,88) | 0,00 (0,00 s.d. 0,00) | 7,62 (-0,13 s.d. 16,03) |
| autentikasi | indobert | 0,79 (-4,43 s.d. 5,95) | 0,00 (0,00 s.d. 0,00) | 0,79 (-4,43 s.d. 5,95) |
| autentikasi | indobertweet | 2,18 (-1,33 s.d. 5,69) | 0,00 (0,00 s.d. 0,00) | 2,17 (-1,34 s.d. 5,68) |
| privasi_data | indobert | 0,00 (-14,10 s.d. 14,53) | 0,00 (0,00 s.d. 0,00) | 0,00 (-14,10 s.d. 14,53) |
| privasi_data | indobertweet | 14,83 (0,69 s.d. 31,09) | 0,00 (0,00 s.d. 0,00) | 14,83 (0,69 s.d. 31,09) |
| antarmuka | indobert | 5,15 (-1,05 s.d. 11,93) | 1,56 (-1,72 s.d. 5,18) | 6,09 (-0,30 s.d. 13,41) |
| antarmuka | indobertweet | -1,05 (-7,08 s.d. 5,11) | 0,00 (-3,26 s.d. 3,25) | -5,28 (-12,57 s.d. 1,80) |
| keandalan | indobert | 1,68 (-1,02 s.d. 4,38) | 0,00 (-0,47 s.d. 0,47) | 1,39 (-1,35 s.d. 4,16) |
| keandalan | indobertweet | -1,23 (-3,19 s.d. 0,70) | 0,00 (-0,48 s.d. 0,47) | -1,55 (-3,62 s.d. 0,49) |

## Recall kelas NEGATIF dan sebaran kekeliruan (himpunan uji berpasangan)

Recall NEGATIF = proporsi butir emas NEGATIF yang diprediksi NEGATIF oleh keputusan tiga kelas, yaitu keluhan yang tertangkap sistem dengan polaritas tepat. Selang 95% Wilson. Luput = aspek hadir tetapi diprediksi TIDAK_ADA; muncul palsu = aspek tidak hadir tetapi diprediksi hadir; terbalik = aspek tertangkap dengan polaritas keliru.

| Cakupan | Model | Register | Emas NEGATIF | Recall NEGATIF (selang 95%) | Recall deteksi | Luput | Muncul palsu | Terbalik |
|---|---|---|---|---|---|---|---|---|
| keamanan_akun | indobert | FORMAL | 53 | 20,8 (12,0 s.d. 33,5) | 17,7 | 51 | 2 | 0 |
| keamanan_akun | indobert | INFORMAL | 53 | 18,9 (10,6 s.d. 31,4) | 17,7 | 51 | 5 | 0 |
| keamanan_akun | indobertweet | FORMAL | 53 | 60,4 (46,9 s.d. 72,4) | 64,5 | 22 | 5 | 3 |
| keamanan_akun | indobertweet | INFORMAL | 53 | 50,9 (37,9 s.d. 63,9) | 54,8 | 28 | 8 | 2 |
| autentikasi | indobert | FORMAL | 129 | 72,9 (64,6 s.d. 79,8) | 71,2 | 38 | 19 | 0 |
| autentikasi | indobert | INFORMAL | 129 | 78,3 (70,4 s.d. 84,5) | 76,5 | 31 | 33 | 0 |
| autentikasi | indobertweet | FORMAL | 129 | 86,0 (79,0 s.d. 91,0) | 85,6 | 19 | 16 | 2 |
| autentikasi | indobertweet | INFORMAL | 129 | 84,5 (77,3 s.d. 89,7) | 84,1 | 21 | 20 | 2 |
| privasi_data | indobert | FORMAL | 31 | 12,9 (5,1 s.d. 28,9) | 12,9 | 27 | 0 | 0 |
| privasi_data | indobert | INFORMAL | 31 | 12,9 (5,1 s.d. 28,9) | 12,9 | 27 | 0 | 0 |
| privasi_data | indobertweet | FORMAL | 31 | 29,0 (16,1 s.d. 46,6) | 29,0 | 22 | 3 | 0 |
| privasi_data | indobertweet | INFORMAL | 31 | 16,1 (7,1 s.d. 32,6) | 16,1 | 26 | 1 | 0 |
| KEAMANAN | indobert | FORMAL | 213 | 51,2 (44,5 s.d. 57,8) | 48,4 | 116 | 21 | 0 |
| KEAMANAN | indobert | INFORMAL | 213 | 54,0 (47,3 s.d. 60,6) | 51,6 | 109 | 38 | 0 |
| KEAMANAN | indobertweet | FORMAL | 213 | 71,4 (65,0 s.d. 77,0) | 72,0 | 63 | 24 | 5 |
| KEAMANAN | indobertweet | INFORMAL | 213 | 66,2 (59,6 s.d. 72,2) | 66,7 | 75 | 29 | 4 |
| KONTROL | indobert | FORMAL | 379 | 70,4 (65,7 s.d. 74,8) | 74,7 | 109 | 83 | 9 |
| KONTROL | indobert | INFORMAL | 379 | 68,9 (64,0 s.d. 73,3) | 71,2 | 124 | 78 | 8 |
| KONTROL | indobertweet | FORMAL | 379 | 67,3 (62,4 s.d. 71,8) | 70,5 | 127 | 47 | 10 |
| KONTROL | indobertweet | INFORMAL | 379 | 70,4 (65,7 s.d. 74,8) | 72,3 | 119 | 45 | 6 |
| SEMUA | indobert | FORMAL | 592 | 63,5 (59,6 s.d. 67,3) | 65,6 | 225 | 104 | 9 |
| SEMUA | indobert | INFORMAL | 592 | 63,5 (59,6 s.d. 67,3) | 64,4 | 233 | 116 | 8 |
| SEMUA | indobertweet | FORMAL | 592 | 68,8 (64,9 s.d. 72,4) | 71,0 | 190 | 71 | 15 |
| SEMUA | indobertweet | INFORMAL | 592 | 68,9 (65,1 s.d. 72,5) | 70,4 | 194 | 74 | 10 |

## Himpunan uji tak berpasangan (pemeriksaan KETAHANAN, tidak mengikat)

Kedua register berisi ulasan yang berbeda, sehingga selisih di bawah ini memuat pengaruh isi di samping pengaruh register. Yang diperiksa hanyalah apakah ARAH dan urutan besarnya sejalan dengan himpunan berpasangan. Angka p tidak dikoreksi.

### Cakupan SEMUA

| Model | Metrik | F1 seluruhnya | F1 FORMAL | F1 INFORMAL | Delta-F1 (pp) | Selang 95% |
|---|---|---|---|---|---|---|
| indobert | F1-ACD | 67,46 | 68,65 | 65,43 | 3,22 | -2,11 s.d. 8,49 |
| indobert | F1-ACSA (NEGATIF) | 96,69 | 96,06 | 97,52 | -1,46 | -3,47 s.d. 0,58 |
| indobert | F1-pasangan | 65,98 | 67,03 | 64,19 | 2,84 | -2,64 s.d. 8,33 |
| indobertweet | F1-ACD | 74,67 | 76,07 | 72,25 | 3,82 | -0,96 s.d. 8,53 |
| indobertweet | F1-ACSA (NEGATIF) | 97,49 | 96,99 | 98,14 | -1,15 | -2,97 s.d. 0,66 |
| indobertweet | F1-pasangan | 73,09 | 74,11 | 71,32 | 2,79 | -2,16 s.d. 7,72 |

| Register | Metrik | b (indobert saja benar) | c (indobertweet saja benar) | p McNemar dua arah (tak dikoreksi) |
|---|---|---|---|---|
| FORMAL | F1-ACD | 62 | 142 | < 0,001 |
| INFORMAL | F1-ACD | 36 | 80 | < 0,001 |
| SEMUA | F1-ACD | 98 | 222 | < 0,001 |
| FORMAL | F1-ACSA (NEGATIF) | 7 | 15 | 0,134 |
| INFORMAL | F1-ACSA (NEGATIF) | 3 | 7 | 0,344 |
| SEMUA | F1-ACSA (NEGATIF) | 10 | 22 | 0,050 |
| FORMAL | F1-pasangan | 59 | 137 | < 0,001 |
| INFORMAL | F1-pasangan | 34 | 79 | < 0,001 |
| SEMUA | F1-pasangan | 93 | 216 | < 0,001 |

| Metrik | Delta-kuadrat (pp) | Selang 95% | p (tak dikoreksi) |
|---|---|---|---|
| F1-ACD | -0,60 | -4,96 s.d. 3,79 | 0,811 |
| F1-ACSA (NEGATIF) | -0,31 | -1,72 s.d. 1,17 | 0,661 |
| F1-pasangan | 0,05 | -4,40 s.d. 4,49 | 0,982 |

### Cakupan KEAMANAN

| Model | Metrik | F1 seluruhnya | F1 FORMAL | F1 INFORMAL | Delta-F1 (pp) | Selang 95% |
|---|---|---|---|---|---|---|
| indobert | F1-ACD | 59,36 | 56,55 | 63,48 | -6,93 | -16,50 s.d. 3,24 |
| indobert | F1-ACSA (NEGATIF) | 97,30 | 96,23 | 98,79 | -2,55 | -5,33 s.d. 0,07 |
| indobert | F1-pasangan | 59,01 | 55,95 | 63,48 | -7,53 | -17,08 s.d. 2,64 |
| indobertweet | F1-ACD | 75,12 | 76,32 | 73,31 | 3,01 | -5,06 s.d. 11,33 |
| indobertweet | F1-ACSA (NEGATIF) | 98,31 | 97,96 | 98,79 | -0,83 | -2,82 s.d. 1,27 |
| indobertweet | F1-pasangan | 73,22 | 74,21 | 71,71 | 2,50 | -5,94 s.d. 11,29 |

| Register | Metrik | b (indobert saja benar) | c (indobertweet saja benar) | p McNemar dua arah (tak dikoreksi) |
|---|---|---|---|---|
| FORMAL | F1-ACD | 17 | 73 | < 0,001 |
| INFORMAL | F1-ACD | 17 | 34 | 0,024 |
| SEMUA | F1-ACD | 34 | 107 | < 0,001 |
| FORMAL | F1-ACSA (NEGATIF) | 0 | 6 | 0,031 |
| INFORMAL | F1-ACSA (NEGATIF) | 1 | 1 | 1,000 |
| SEMUA | F1-ACSA (NEGATIF) | 1 | 7 | 0,070 |
| FORMAL | F1-pasangan | 17 | 70 | < 0,001 |
| INFORMAL | F1-pasangan | 17 | 32 | 0,044 |
| SEMUA | F1-pasangan | 34 | 102 | < 0,001 |

| Metrik | Delta-kuadrat (pp) | Selang 95% | p (tak dikoreksi) |
|---|---|---|---|
| F1-ACD | -9,94 | -18,57 s.d. -1,11 | 0,027 |
| F1-ACSA (NEGATIF) | -1,73 | -3,57 s.d. -0,04 | 0,045 |
| F1-pasangan | -10,02 | -18,59 s.d. -1,37 | 0,023 |

### Cakupan KONTROL

| Model | Metrik | F1 seluruhnya | F1 FORMAL | F1 INFORMAL | Delta-F1 (pp) | Selang 95% |
|---|---|---|---|---|---|---|
| indobert | F1-ACD | 71,32 | 73,90 | 66,51 | 7,40 | 1,18 s.d. 13,72 |
| indobert | F1-ACSA (NEGATIF) | 96,29 | 95,93 | 96,73 | -0,79 | -3,47 s.d. 2,01 |
| indobert | F1-pasangan | 69,30 | 71,83 | 64,58 | 7,26 | 0,65 s.d. 13,80 |
| indobertweet | F1-ACD | 74,43 | 75,95 | 71,57 | 4,37 | -1,63 s.d. 10,32 |
| indobertweet | F1-ACSA (NEGATIF) | 96,96 | 96,31 | 97,74 | -1,43 | -4,06 s.d. 1,15 |
| indobertweet | F1-pasangan | 73,02 | 74,05 | 71,07 | 2,99 | -3,25 s.d. 9,23 |

| Register | Metrik | b (indobert saja benar) | c (indobertweet saja benar) | p McNemar dua arah (tak dikoreksi) |
|---|---|---|---|---|
| FORMAL | F1-ACD | 45 | 69 | 0,031 |
| INFORMAL | F1-ACD | 19 | 46 | 0,001 |
| SEMUA | F1-ACD | 64 | 115 | < 0,001 |
| FORMAL | F1-ACSA (NEGATIF) | 7 | 9 | 0,804 |
| INFORMAL | F1-ACSA (NEGATIF) | 2 | 6 | 0,289 |
| SEMUA | F1-ACSA (NEGATIF) | 9 | 15 | 0,307 |
| FORMAL | F1-pasangan | 42 | 67 | 0,021 |
| INFORMAL | F1-pasangan | 17 | 47 | < 0,001 |
| SEMUA | F1-pasangan | 59 | 114 | < 0,001 |

| Metrik | Delta-kuadrat (pp) | Selang 95% | p (tak dikoreksi) |
|---|---|---|---|
| F1-ACD | 3,02 | -1,88 s.d. 8,04 | 0,225 |
| F1-ACSA (NEGATIF) | 0,64 | -1,46 s.d. 2,83 | 0,562 |
| F1-pasangan | 4,27 | -0,85 s.d. 9,40 | 0,107 |
