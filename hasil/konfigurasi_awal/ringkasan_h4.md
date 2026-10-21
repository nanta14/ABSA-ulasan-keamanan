# Analisis fertilitas tokenizer dan H4

Himpunan uji berpasangan. Fertilitas = jumlah token subkata dibagi jumlah kata (rangkaian huruf). Tokenizer: IndoBERT = `indolem/indobert-base-uncased`, IndoBERTweet = `indolem/indobertweet-base-uncased`.

Kemunculan kata yang tokenisasinya memuat [UNK]: IndoBERT 0,00%, IndoBERTweet 0,00%.

Sumber kelas kata:

- Kata takbaku: 3905 bentuk tunggal dari slang_formal.csv.
- Penanda aspek: 76 kata tunggal dari kata_kunci_aspek.txt; 111 entri berupa frasa tidak dipakai.
- Pembawa sentimen: 1687 kata dari sentiwords_id.txt, diperluas 833 bentuk takbaku padanan.
- Penanda aspek netral: 58 kata, yaitu penanda aspek yang tidak tercatat sebagai pembawa sentimen. Irisan kedua kelas 18 kata: awas, berantakan, berat, bocor, gangguan, korban, lambat, membingungkan, menipu, ngeri, penipu, penipuan, rahasia, rapi, spam, takut, tipu, waspada.

## Fertilitas per kelas kata

| Kelas kata | Register | IndoBERT | IndoBERTweet | Selisih (IndoBERT - IndoBERTweet) | Kemunculan kata |
|---|---|---|---|---|---|
| Seluruh kata | FORMAL | 1,066 | 1,059 | 0,008 | 21777 |
| Seluruh kata | INFORMAL | 1,181 | 1,077 | 0,103 | 21266 |
| Kata takbaku | FORMAL | 1,032 | 1,000 | 0,032 | 280 |
| Kata takbaku | INFORMAL | 1,290 | 1,020 | 0,270 | 3467 |
| Penanda aspek | FORMAL | 1,209 | 1,256 | -0,047 | 621 |
| Penanda aspek | INFORMAL | 1,424 | 1,164 | 0,260 | 635 |
| Penanda aspek netral | FORMAL | 1,289 | 1,353 | -0,064 | 450 |
| Penanda aspek netral | INFORMAL | 1,521 | 1,202 | 0,320 | 516 |
| Pembawa sentimen | FORMAL | 1,014 | 1,010 | 0,004 | 2357 |
| Pembawa sentimen | INFORMAL | 1,081 | 1,012 | 0,069 | 1939 |

Bila selisih antarmodel terpusat pada pembawa sentimen dan tidak pada penanda aspek, H3 dan H4 menunjuk ke penjelasan yang sama (Subbab 3.5.6). Karena sebagian kata kunci aspek juga kata evaluatif, perbandingan yang bersih adalah pembawa sentimen lawan penanda aspek netral.

## Fertilitas per aspek (ulasan yang aspeknya hadir)

| Aspek | Kode | Ulasan | IndoBERT baku | IndoBERT takbaku | IndoBERTweet baku | IndoBERTweet takbaku | Selisih antarmodel (takbaku) |
|---|---|---|---|---|---|---|---|
| keamanan_akun | KA | 73 | 1,060 | 1,162 | 1,059 | 1,070 | 0,093 |
| autentikasi | AU | 151 | 1,063 | 1,180 | 1,058 | 1,079 | 0,101 |
| privasi_data | PD | 35 | 1,044 | 1,155 | 1,045 | 1,067 | 0,088 |
| antarmuka | AM | 103 | 1,076 | 1,170 | 1,061 | 1,075 | 0,095 |
| keandalan | KD | 389 | 1,067 | 1,179 | 1,061 | 1,078 | 0,101 |

## Korelasi Spearman (EKSPLORATORI, di luar koreksi Holm)

Lima titik per korelasi; angka p eksak dari 120 permutasi. Dengan lima titik, angka p dua arah terkecil yang mungkin adalah 0,017 (urutan sempurna), sehingga koefisien diperlakukan sebagai penunjuk arah, bukan bukti sebab-akibat (Subbab 3.5.5 dan 3.5.6).

| Analisis | Model | Metrik | rho | p eksak | Keterangan |
|---|---|---|---|---|---|
| H4: selisih fertilitas antarmodel lawan Delta-kuadrat | indobert - indobertweet | ACD | 0,60 | 0,350 |  |
| Diagram pencar: fertilitas versi takbaku lawan Delta-F1 | indobert | ACD | 0,30 | 0,683 |  |
| Diagram pencar: fertilitas versi takbaku lawan Delta-F1 | indobertweet | ACD | -0,60 | 0,350 |  |
| H4: selisih fertilitas antarmodel lawan Delta-kuadrat | indobert - indobertweet | ACSA | 0,22 | 1,000 |  |
| Diagram pencar: fertilitas versi takbaku lawan Delta-F1 | indobert | ACSA | 0,22 | 1,000 |  |
| Diagram pencar: fertilitas versi takbaku lawan Delta-F1 | indobertweet | ACSA | - | - | tidak terdefinisi: salah satu peubah konstan |
| H4: selisih fertilitas antarmodel lawan Delta-kuadrat | indobert - indobertweet | PASANGAN | 0,60 | 0,350 |  |
| Diagram pencar: fertilitas versi takbaku lawan Delta-F1 | indobert | PASANGAN | 0,30 | 0,683 |  |
| Diagram pencar: fertilitas versi takbaku lawan Delta-F1 | indobertweet | PASANGAN | -0,60 | 0,350 |  |

### Urutan aspek (H4)

| Metrik | Urutan menurut selisih fertilitas | Urutan menurut Delta-kuadrat |
|---|---|---|
| ACD | autentikasi > keandalan > antarmuka > keamanan_akun > privasi_data | antarmuka > keandalan > autentikasi > keamanan_akun > privasi_data |
| ACSA | autentikasi > keandalan > antarmuka > keamanan_akun > privasi_data | antarmuka > privasi_data > autentikasi > keandalan > keamanan_akun |
| PASANGAN | autentikasi > keandalan > antarmuka > keamanan_akun > privasi_data | antarmuka > keandalan > autentikasi > keamanan_akun > privasi_data |

Gambar: `gambar_h4_pencar.png` (tiga panel, sumbu tegak disamakan) dan `gambar_fertilitas_kelas_kata.png` (diagram batang berkelompok). Kode aspek: KA = keamanan_akun, AU = autentikasi, PD = privasi_data, AM = antarmuka, KD = keandalan.
