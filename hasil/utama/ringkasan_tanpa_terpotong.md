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
| indobert | F1-ACD | 77,25 | 78,32 | -1,07 | -3,05 s.d. 0,89 | 62/71 | 0,807 | 1,000 | TIDAK |
| indobert | F1-ACSA (NEGATIF) | 97,78 | 97,96 | -0,17 | -0,71 s.d. 0,35 | 5/7 | 0,806 | 1,000 | TIDAK |
| indobert | F1-pasangan | 75,12 | 76,07 | -0,94 | -2,93 s.d. 0,96 | 61/69 | 0,785 | 1,000 | TIDAK |
| indobertweet | F1-ACD | 80,74 | 79,90 | 0,83 | -0,80 s.d. 2,50 | 49/46 | 0,419 | 1,000 | TIDAK |
| indobertweet | F1-ACSA (NEGATIF) | 97,96 | 97,87 | 0,09 | -0,35 s.d. 0,53 | 4/3 | 0,500 | 1,000 | TIDAK |
| indobertweet | F1-pasangan | 78,18 | 77,92 | 0,25 | -1,41 s.d. 1,95 | 46/47 | 0,582 | 1,000 | TIDAK |

Uji penjaga: 0 dari 6 hipotesis nol ditolak. Bagi sel yang tidak ditolak, H2 dan H3 tetap dilaporkan tetapi ditafsirkan hati-hati.

### Delta-kuadrat (H2)

| Metrik | Delta-kuadrat (pp) | Selang 95% | p | p Holm | H0 ditolak |
|---|---|---|---|---|---|
| F1-ACD | -1,91 | -4,40 s.d. 0,53 | 0,122 | 0,367 | TIDAK |
| F1-ACSA (NEGATIF) | -0,26 | -0,82 s.d. 0,26 | 0,342 | 0,659 | TIDAK |
| F1-pasangan | -1,20 | -3,66 s.d. 1,25 | 0,329 | 0,659 | TIDAK |

### Selisih subtugas, Delta-F1-ACSA dikurangi Delta-F1-ACD (H3)

| Model | Selisih (pp) | Selang 95% | p | p Holm | H0 ditolak |
|---|---|---|---|---|---|
| indobert | 0,90 | -1,16 s.d. 2,98 | 0,194 | 0,387 | TIDAK |
| indobertweet | -0,75 | -2,45 s.d. 0,91 | 0,811 | 0,811 | TIDAK |

### Dua model dalam satu register (McNemar dua arah)

| Register | Metrik | b (indobert saja benar) | c (indobertweet saja benar) | p | p Holm | H0 ditolak |
|---|---|---|---|---|---|---|
| FORMAL | F1-ACD | 62 | 99 | 0,004 | 0,026 | YA |
| FORMAL | F1-ACSA (NEGATIF) | 6 | 8 | 0,791 | 1,000 | TIDAK |
| FORMAL | F1-pasangan | 62 | 96 | 0,008 | 0,042 | YA |
| INFORMAL | F1-ACD | 59 | 84 | 0,044 | 0,133 | TIDAK |
| INFORMAL | F1-ACSA (NEGATIF) | 6 | 5 | 1,000 | 1,000 | TIDAK |
| INFORMAL | F1-pasangan | 57 | 84 | 0,028 | 0,113 | TIDAK |

## Himpunan uji berpasangan - cakupan KEAMANAN (KEPEKAAN: tidak dipakai untuk menerima atau menolak H1-H3)

### Kinerja dan penurunan (H1, uji penjaga)

| Model | Metrik | F1 FORMAL | F1 INFORMAL | Delta-F1 (pp) | Selang 95% | McNemar b/c | p | p Holm | H0 ditolak |
|---|---|---|---|---|---|---|---|---|---|
| indobert | F1-ACD | 78,20 | 77,49 | 0,70 | -2,61 s.d. 3,97 | 29/24 | 0,292 | 0,960 | TIDAK |
| indobert | F1-ACSA (NEGATIF) | 98,36 | 98,37 | -0,01 | -0,70 s.d. 0,68 | 1/1 | 0,750 | 1,000 | TIDAK |
| indobert | F1-pasangan | 76,78 | 75,64 | 1,14 | -2,21 s.d. 4,35 | 28/22 | 0,240 | 0,960 | TIDAK |
| indobertweet | F1-ACD | 82,27 | 79,16 | 3,12 | 0,36 s.d. 6,08 | 25/14 | 0,054 | 0,324 | TIDAK |
| indobertweet | F1-ACSA (NEGATIF) | 98,14 | 98,14 | 0,00 | 0,00 s.d. 0,00 | 0/0 | 1,000 | 1,000 | TIDAK |
| indobertweet | F1-pasangan | 79,55 | 76,35 | 3,20 | 0,44 s.d. 6,18 | 25/14 | 0,054 | 0,324 | TIDAK |

