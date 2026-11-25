# XAI-FUNGI – podsumowanie podejść z semestru letniego 2026

*Wersja robocza, 20.11.2026, aktualizacja 25.11.2026 (sekcje 3 i 7). Przygotowane na podstawie notebooków wariantów A–D (katalog `variants/`).*

Wszystkie liczby pochodzą z zapisanych wyników w notebookach autorów. Liczby oznaczone jako
**[weryfikacja V2]** policzyliśmy sami w ramach tego projektu, na danych i kodzie z repozytoriów wariantów
(skrypt: `docs/weryfikacja_v2.py`).

## 0. Dane i zadanie

- Zbiór XAI-FUNGI (Zenodo, rekord 15222484): transkrypcje wywiadów, w których uczestnicy na głos analizują
  wizualizacje wyjaśnień modelu klasyfikującego grzyby.
- Grupy: **DE** – eksperci dziedzinowi (mykolodzy), **IT** – studenci informatyki, **SSH** – studenci kierunków
  społeczno-humanistycznych.
- 39 uczestników (13 DE, 8 IT, 18 SSH) w 38 plikach CSV – jeden plik (`PK_DE_11-12`) zawiera dwóch ekspertów.
  Dlatego część analiz raportuje N = 39, a część N = 38 (z 12 DE).
- Zadanie: na podstawie wypowiedzi przewidzieć grupę uczestnika (warianty A, B), zbadać naturalną strukturę grup
  bez etykiet (C) albo opisać przebieg wywiadu w czasie (D).
- Mały zbiór (39 osób, tylko 8 w grupie IT) oznacza, że wyniki mają duży rozrzut między podziałami danych.

## 1. Klasyfikacja z wykorzystaniem TF-IDF

### Wariant A – pełne transkrypty (`variants/A_klasyfikacja/analysis_tfidf.ipynb`)

**Metoda.** Jeden dokument na uczestnika – tylko wypowiedzi uczestnika (bez badacza), z dopisanymi znacznikami
kontekstu `[SLIDE=…] [QUESTION=…] [PROBLEM=…]`. TF-IDF (unigramy i bigramy, maks. 5000 cech, `min_df=2`,
`max_df=0.8`, własna lista stop-słów), regresja logistyczna lub LinearSVM z `class_weight="balanced"`.
Ewaluacja: StratifiedKFold, 3 foldy, `random_state=42`, metryka F1 macro.

**Wyniki (3 klasy).**

| Model | F1 macro (średnia ± odch. std z 3 foldów) |
|---|---|
| TF-IDF + regresja logistyczna | 0,730 ± 0,092 |
| TF-IDF + LinearSVM | 0,709 ± 0,122 |

Poprawnie sklasyfikowani uczestnicy (regresja logistyczna, 3-fold): DE 12/13, IT 2/8, SSH 18/18.
Grupa IT jest niemal zawsze mylona z SSH.

**Klasyfikacja binarna** (ten sam pipeline, regresja logistyczna, 3-fold, F1 macro):

| Para | F1 macro | Uwagi |
|---|---|---|
| DE vs SSH | 0,889 | recall DE 0,77, SSH 1,00 |
| DE vs IT | 0,883 | recall DE 0,92, IT 0,88 |
| IT vs SSH | 0,624 | recall IT tylko 0,25 |
| DE vs reszta | 0,783 | recall DE 0,54 |

**Interpretacja (wagi modelu, LIME).** Dla DE ważne są słowa związane z wiedzą dziedzinową („gatunki”, „gatunek”),
ale też słowa takie jak „natomiast”, „oczywiście” oraz tag transkrypcji „[śmiech]”. Dla IT najsilniejsze cechy to
„jeżeli”, „faktycznie”, „ai” – i tag „[niewyraźne]”. Część cech to więc artefakty sposobu transkrypcji,
a nie języka uczestników.

### Wariant B – TF-IDF na odpowiedziach na pytania (`variants/B_minimalny_wycinek/analysis.ipynb`)

**Metoda.** Jednostką jest odpowiedź uczestnika na jedno pytanie badacza (ok. 550 fragmentów). Losowy podział
80/20 (`train_test_split`, stratyfikacja po grupie), TF-IDF + regresja logistyczna.

