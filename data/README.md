# Data

The review texts are not stored in this repository (see the main README). Place the split files here with the names
below to run the scripts.

| File | Rows | Content |
|---|---|---|
| `latih.csv` | 1,650 | training set (1,006 FORMAL, 644 INFORMAL) |
| `pengembangan.csv` | 291 | development set |
| `uji_takberpasangan.csv` | 744 | unpaired test set, annotated without model suggestions |
| `uji_berpasangan.csv` | 1,146 | paired test set: 573 reviews × {INFORMAL original, FORMAL normalization} |

## Columns

`latih.csv`, `pengembangan.csv`, `uji_takberpasangan.csv`

| Column | Meaning |
|---|---|
| `id_ulasan` | internal review id (e.g. `R00943`); not a Google Play id |
| `teks` | review text |
| `asp_keamanan_akun`, `asp_autentikasi`, `asp_privasi_data`, `asp_antarmuka`, `asp_keandalan` | `TIDAK_ADA`, `NEGATIF`, or `POSITIF` |
| `sumber` | annotation package the label came from |
| `metode_anotasi` | with or without model suggestions |
| `peran_pembagian` | role in the split |

`uji_berpasangan.csv`

| Column | Meaning |
|---|---|
| `id_ulasan` | shared by both versions of a pair |
| `id_butir` | `<id>_INF` or `<id>_FOR` |
| `register` | `INFORMAL` (original) or `FORMAL` (manual normalization) |
| `teks` | review text |
| five aspect columns | identical labels for both versions |
| `skor_informalitas` | informality score of the original informal review |
| `sumber` | annotation package |

Register rule: INFORMAL if the share of words found in the colloquial lexicon is above 0.20 or the review contains at
least three such words.
