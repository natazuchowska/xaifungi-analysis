# Wariant D + JEV – analiza dynamiki z modelem decyzyjnym

Zamiana generatywnego LLM z wariantu D (`variants/D_dynamika_llm/`) na model decyzyjny **JEV**
(`jev-1.13-free`, API opencode.ai), zgodnie z planem ze spotkania 13.11.2026.

## Jak uruchomić

1. W tym folderze utwórz plik `.env` z linią `OPENCODE_API_KEY=...` (plik jest w `.gitignore`).
2. `pip install requests python-dotenv`
3. Otwórz `analysis.ipynb` i uruchamiaj sekcje po kolei. Sekcja 5 ocenia kolejną partię
   (domyślnie 20 rekordów); można ją uruchamiać wielokrotnie – rekordy już ocenione są pomijane.

## Pliki

| Plik | Zawartość |
|---|---|
| `analysis.ipynb` | Notebook z całym procesem (konfiguracja, filtr uczestników, zapytania do JEV, kontrola jakości) |
| `parsed_transcripts.jsonl` | Dane wejściowe – wypowiedzi per slajd z wariantu D (zawierają też badaczy, filtrowane w notebooku) |
| `jev_results.jsonl` | Wyniki JEV: jeden wiersz = uczestnik × slajd |
| `jev_errors.jsonl` | Błędy zapytań (tworzony automatycznie, jeśli wystąpią) |
| `jev_results_backup.jsonl` | Kopia wyników sprzed filtrowania (zawiera też oceny badacza – nie używać do analizy) |
| `jev_pilot.json` | Wynik pierwszego testowego zapytania |
| `src/`, `llm_responses*.json`, `correlation_3d.html` | Kopia kodu i wyników wariantu D do późniejszego porównania |

## Ograniczenia

- `parsed_transcripts.jsonl` nie zawiera 7 wywiadów prowadzonych przez badacza DR – analizą objętych jest 32 z 39 uczestników.
- Transkrypty są wysyłane do zewnętrznego API.

Szczegóły i wyniki: [`docs/podsumowania.md`](../../docs/podsumowania.md), sekcja 7.