| Konfiguracja | Accuracy | F1 macro |
|---|---|---|
| Bazowa (1000 cech) | 0,75 | 0,68 |
| + `class_weight="balanced"` | 0,71 | 0,67 |
| + `class_weight` + regularyzacja L1 | 0,78 | 0,76 |
| Bigramy / `min_df=3` / `max_df=0.85` | 0,75–0,77 | 0,73–0,75 |

**Ważne zastrzeżenie.** Podział jest losowy na poziomie fragmentów, a nie uczestników – odpowiedzi tej samej
osoby trafiają jednocześnie do zbioru treningowego i testowego. Model może więc rozpoznawać konkretną osobę,
a nie grupę. Wyniki B nie są bezpośrednio porównywalne z A.

### [weryfikacja V2] Stabilność wyniku A

Uruchomiliśmy ponownie pipeline TF-IDF + regresja logistyczna z wariantu A na tych samych danych
(`data/processed/participant_documents.csv`). Wynik 0,730 odtwarza się dokładnie, ale zależy od jednego
konkretnego podziału na foldy:

| Wariant danych wejściowych | F1 macro, 3-fold, seed 42 | F1 macro, 10 × 3-fold (powtórzone) |
|---|---|---|
| Oryginalne dokumenty (ze znacznikami) | 0,730 ± 0,092 | 0,649 ± 0,116 |
| Bez znaczników `[SLIDE/QUESTION/PROBLEM]` | 0,709 ± 0,122 | 0,643 ± 0,119 |
| Bez znaczników i bez tagów transkrypcji (`[śmiech]`, `[niewyraźne]`…) | 0,770 ± 0,037 | 0,687 ± 0,119 |

Wnioski: realistyczna wartość F1 macro to ok. **0,65–0,69**, a nie 0,73. Usunięcie znaczników nie obniża wyniku,
czyli DE nie jest rozpoznawane wyłącznie po znacznikach slajdów. Usunięcie tagów transkrypcji lekko poprawia wynik.

### Wnioski dla TF-IDF

- TF-IDF dobrze odróżnia ekspertów od studentów (DE vs SSH i DE vs IT: F1 ≈ 0,88).
- Rozróżnienie IT od SSH jest słabe (F1 0,62, recall IT 0,25) – to główny problem wszystkich podejść.
- Wszyscy eksperci DE byli przepytywani przez tę samą osobę (prefiks `PK`), a studenci przez czterech innych
  badaczy. Różnice w stylu transkrypcji i prowadzenia wywiadu mogą więc częściowo „przeciekać” do klasyfikatora.
  Tego nie da się w pełni rozdzielić na tych danych i trzeba to opisać jako ograniczenie w artykule.

## 2. Klasyfikacja z wykorzystaniem transformerów i pretrenowanych modeli językowych

### Wariant A – fine-tuning HerBERT (`variants/A_klasyfikacja/analysis_transformers.ipynb`)

**Metoda.** Model `allegro/herbert-base-cased`. Wypowiedzi uczestnika dzielone na fragmenty po 128 słów
z zakładką 32 słów (2014 fragmentów), `max_length=256` tokenów. Fine-tuning klasyfikatora sekwencji
z ważoną funkcją straty (wagi klas „balanced”), 5 epok, learning rate 2e-5, batch 8.
Ewaluacja: GroupKFold (3 foldy) z grupowaniem po uczestniku – fragmenty jednej osoby nie trafiają jednocześnie
do treningu i testu. Etykieta uczestnika = najczęstsza etykieta jego fragmentów (głosowanie większościowe).

**Wyniki.**

| Poziom | Wynik |
|---|---|
| Uczestnicy – accuracy | 79,5% (31/39) |
| Uczestnicy – F1 macro | 0,67 |
| Uczestnicy – poprawnie per grupa | DE 13/13, SSH 17/18, IT 1/8 |
| Fragmenty – accuracy per grupa | DE 94,3%, SSH 77,3%, IT 27,7% |
| Fragmenty – accuracy łącznie [weryfikacja V2] | ok. 68,8% |

Uwaga: w notebooku wartość 79,49% jest opisana jako „CHUNK ACCURACY”, ale jest to accuracy na poziomie
uczestników. Łączną accuracy fragmentów policzyliśmy z wyników per grupa.

