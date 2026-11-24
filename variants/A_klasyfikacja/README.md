# Wariant A – klasyfikacja grupy na pełnych transkryptach

**Źródło:** fork [KosmicznaBarta/xaifungi-analysis](https://github.com/KosmicznaBarta/xaifungi-analysis), commit `d812e17` (semestr letni 2026).
**Autorzy (wg historii commitów):** Bartek Meapek, xxMegi.

Kod skopiowany bez zmian merytorycznych – zmienione są tylko nazwy plików.

| Plik | Zawartość |
|---|---|
| `analysis_tfidf.ipynb` (oryg. `analysis.ipynb`) | TF-IDF + regresja logistyczna / LinearSVM, analiza słów, LIME, klasyfikacje binarne (DE vs SSH, DE vs IT, IT vs SSH) |
| `analysis_transformers.ipynb` (oryg. `analysis_huggingface.ipynb`) | Fine-tuning HerBERT (`allegro/herbert-base-cased`) na fragmentach tekstu, GroupKFold po uczestnikach |
| `initial_preprocessing_check.ipynb` | Kontrola wstępnego przetwarzania |
| `src/preprocessing/build_initial_segments.py` | Budowa segmentów i dokumentów per uczestnik (tylko wypowiedzi uczestnika) |
| `results/tfidf_results.csv` | Wyniki F1 macro dla TF-IDF |

Dane (`transcripts/`, `data/processed/`) nie są kopiowane do tego repozytorium – pobiera się je z Zenodo
(<https://zenodo.org/records/15222484>), a pliki przetworzone tworzy `build_initial_segments.py`.

Podsumowanie wyników: [`docs/podsumowania.md`](../../docs/podsumowania.md).