Uji penjaga: 0 dari 6 hipotesis nol ditolak. Bagi sel yang tidak ditolak, H2 dan H3 tetap dilaporkan tetapi ditafsirkan hati-hati.

### Delta-kuadrat (H2)

| Metrik | Delta-kuadrat (pp) | Selang 95% | p | p Holm | H0 ditolak |
|---|---|---|---|---|---|
| F1-ACD | -2,41 | -6,65 s.d. 1,72 | 0,257 | 0,772 | TIDAK |
| F1-ACSA (NEGATIF) | -0,01 | -0,70 s.d. 0,68 | 0,953 | 0,953 | TIDAK |
| F1-pasangan | -2,06 | -6,29 s.d. 2,01 | 0,321 | 0,772 | TIDAK |

### Selisih subtugas, Delta-F1-ACSA dikurangi Delta-F1-ACD (H3)

| Model | Selisih (pp) | Selang 95% | p | p Holm | H0 ditolak |
|---|---|---|---|---|---|
| indobert | -0,71 | -4,13 s.d. 2,70 | 0,655 | 1,000 | TIDAK |
| indobertweet | -3,12 | -6,08 s.d. -0,36 | 0,987 | 1,000 | TIDAK |

### Dua model dalam satu register (McNemar dua arah)

| Register | Metrik | b (indobert saja benar) | c (indobertweet saja benar) | p | p Holm | H0 ditolak |
|---|---|---|---|---|---|---|
| FORMAL | F1-ACD | 26 | 40 | 0,109 | 0,653 | TIDAK |
| FORMAL | F1-ACSA (NEGATIF) | 2 | 1 | 1,000 | 1,000 | TIDAK |
| FORMAL | F1-pasangan | 25 | 36 | 0,200 | 1,000 | TIDAK |
| INFORMAL | F1-ACD | 24 | 32 | 0,350 | 1,000 | TIDAK |
| INFORMAL | F1-ACSA (NEGATIF) | 1 | 0 | 1,000 | 1,000 | TIDAK |
| INFORMAL | F1-pasangan | 24 | 30 | 0,497 | 1,000 | TIDAK |

## Himpunan uji berpasangan - cakupan KONTROL (KEPEKAAN: tidak dipakai untuk menerima atau menolak H1-H3)

### Kinerja dan penurunan (H1, uji penjaga)

| Model | Metrik | F1 FORMAL | F1 INFORMAL | Delta-F1 (pp) | Selang 95% | McNemar b/c | p | p Holm | H0 ditolak |
|---|---|---|---|---|---|---|---|---|---|
| indobert | F1-ACD | 76,75 | 78,77 | -2,02 | -4,30 s.d. 0,23 | 33/47 | 0,954 | 1,000 | TIDAK |
| indobert | F1-ACSA (NEGATIF) | 97,45 | 97,72 | -0,27 | -1,06 s.d. 0,46 | 4/6 | 0,828 | 1,000 | TIDAK |
| indobert | F1-pasangan | 74,25 | 76,30 | -2,05 | -4,33 s.d. 0,20 | 33/47 | 0,954 | 1,000 | TIDAK |
| indobertweet | F1-ACD | 79,90 | 80,30 | -0,40 | -2,33 s.d. 1,56 | 24/32 | 0,886 | 1,000 | TIDAK |
| indobertweet | F1-ACSA (NEGATIF) | 97,86 | 97,72 | 0,14 | -0,56 s.d. 0,85 | 4/3 | 0,500 | 1,000 | TIDAK |
| indobertweet | F1-pasangan | 77,44 | 78,78 | -1,34 | -3,31 s.d. 0,63 | 21/33 | 0,962 | 1,000 | TIDAK |

