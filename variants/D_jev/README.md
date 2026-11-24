# Wariant D – profile uczestników i ich dynamika (LLM)

**Źródło:** fork [AngeloNorelli/xaifungiD-analysis](https://github.com/AngeloNorelli/xaifungiD-analysis), commit `4e3b0e7`.
**Autorzy (wg historii commitów):** AngeloNorelli, Stanisław Mnich.

Pełny opis pipeline'u, promptów i metryk jest w [`README_oryginal.md`](README_oryginal.md).

W skrócie: transkrypt → `TranscriptParser` (wypowiedzi uczestnika per slajd) → lokalny LLM przez Ollama
(`LocalLLM`) ocenia na każdym slajdzie `engagement_level`, `confidence_level`, `communication_style` (0–1)
→ wykresy dynamiki → `XAIExplanation` generuje opis zmian między kolejnymi slajdami.

Zapisane wyniki LLM (`llm_responses*.json`) i sparsowane transkrypty (`parsed_transcripts.jsonl`) są w repozytorium,
bo ich ponowne wygenerowanie wymaga lokalnego modelu i długiego czasu obliczeń.

**To jest wariant, w którym zgodnie z planem z 13.11 typowy LLM ma zostać zastąpiony modelem typu „decision model” (JEV).**

Podsumowanie wyników: [`docs/podsumowania.md`](../../docs/podsumowania.md).
