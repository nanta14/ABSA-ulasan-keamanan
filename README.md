# Register Robustness of IndoBERT and IndoBERTweet in Security-Aspect Sentiment Analysis

Annotated data, code, annotation resources, and aggregate results for the study **"Evaluating the Robustness of IndoBERT and
IndoBERTweet to Informal Register in Security-Aspect Sentiment Analysis of Indonesian Digital Finance App Reviews"**
(master's thesis, Master of Information Technology, Faculty of Science and Technology, Universitas Islam Negeri Syarif
Hidayatullah Jakarta, 2026; journal article under review).

*Ringkasan dalam bahasa Indonesia ada di bagian akhir.*

## What the study does

Indonesian app reviews are written in a formal and an informal register, and security complaints are more often
informal. The study builds a **paired test set**: 573 naturally informal Google Play reviews of digital finance
applications, each with a manually normalized formal version that keeps the meaning and the gold labels identical.
IndoBERT (`indolem/indobert-base-uncased`) and IndoBERTweet (`indolem/indobertweet-base-uncased`) are fine-tuned under
identical conditions and evaluated on both versions for

- **ACD** – aspect category detection (F1 of the PRESENT class),
- **ACSA** – aspect polarity on gold-present items (F1 of the NEGATIVE class),
- **F1-pair** – category and polarity both correct (primary metric),

over five aspect categories: three security aspects (account security, authentication, data privacy) and two control
aspects (interface, reliability).

Main findings (seed 42, paired test set, pooled categories): the formal-minus-informal difference ΔF1 ranged from
−0.29 to 1.36 percentage points and none of the four hypotheses was supported; IndoBERTweet scored about four F1-pair
points higher on both registers (five-seed mean); 45.7–62.9 % of data-privacy complaints were missed in both registers.
Full tables are in [`hasil/`](hasil/).

## Repository structure

```
skrip/                       scripts (Python) and unit tests
  latih_prediksi.py          fine-tuning with five 3-way heads; writes per-item raw predictions
  cari_hiperparameter.py     exhaustive 18-combination search on the development set
  evaluasi_statistik.py      all metrics and tests from the per-item predictions
                             (exact McNemar, review-level cluster bootstrap, Holm per family)
  rangkum_benih.py           seed sensitivity analysis (seeds 42–46)
  analisis_fertilitas.py     tokenizer fertility by word class and the H4 correlation
  test_*.py                  33 pytest cases (run without a GPU)
sumber_daya/
  kata_kunci_aspek.txt       187 aspect keywords/phrases used to draw candidate reviews
  lampiran_kata_kunci_aspek.csv   same list with aspect code and type
hasil/
  ringkasan_pencarian.md     hyperparameter search (selected: lr 5e-5, batch 16, 3 epochs)
  utama/                     results with the selected configuration (used in the paper)
  konfigurasi_awal/          results with the initial configuration (lr 2e-5, batch 16, 4 epochs), sensitivity only
data/                        the four annotated splits (person names masked)
  latih.csv  pengembangan.csv  uji_takberpasangan.csv  uji_berpasangan.csv
  README.md                  schema, masking procedure, hashes, terms of use
```

## Data availability

The annotated corpus is included in [`data/`](data/): 3,258 reviews labelled for five aspect categories and for
register, split into training, development, and unpaired test sets, plus the paired test set of 573 informal reviews
with their formal normalizations. Person names written inside the review text were masked before release (22 spans in
18 reviews); user names, profile images, and review identifiers were discarded at collection, and star ratings and
application names are not included. Details are in [`data/README.md`](data/README.md). The data are for
non-commercial research only.

The reported results were computed on the text before masking, which differs from the released text only in the masked
spans. The annotation guideline and the per-item predictions are available from the author on request.

The colloquial lexicon used for the informality score is not redistributed here; use the original resource of
Salsabila et al. (2018), *Colloquial Indonesian Lexicon* (IALP 2018).

## Reproducing the analysis

Tested with Python 3.13, PyTorch 2.11.0, Transformers 5.18.0, NumPy 2.1.3, and pandas 2.2.3 (training on an NVIDIA
Tesla T4, Google Colab).