Uji penjaga: 0 dari 6 hipotesis nol ditolak. Bagi sel yang tidak ditolak, H2 dan H3 tetap dilaporkan tetapi ditafsirkan hati-hati.

### Delta-kuadrat (H2)

| Metrik | Delta-kuadrat (pp) | Selang 95% | p | p Holm | H0 ditolak |
|---|---|---|---|---|---|
| F1-ACD | -1,61 | -4,45 s.d. 1,16 | 0,264 | 0,792 | TIDAK |
| F1-ACSA (NEGATIF) | -0,41 | -1,23 s.d. 0,40 | 0,346 | 0,792 | TIDAK |
| F1-pasangan | -0,70 | -3,52 s.d. 2,13 | 0,623 | 0,792 | TIDAK |

### Selisih subtugas, Delta-F1-ACSA dikurangi Delta-F1-ACD (H3)

| Model | Selisih (pp) | Selang 95% | p | p Holm | H0 ditolak |
|---|---|---|---|---|---|
| indobert | 1,75 | -0,62 s.d. 4,18 | 0,077 | 0,155 | TIDAK |
| indobertweet | 0,54 | -1,52 s.d. 2,58 | 0,302 | 0,302 | TIDAK |

### Dua model dalam satu register (McNemar dua arah)

| Register | Metrik | b (indobert saja benar) | c (indobertweet saja benar) | p | p Holm | H0 ditolak |
|---|---|---|---|---|---|---|
| FORMAL | F1-ACD | 36 | 59 | 0,023 | 0,141 | TIDAK |
| FORMAL | F1-ACSA (NEGATIF) | 4 | 7 | 0,549 | 1,000 | TIDAK |
| FORMAL | F1-pasangan | 37 | 60 | 0,025 | 0,141 | TIDAK |
| INFORMAL | F1-ACD | 35 | 52 | 0,086 | 0,257 | TIDAK |
| INFORMAL | F1-ACSA (NEGATIF) | 5 | 5 | 1,000 | 1,000 | TIDAK |
| INFORMAL | F1-pasangan | 33 | 54 | 0,031 | 0,141 | TIDAK |

### Kelas POSITIF (EKSPLORATORI, tanpa pengujian)

| Model | F1 FORMAL (selang 95%) | F1 INFORMAL (selang 95%) | Delta-F1 (selang 95%) |
|---|---|---|---|
| indobert | 83,48 (75,44 s.d. 90,14) | 85,22 (77,23 s.d. 91,80) | -1,74 (-6,32 s.d. 2,50) |
| indobertweet | 85,96 (78,40 s.d. 92,11) | 85,22 (77,08 s.d. 91,80) | 0,75 (-3,58 s.d. 5,22) |

## Per kategori aspek (EKSPLORATORI: selang kepercayaan, tanpa angka p)

| Aspek | Model | Delta-F1-ACD | Delta-F1-ACSA | Delta-F1-pasangan |
|---|---|---|---|---|
| keamanan_akun | indobert | -4,96 (-14,59 s.d. 3,92) | -0,99 (-3,43 s.d. 0,00) | -7,01 (-16,35 s.d. 2,01) |
| keamanan_akun | indobertweet | 4,56 (-0,99 s.d. 10,75) | 0,00 (0,00 s.d. 0,00) | 4,81 (-0,82 s.d. 11,18) |
| autentikasi | indobert | 0,62 (-2,77 s.d. 4,05) | 0,38 (0,00 s.d. 1,25) | 2,08 (-1,23 s.d. 5,49) |
| autentikasi | indobertweet | 2,99 (0,00 s.d. 6,17) | 0,00 (0,00 s.d. 0,00) | 2,99 (-0,00 s.d. 6,16) |
| privasi_data | indobert | 15,60 (3,86 s.d. 29,46) | 0,00 (0,00 s.d. 0,00) | 15,60 (3,86 s.d. 29,46) |
| privasi_data | indobertweet | 4,90 (-9,23 s.d. 20,21) | 0,00 (0,00 s.d. 0,00) | 4,90 (-9,23 s.d. 20,21) |
| antarmuka | indobert | 0,21 (-5,24 s.d. 5,84) | 0,95 (-2,15 s.d. 4,40) | 2,24 (-2,63 s.d. 7,65) |
| antarmuka | indobertweet | 3,41 (-2,54 s.d. 9,78) | 0,93 (-1,88 s.d. 4,14) | 1,28 (-5,34 s.d. 8,04) |
| keandalan | indobert | -2,17 (-4,59 s.d. 0,19) | -0,48 (-1,33 s.d. 0,33) | -2,51 (-5,08 s.d. -0,08) |
| keandalan | indobertweet | -0,96 (-3,00 s.d. 1,02) | 0,00 (-0,65 s.d. 0,65) | -1,56 (-3,53 s.d. 0,39) |

