# XAI-FUNGI-analysis – „Przepraszam, z kim rozmawiam?” V2

Projekt WSHOP 2026 (zima): Natalia Żuchowska, Tomasz Fela. Opiekun: dr Szymon Bobek.

**Cel:** zebranie i częściowe ujednolicenie metodologii analiz z poprzedniego semestru (warianty A–D)
oraz pomoc przy pisaniu artykułu naukowego podsumowującego te analizy, ze szczególnym uwzględnieniem
analizy dynamiki wywiadów.

Strona projektu: <https://wiki.iis.uj.edu.pl/courses:wshop:projects:2026:xaifungifin:start>
Zbiór danych XAI-FUNGI: <https://zenodo.org/records/15222484>

## Struktura repozytorium

```
analysis.ipynb                  ← notebook startowy (z repozytorium sbobek/xaifungi-analysis)
docs/
  podsumowania.md               ← podsumowania wszystkich podejść (wersja robocza raportu)
  raport_xaifungi.docx          ← raport w formacie Word
variants/
  A_klasyfikacja/               ← TF-IDF + transformery (HerBERT), klasyfikacja DE / IT / SSH
  B_minimalny_wycinek/          ← ile tekstu wystarcza do rozpoznania grupy
  C_nienadzorowane/             ← klasteryzacja, ARI / NMI
  D_dynamika_llm/               ← profile per slajd generowane przez LLM, dynamika w czasie
img/                            ← wykresy – NIE są commitowane
```

## Skąd pochodzi kod

| Wariant | Źródło | Commit |
|---|---|---|
| A | [KosmicznaBarta/xaifungi-analysis](https://github.com/KosmicznaBarta/xaifungi-analysis) | `d812e17` |
| B | [LukashWalancik/xaifungi-analysis](https://github.com/LukashWalancik/xaifungi-analysis) | `c0d4b72` |
| C | [strek-o/xaifungi-analysis](https://github.com/strek-o/xaifungi-analysis) | `7f541d0` |
| D | [AngeloNorelli/xaifungiD-analysis](https://github.com/AngeloNorelli/xaifungiD-analysis) | `4e3b0e7` |

Kod wariantów jest skopiowany bez zmian merytorycznych. Surowe dane nie są przechowywane w repozytorium.

## Plan (spotkanie 13.11.2026)

- [x] Zebranie kodu wariantów A–D w jednym repozytorium
- [x] Podsumowanie: klasyfikacja z TF-IDF
- [x] Podsumowanie: klasyfikacja z transformerami i pretrenowanymi modelami językowymi
- [x] Podsumowanie: analiza dynamiki w czasie (LLM)
- [x] Raport w formacie DOC (`docs/raport_xaifungi.docx`)
- [ ] Zamiana LLM w analizie dynamiki na model typu „decision model” (JEV) – do doprecyzowania z prowadzącym
- [ ] Ujednolicenie metodologii (wspólny podział danych i metryki) – propozycja w `docs/podsumowania.md`, sekcja 6
