# Wariant C – nienadzorowana struktura grup

**Źródło:** fork [strek-o/xaifungi-analysis](https://github.com/strek-o/xaifungi-analysis), commit `7f541d0`.
**Autor:** strek-o.

Klasteryzacja (KMeans) uczestników na cechach lingwistycznych, TF-IDF + SVD (LSA), cechach behawioralnych
i kodach MAXQDA; ocena zgodności z grupami DE/IT/SSH przez ARI i NMI.

| Plik | Zawartość |
|---|---|
| `analysis.ipynb` | Cała analiza z wnioskami |
| `src/dataset.py` | Pobieranie zbioru z Zenodo |
| `src/transcripts.py` | Wczytywanie i filtrowanie transkryptów |
| `src/features.py` | Cechy lingwistyczne, TF-IDF + SVD, cechy slajdów |
| `src/responses.py` | Cechy behawioralne (decyzje w zadaniach, pewność) |
| `src/maxqda.py` | Kody tematyczne MAXQDA |

Podsumowanie wyników: [`docs/podsumowania.md`](../../docs/podsumowania.md).