## Recall kelas NEGATIF dan sebaran kekeliruan (himpunan uji berpasangan)

Recall NEGATIF = proporsi butir emas NEGATIF yang diprediksi NEGATIF oleh keputusan tiga kelas, yaitu keluhan yang tertangkap sistem dengan polaritas tepat. Selang 95% Wilson. Luput = aspek hadir tetapi diprediksi TIDAK_ADA; muncul palsu = aspek tidak hadir tetapi diprediksi hadir; terbalik = aspek tertangkap dengan polaritas keliru.

| Cakupan | Model | Register | Emas NEGATIF | Recall NEGATIF (selang 95%) | Recall deteksi | Luput | Muncul palsu | Terbalik |
|---|---|---|---|---|---|---|---|---|
| keamanan_akun | indobert | FORMAL | 53 | 49,1 (36,1 s.d. 62,1) | 54,8 | 28 | 9 | 3 |
| keamanan_akun | indobert | INFORMAL | 53 | 56,6 (43,3 s.d. 69,0) | 61,3 | 24 | 9 | 2 |
| keamanan_akun | indobertweet | FORMAL | 53 | 73,6 (60,4 s.d. 83,6) | 77,4 | 14 | 11 | 3 |
| keamanan_akun | indobertweet | INFORMAL | 53 | 64,2 (50,7 s.d. 75,7) | 69,4 | 19 | 10 | 3 |
| autentikasi | indobert | FORMAL | 129 | 88,4 (81,7 s.d. 92,8) | 86,4 | 18 | 20 | 0 |
| autentikasi | indobert | INFORMAL | 129 | 89,1 (82,6 s.d. 93,4) | 88,6 | 15 | 26 | 2 |
| autentikasi | indobertweet | FORMAL | 129 | 89,9 (83,5 s.d. 94,0) | 90,2 | 13 | 17 | 3 |
| autentikasi | indobertweet | INFORMAL | 129 | 86,8 (79,9 s.d. 91,6) | 87,1 | 17 | 21 | 3 |
| privasi_data | indobert | FORMAL | 31 | 54,8 (37,8 s.d. 70,8) | 54,8 | 14 | 3 | 0 |
| privasi_data | indobert | INFORMAL | 31 | 38,7 (23,7 s.d. 56,2) | 38,7 | 19 | 4 | 0 |
| privasi_data | indobertweet | FORMAL | 31 | 45,2 (29,2 s.d. 62,2) | 45,2 | 17 | 6 | 0 |
| privasi_data | indobertweet | INFORMAL | 31 | 35,5 (21,1 s.d. 53,1) | 35,5 | 20 | 2 | 0 |
| KEAMANAN | indobert | FORMAL | 213 | 73,7 (67,4 s.d. 79,2) | 73,3 | 60 | 32 | 3 |
| KEAMANAN | indobert | INFORMAL | 213 | 73,7 (67,4 s.d. 79,2) | 74,2 | 58 | 39 | 4 |
| KEAMANAN | indobertweet | FORMAL | 213 | 79,3 (73,4 s.d. 84,2) | 80,4 | 44 | 34 | 6 |
| KEAMANAN | indobertweet | INFORMAL | 213 | 73,7 (67,4 s.d. 79,2) | 75,1 | 56 | 33 | 6 |
| KONTROL | indobert | FORMAL | 379 | 67,0 (62,1 s.d. 71,6) | 71,4 | 123 | 63 | 10 |
| KONTROL | indobert | INFORMAL | 379 | 70,2 (65,4 s.d. 74,6) | 74,2 | 111 | 61 | 10 |
| KONTROL | indobertweet | FORMAL | 379 | 71,8 (67,0 s.d. 76,1) | 75,3 | 106 | 57 | 10 |
| KONTROL | indobertweet | INFORMAL | 379 | 70,7 (65,9 s.d. 75,1) | 73,5 | 114 | 41 | 6 |
| SEMUA | indobert | FORMAL | 592 | 69,4 (65,6 s.d. 73,0) | 72,1 | 183 | 95 | 13 |
| SEMUA | indobert | INFORMAL | 592 | 71,5 (67,7 s.d. 74,9) | 74,2 | 169 | 100 | 14 |
| SEMUA | indobertweet | FORMAL | 592 | 74,5 (70,8 s.d. 77,8) | 77,1 | 150 | 91 | 16 |
| SEMUA | indobertweet | INFORMAL | 592 | 71,8 (68,0 s.d. 75,3) | 74,0 | 170 | 74 | 12 |