**Zastrzeżenia metodologiczne.**

- Zbiorem walidacyjnym w treningu jest fold testowy, a włączone jest `load_best_model_at_end=True`. Najlepsza
  epoka jest więc wybierana na danych testowych, co lekko zawyża wynik. Potrzebny osobny zbiór walidacyjny.
- W logach pojawia się ostrzeżenie o brakujących wagach LayerNorm przy wczytywaniu najlepszego checkpointu
  (biblioteka `transformers` 5.x). Warto sprawdzić, czy ewaluacja na pewno odbywa się na poprawnie wczytanym modelu.

### Wariant B – fine-tuning HerBERT na odpowiedziach na pytania

Podział GroupShuffleSplit 80/20 po uczestnikach. Wynik na zbiorze walidacyjnym: accuracy 0,70,
F1 macro 0,50, F1 dla IT = 0,0 (model nie rozpoznał żadnego studenta IT).

### Wnioski dla transformerów

- HerBERT nie poprawia wyników względem TF-IDF: F1 macro 0,67 vs 0,65–0,73 dla TF-IDF.
- Wzorzec błędów jest identyczny: DE prawie bezbłędnie, IT prawie zawsze jako SSH.
- Przy 39 uczestnikach przewaga dużych modeli jest ograniczona. Sensowną kolejną próbą są embeddingi zdań bez
  fine-tuningu (np. `paraphrase-multilingual-MiniLM-L12-v2`, którego wariant B używał do eksploracji)
  + prosty klasyfikator, oceniane tym samym protokołem co TF-IDF.

## 3. Analiza dynamiki w czasie (podejście z wielkimi modelami językowymi)

### Wariant D (`variants/D_dynamika_llm/`)

**Metoda.** Wypowiedzi uczestnika grupowane są per slajd (`TranscriptParser`, ok. 1781 rekordów).
Lokalny LLM uruchamiany przez Ollama – w kodzie domyślnie `qwen3.5:9b`, temperatura 0,7
(README w jednym miejscu podaje `qwen3:5b`; nie wiadomo, którym modelem wygenerowano zapisane wyniki) na każdym slajdzie zwraca w JSON trzy oceny w skali 0–1:

- `engagement_level` – zaangażowanie,
- `confidence_level` – pewność siebie,
- `communication_style` – techniczność / formalność wypowiedzi.

Z ocen powstają wykresy przebiegu wywiadu slajd po slajdzie. Moduł `XAIExplanation` prosi LLM o słowne
wyjaśnienie zmian między kolejnymi slajdami (z cytatami z transkryptu). `Plot.py` liczy korelację przebiegów
jednego uczestnika z pozostałymi i rysuje wykres 3D.

**Co zostało zrobione.** Działający pipeline, zapisane oceny dla 31 z 38 uczestników (`llm_responses.json`),
wariant z oceną wszystkich slajdów naraz (`llm_responses_all_slide_at_once.json`), przykładowe wyjaśnienia.
Autorzy nie przeprowadzili ilościowej oceny, czy profile różnią się między grupami ani czy oceny LLM są wiarygodne.
Ten etap był zaplanowany jako następny na spotkaniu 14.04.

### [weryfikacja V2] Czy profile LLM odróżniają grupy?

Na podstawie `llm_responses.json`:

- Oceny są dostępne dla **31 z 38** uczestników (500 ocen slajdów). Brakuje wszystkich 7 wywiadów
  prowadzonych przez badacza DR (`DR_IT_05`, `DR_SSH_01`–`04`, `DR_SSH_06`–`07`): parser wariantu D
  (`TranscriptParser`) nie wyodrębnił z nich żadnego slajdu, więc LLM nie dostał tych danych.
  W efekcie analiza dynamiki obejmuje tylko 12 z 18 osób z grupy SSH i 7 z 8 z grupy IT.
- Średnie ocen w grupach:

| Grupa | engagement | confidence | communication |
|---|---|---|---|
| DE | 0,797 | 0,659 | 0,707 |
| IT | 0,788 | 0,534 | 0,660 |
| SSH | 0,784 | 0,560 | 0,678 |