```bash
pip install -r requirements.txt
cd skrip
python -m pytest -q                                   # 33 unit tests, no GPU needed

# 1) check schema, leakage gate, label distribution, and truncation (no training)
python latih_prediksi.py --data-dir ../data --keluaran-dir keluaran --periksa

# 2) hyperparameter search on the development set
python cari_hiperparameter.py --data-dir ../data --keluaran-dir keluaran_pencarian --acuan-dir keluaran

# 3) fine-tune both models with the selected configuration (seed 42, then 43–46)
python latih_prediksi.py --data-dir ../data --keluaran-dir keluaran --laju-belajar 5e-5 --ukuran-tumpukan 16 --epoch 3
python latih_prediksi.py --data-dir ../data --keluaran-dir keluaran --laju-belajar 5e-5 --ukuran-tumpukan 16 --epoch 3 --benih 43

# 4) metrics and hypothesis tests from the saved predictions
python evaluasi_statistik.py --prediksi-dir keluaran/prediksi --hasil-dir keluaran/hasil
python evaluasi_statistik.py --prediksi-dir keluaran/prediksi --hasil-dir keluaran/hasil_tanpa_terpotong --tanpa-terpotong
python rangkum_benih.py --prediksi-dir keluaran/prediksi --hasil-dir keluaran/hasil_benih --selisih-utama keluaran/hasil/selisih.csv

# 5) tokenizer fertility and H4
python analisis_fertilitas.py --pasangan ../data/uji_berpasangan.csv --selisih keluaran/hasil/selisih.csv \
       --hasil-dir keluaran/hasil_fertilitas --leksikon-takbaku <colloquial-lexicon.csv> \
       --kata-aspek ../sumber_daya/kata_kunci_aspek.txt --leksikon-sentimen <positive.txt> <negative.txt>
```

Without arguments, `latih_prediksi.py` uses the initial configuration (2e-5, 16, 4 epochs); the paper reports the
selected configuration (5e-5, 16, 3 epochs). Each run writes a log with SHA-256 hashes of the data files, and training
is aborted if the leakage gate fails (no paired review may appear in training or development data).

## Annotation

Three annotators labelled each review for the five categories with ABSENT, POSITIVE, or NEGATIVE. Reliability was
measured on 900 reviews annotated without model suggestions (mean Fleiss' κ = 0.85). The remaining reviews were
annotated singly with label suggestions from Gemini 3.1 Flash Lite (Google), all reviewed by a human annotator. The
unpaired test set and 156 of the 573 pairs were annotated without suggestions.

## Licence

Code in `skrip/` is released under the MIT License (see [`LICENSE`](LICENSE)). The annotations and normalizations in
`data/`, documentation, keyword lists, and result summaries are released under
[CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/); the review texts themselves were written by Google Play
users and are shared for non-commercial research only (see [`data/README.md`](data/README.md#terms-of-use)).

## Citation

If you use this repository, please cite the thesis (and the article once published):

```
M. L. Septipalan, "Evaluasi Ketahanan Register IndoBERT dan IndoBERTweet pada Analisis Sentimen Aspek Keamanan
Aplikasi Keuangan Digital," Master's thesis, Universitas Islam Negeri Syarif Hidayatullah Jakarta, 2026.
```

## Ringkasan (Bahasa Indonesia)

Repositori ini memuat korpus beranotasi, skrip, daftar kata kunci, dan ringkasan hasil tesis *Evaluasi Ketahanan
Register IndoBERT dan IndoBERTweet pada Analisis Sentimen Aspek Keamanan Aplikasi Keuangan Digital*. Folder `data/`
berisi 3.258 ulasan berlabel lima kategori aspek dan register beserta 573 pasang teks takbaku–baku. Nama orang di dalam
teks sudah disamarkan menjadi `[NAMA]` (22 penggalan pada 18 ulasan), dan data hanya untuk keperluan penelitian
nonkomersial. Pedoman anotasi dan prediksi per butir tersedia atas permintaan kepada penulis. Pembimbing: Ir. Nashrul Hakiem, S.Si., M.T., Ph.D. dan Khodijah Hulliyah, S.Kom.,
M.Si., Ph.D.
