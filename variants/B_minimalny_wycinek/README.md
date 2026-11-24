# Wariant B – minimalny wycinek rozmowy

**Źródło:** fork [LukashWalancik/xaifungi-analysis](https://github.com/LukashWalancik/xaifungi-analysis), commit `c0d4b72`.
**Autor:** Łukasz Walancik.

`analysis.ipynb` (tworzony w Google Colab) zawiera: eksplorację danych, czyszczenie tekstu (klasa `Transcript`),
podział na slajdy / pytania / zdania, TF-IDF + regresję logistyczną z SHAP, próbę fine-tuningu transformera
oraz właściwy eksperyment wariantu B – jak jakość klasyfikacji zależy od długości wycinka wypowiedzi.

Podsumowanie wyników: [`docs/podsumowania.md`](../../docs/podsumowania.md).