- Jedyna widoczna różnica: eksperci mają wyższą ocenianą pewność siebie (0,66 vs 0,53–0,56).
- Klasyfikator (regresja logistyczna, StratifiedKFold 3) na średniej i odchyleniu standardowym trzech ocen
  per uczestnik osiąga **F1 macro 0,32**, czyli poziom losowy (ok. 0,33 dla trzech klas).

### Wnioski dla dynamiki

- Pipeline daje czytelne, interpretowalne przebiegi pojedynczych wywiadów, ale w obecnej postaci profile LLM
  prawie nie niosą informacji o grupie uczestnika.
- Oceny są niedeterministyczne (temperatura 0,7), bez walidacji z oceną człowieka, a część odpowiedzi jest
  niepoprawna formalnie.
- To argument za planowaną zamianą generatywnego LLM na model, który nie generuje tekstu, tylko zwraca
  stabilną reprezentację lub decyzję (punkt „decision model” / JEV) – patrz sekcja 6.

## 4. Wariant B – minimalny wycinek rozmowy

Pytanie: ile wypowiedzi wystarczy, żeby rozpoznać grupę? Model TF-IDF + regresja logistyczna trenowany na pełnych
odpowiedziach, testowany na odpowiedziach obciętych do części słów (F1 ważone, nie macro):

| Część wypowiedzi | 10% | 20% | 30% | 40% | 50% | 60% | 75% | 100% |
|---|---|---|---|---|---|---|---|---|
| Podział na pytania | 0,577 | 0,586 | 0,653 | 0,699 | 0,698 | 0,736 | 0,772 | 0,750 |
| Podział na slajdy | 0,576 | 0,651 | 0,705 | 0,699 | 0,692 | 0,722 | 0,708 | 0,758 |
| Podział na zdania | 0,456 | 0,478 | 0,483 | 0,492 | 0,495 | 0,512 | 0,526 | 0,537 |

Z tabeli wynika, że już ok. 60% odpowiedzi daje wynik bliski pełnemu tekstowi, a pojedyncze zdania są za krótkie
do rozpoznania grupy.
Najlepiej rozróżniają grupy odpowiedzi na pytania Q3, Q13, Q16, ale liczebności są bardzo małe (3–12 fragmentów
na pytanie), więc ranking pytań nie jest wiarygodny. Te same zastrzeżenia co w sekcji 1: losowy podział
fragmentów (przeciek uczestnika) i F1 ważone zamiast macro.

## 5. Wariant C – nienadzorowana struktura grup

KMeans na różnych zestawach cech, zgodność klastrów z grupami mierzona ARI i NMI (N = 38):

| Cechy | ARI | NMI |
|---|---|---|
| 6 prostych cech lingwistycznych | 0,144 | 0,204 |
| TF-IDF + SVD (15 wymiarów) | 0,443 | 0,540 |
| Proste cechy + TF-IDF | 0,169 | 0,227 |
| Kody tematyczne MAXQDA | 0,468 | 0,598 |
| MAXQDA, k = 2 | 0,604 | 0,747 |

Wnioski:

- Naturalna struktura danych to **dwie grupy: eksperci vs studenci**. Przy k = 2 na kodach MAXQDA podział jest
  idealny (12/12 DE w jednym klastrze, żadnego studenta).
- IT i SSH nie rozdzielają się żadnym zestawem cech (ARI ok. 0 również z cechami behawioralnymi).
- Ważne odkrycie o danych: tagowanie `slide_id` jest skrajnie asymetryczne. U ekspertów bez przypisanego slajdu
  jest 29% słów, u studentów ok. 96%. Każda cecha zbudowana na `slide_id` staje się więc ukrytym detektorem DE.

## 6. Wnioski wspólne i propozycja ujednolicenia metodologii

**Spójne wyniki ze wszystkich wariantów:**

1. Eksperta da się odróżnić od studenta (TF-IDF, HerBERT i klasteryzacja zgodnie).
2. Studentów IT i SSH nie da się wiarygodnie rozróżnić na podstawie samych wypowiedzi.
3. Bardziej złożone modele (HerBERT, LLM) nie poprawiają wyników względem TF-IDF.

**Problemy do naprawienia przy ujednolicaniu:**

- Różne podziały danych (losowo per fragment w B, per uczestnik w A) i różne metryki (F1 macro vs ważone,
  accuracy). Wyników nie da się bezpośrednio porównać.
