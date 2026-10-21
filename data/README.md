# Data

The four split files used in the study (3,258 Google Play reviews in total, plus the 573 formal normalizations). Person
names inside the review text have been masked (see below).

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

## What was removed or masked

- **At collection:** user names, profile images, and review identifiers were discarded and never stored.
  Star ratings and application names are kept outside this repository, so a review cannot be linked to an app here.
- **Before release:** person names that users wrote inside the review text (their own name, a third party's name, a
  staff member's name, a payee account name) were replaced with `[NAMA]`, and one personal referral code with `[KODE]`.
  Candidates were found automatically (address terms such as *pak*, *bu*, *cs*, *atas nama*, *bernama*, plus rare
  capitalized words and a list of common Indonesian first names) and every candidate was checked by hand. In total 22
  spans in 18 reviews were masked, identically in the INFORMAL and FORMAL version of a pair. Names of applications,
  banks, places, and virtual assistants (e.g. *Diana*, *Aisyah*) and of public officials were left as they are.
- A pattern scan found no e-mail addresses and no digit runs as long as a phone or account number (longest run: 8
  digits).

All labels and all other columns are unchanged. The results reported in the thesis and article were computed on the
text **before** masking; the 22 masked spans are the only difference, so rerunning the scripts on these files may give
numbers that differ slightly from the reported ones, and the SHA-256 hashes in the original run logs will not match.

SHA-256 of the released files (release v1.0):

```
b8a48527f3d113c37490d56fcf1a266f5be268bd32686d59bb3673b1d7498da6  latih.csv
7d52e7b01bdff9d7197c6a72b99fbe6c856cd5458ab7436acefd7a8a6013ae38  pengembangan.csv
abe8674c153255072a43fb878841512fc4c7848f8bf6e4c40a74c6b68152e01e  uji_takberpasangan.csv
8efe48fcdd2f10908228dc80d05b0ef9db6bd49ee81ac0109e20380cf355c028  uji_berpasangan.csv
```

## Terms of use

The review texts were written by Google Play users and are shared here **for non-commercial research only**, under
[CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) for the annotations and normalizations. Do not try to
re-identify the authors of the reviews. If you find personal data that was missed, or you wrote one of these reviews and
want it removed, please open an issue or contact the author; the item will be removed in the next release.