## Himpunan uji tak berpasangan (pemeriksaan KETAHANAN, tidak mengikat)

Kedua register berisi ulasan yang berbeda, sehingga selisih di bawah ini memuat pengaruh isi di samping pengaruh register. Yang diperiksa hanyalah apakah ARAH dan urutan besarnya sejalan dengan himpunan berpasangan. Angka p tidak dikoreksi.

### Cakupan SEMUA

| Model | Metrik | F1 seluruhnya | F1 FORMAL | F1 INFORMAL | Delta-F1 (pp) | Selang 95% |
|---|---|---|---|---|---|---|
| indobert | F1-ACD | 75,52 | 76,58 | 73,67 | 2,92 | -1,61 s.d. 7,51 |
| indobert | F1-ACSA (NEGATIF) | 97,05 | 96,46 | 97,81 | -1,35 | -3,25 s.d. 0,58 |
| indobert | F1-pasangan | 73,73 | 74,47 | 72,45 | 2,02 | -2,77 s.d. 6,85 |
| indobertweet | F1-ACD | 77,76 | 79,19 | 75,30 | 3,89 | -0,51 s.d. 8,26 |
| indobertweet | F1-ACSA (NEGATIF) | 97,95 | 97,44 | 98,60 | -1,15 | -2,67 s.d. 0,33 |
| indobertweet | F1-pasangan | 76,10 | 76,91 | 74,70 | 2,21 | -2,46 s.d. 6,79 |

| Register | Metrik | b (indobert saja benar) | c (indobertweet saja benar) | p McNemar dua arah (tak dikoreksi) |
|---|---|---|---|---|
| FORMAL | F1-ACD | 58 | 87 | 0,020 |
| INFORMAL | F1-ACD | 38 | 47 | 0,386 |
| SEMUA | F1-ACD | 96 | 134 | 0,015 |
| FORMAL | F1-ACSA (NEGATIF) | 6 | 14 | 0,115 |
| INFORMAL | F1-ACSA (NEGATIF) | 3 | 8 | 0,227 |
| SEMUA | F1-ACSA (NEGATIF) | 9 | 22 | 0,029 |
| FORMAL | F1-pasangan | 60 | 88 | 0,026 |
| INFORMAL | F1-pasangan | 36 | 47 | 0,272 |
| SEMUA | F1-pasangan | 96 | 135 | 0,012 |

| Metrik | Delta-kuadrat (pp) | Selang 95% | p (tak dikoreksi) |
|---|---|---|---|
| F1-ACD | -0,97 | -4,75 s.d. 2,88 | 0,613 |
| F1-ACSA (NEGATIF) | -0,20 | -1,75 s.d. 1,35 | 0,807 |
| F1-pasangan | -0,19 | -4,17 s.d. 3,82 | 0,941 |

### Cakupan KEAMANAN