- Jedno ziarno losowości przy 3 foldach daje wynik o ±0,1 – za mało stabilne do artykułu.
- Wybór epoki na zbiorze testowym (HerBERT).
- Czynniki zakłócające: badacz `PK` = wszyscy DE; asymetryczne tagowanie slajdów; tagi transkrypcji.
- Różne N (38 vs 39).

**Proponowany wspólny protokół:**

- Jednostka oceny: uczestnik. Podział zawsze grupowany po uczestniku (StratifiedGroupKFold albo
  leave-one-participant-out), powtórzony co najmniej 10 razy z różnymi ziarnami.
- Metryki: F1 macro (główna), recall per grupa, macierz pomyłek; wynik jako średnia ± odchylenie std.
- Trzy zadania raportowane osobno: DE / IT / SSH, DE vs studenci, IT vs SSH.
- Wspólne czyszczenie tekstu: tylko wypowiedzi uczestnika, usunięte znaczniki kontekstu i tagi transkrypcji.
- Model dobierany na osobnym zbiorze walidacyjnym wewnątrz treningu.
- N = 39 (rozdzielenie pliku `PK_DE_11-12` na dwóch uczestników, jak w wariancie A).

**Zamiana LLM na „decision model” (JEV) w analizie dynamiki** – w toku, opis w sekcji 7.

## 7. Analiza dynamiki z modelem JEV (V2, w toku)

Kod: `variants/D_jev/analysis.ipynb` (gałąź `testAddJevModel`).

**Model.** JEV (`jev-1.13-free`) udostępniany przez API opencode.ai. W przeciwieństwie do generatywnego LLM
z wariantu D nie zwraca wolnego tekstu, tylko dla każdego zadanego pytania: ocenę na zadanej skali,
pewność odpowiedzi i rozkład prawdopodobieństwa nad kategoriami. Odpowiedź ma zawsze poprawną strukturę,
więc odpada problem niepoprawnego JSON-a.

**Metoda.** Te same jednostki co w wariancie D (wypowiedzi uczestnika na jednym slajdzie, `parsed_transcripts.jsonl`)
i te same trzy wymiary, ale w skali 0–2 z opisanymi kategoriami:

| Wymiar | 0 | 1 | 2 |
|---|---|---|---|
| `engagement_level` | niskie zaangażowanie | umiarkowane | wysokie |
| `confidence_level` | niska wyrażana pewność | umiarkowana | wysoka |
| `communication_style` | zwięzły, bezpośredni | zrównoważony | rozbudowany, refleksyjny |

Wynik zapisywany jest jako ocena (średnia ważona prawdopodobieństwami, 0–2), ocena znormalizowana (0–1),
pewność modelu i pełny rozkład prawdopodobieństw.

**Poprawka danych wejściowych.** `parsed_transcripts.jsonl` zawiera 1781 rekordów, z czego 849 to wypowiedzi
badaczy (`PK`, `MW`, `MK`, `MZ`), a nie uczestników. Pierwsze uruchomienia oceniały również je.
Notebook filtruje teraz rekordy do 932 rekordów 32 uczestników, a oceny badaczy zostały usunięte z wyników.

**Stan na 25.11.2026.** Pilotaż na 51 rekordach (4 uczestników: `MK_IT_03`, `MK_IT_06`, `MK_SSH_02`, `MK_SSH_04`)
z 932. Zapytania wykonywane są partiami po 20, z zapisem po każdym rekordzie.

**Następne kroki.**

1. Ocenić wszystkie 932 rekordy.
2. Porównać JEV z LLM z wariantu D na tych samych slajdach (zgodność ocen, stabilność przy powtórzeniu zapytania).
3. Powtórzyć test z sekcji 3: czy profile JEV odróżniają grupy DE / IT / SSH (dla LLM: F1 macro 0,32 – poziom losowy).
4. Naprawić parser dla 7 wywiadów DR, żeby objąć wszystkich 39 uczestników.
5. Wykorzystać `XAIExplanation` i `Plot` z wariantu D na wynikach JEV.

**Uwaga.** Transkrypty są wysyłane do zewnętrznego API. Zbiór XAI-FUNGI jest publiczny (Zenodo),
ale warto potwierdzić z prowadzącym, że takie użycie jest w porządku na potrzeby artykułu.