| Model | Metrik | F1 seluruhnya | F1 FORMAL | F1 INFORMAL | Delta-F1 (pp) | Selang 95% |
|---|---|---|---|---|---|---|
| indobert | F1-ACD | 75,54 | 75,44 | 75,68 | -0,23 | -8,02 s.d. 7,78 |
| indobert | F1-ACSA (NEGATIF) | 98,11 | 97,04 | 99,59 | -2,55 | -4,66 s.d. -0,64 |
| indobert | F1-pasangan | 73,09 | 71,90 | 74,90 | -3,00 | -11,22 s.d. 5,16 |
| indobertweet | F1-ACD | 79,58 | 80,20 | 78,65 | 1,55 | -5,88 s.d. 9,01 |
| indobertweet | F1-ACSA (NEGATIF) | 98,63 | 98,24 | 99,19 | -0,95 | -2,77 s.d. 0,86 |
| indobertweet | F1-pasangan | 77,76 | 78,17 | 77,15 | 1,02 | -6,71 s.d. 8,78 |

| Register | Metrik | b (indobert saja benar) | c (indobertweet saja benar) | p McNemar dua arah (tak dikoreksi) |
|---|---|---|---|---|
| FORMAL | F1-ACD | 11 | 30 | 0,004 |
| INFORMAL | F1-ACD | 13 | 19 | 0,377 |
| SEMUA | F1-ACD | 24 | 49 | 0,005 |
| FORMAL | F1-ACSA (NEGATIF) | 1 | 5 | 0,219 |
| INFORMAL | F1-ACSA (NEGATIF) | 1 | 0 | 1,000 |
| SEMUA | F1-ACSA (NEGATIF) | 2 | 5 | 0,453 |
| FORMAL | F1-pasangan | 11 | 33 | 0,001 |
| INFORMAL | F1-pasangan | 13 | 18 | 0,473 |
| SEMUA | F1-pasangan | 24 | 51 | 0,002 |

| Metrik | Delta-kuadrat (pp) | Selang 95% | p (tak dikoreksi) |
|---|---|---|---|
| F1-ACD | -1,78 | -7,53 s.d. 4,01 | 0,535 |
| F1-ACSA (NEGATIF) | -1,60 | -3,45 s.d. 0,00 | 0,058 |
| F1-pasangan | -4,02 | -9,86 s.d. 1,92 | 0,178 |

### Cakupan KONTROL

| Model | Metrik | F1 seluruhnya | F1 FORMAL | F1 INFORMAL | Delta-F1 (pp) | Selang 95% |
|---|---|---|---|---|---|---|
| indobert | F1-ACD | 75,50 | 77,19 | 72,36 | 4,83 | -0,94 s.d. 10,66 |
| indobert | F1-ACSA (NEGATIF) | 96,35 | 96,05 | 96,71 | -0,66 | -3,44 s.d. 2,20 |
| indobert | F1-pasangan | 74,10 | 75,84 | 70,85 | 4,99 | -1,11 s.d. 11,14 |
| indobertweet | F1-ACD | 76,71 | 78,66 | 73,05 | 5,61 | -0,03 s.d. 11,34 |
| indobertweet | F1-ACSA (NEGATIF) | 97,49 | 96,88 | 98,23 | -1,35 | -3,51 s.d. 0,77 |
| indobertweet | F1-pasangan | 75,13 | 76,24 | 73,05 | 3,19 | -2,74 s.d. 9,18 |

| Register | Metrik | b (indobert saja benar) | c (indobertweet saja benar) | p McNemar dua arah (tak dikoreksi) |
|---|---|---|---|---|
| FORMAL | F1-ACD | 47 | 57 | 0,378 |
| INFORMAL | F1-ACD | 25 | 28 | 0,784 |
| SEMUA | F1-ACD | 72 | 85 | 0,338 |
| FORMAL | F1-ACSA (NEGATIF) | 5 | 9 | 0,424 |
| INFORMAL | F1-ACSA (NEGATIF) | 2 | 8 | 0,109 |
| SEMUA | F1-ACSA (NEGATIF) | 7 | 17 | 0,064 |
| FORMAL | F1-pasangan | 49 | 55 | 0,624 |
| INFORMAL | F1-pasangan | 23 | 29 | 0,488 |
| SEMUA | F1-pasangan | 72 | 84 | 0,379 |

| Metrik | Delta-kuadrat (pp) | Selang 95% | p (tak dikoreksi) |
|---|---|---|---|
| F1-ACD | -0,78 | -5,70 s.d. 4,12 | 0,768 |
| F1-ACSA (NEGATIF) | 0,69 | -1,61 s.d. 3,01 | 0,563 |
| F1-pasangan | 1,80 | -3,48 s.d. 7,12 | 0,488 |
