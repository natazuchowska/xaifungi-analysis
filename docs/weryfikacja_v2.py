"""Weryfikacja V2 – skrypt odtwarzający liczby oznaczone w docs/podsumowania.md jako [weryfikacja V2].

Użycie:
    python docs/weryfikacja_v2.py tfidf <ścieżka do participant_documents.csv>
    python docs/weryfikacja_v2.py llm variants/D_dynamika_llm/llm_responses.json

Plik participant_documents.csv powstaje w wariancie A (variants/A_klasyfikacja/src/preprocessing/
build_initial_segments.py) i znajduje się w repozytorium KosmicznaBarta/xaifungi-analysis w data/processed/.
"""
import json
import re
import sys

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import (RepeatedStratifiedKFold, StratifiedKFold,
                                     cross_val_predict, cross_val_score)
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.preprocessing import StandardScaler

# Lista stop-słów skopiowana z variants/A_klasyfikacja/analysis_tfidf.ipynb
POLISH_STOPWORDS = [
    "i", "oraz", "a", "ale", "że", "to", "jest", "są", "być", "było", "była", "były",
    "ten", "ta", "te", "tym", "tego", "tej", "tych", "tak", "nie", "no", "mhm", "yyy", "yy",
    "w", "we", "z", "ze", "na", "do", "od", "po", "dla", "o", "u", "się", "sobie", "mi", "mnie", "ja",
    "pani", "pan", "tutaj", "tam", "bardziej", "raczej", "chyba", "może", "jakby", "więc", "czyli",
    "none", "nan", "przechodzę", "slajdu", "slajdzie", "slajd", "slajdy", "kolejnego", "kolejny",
    "następnego", "następny", "czytam", "mówi", "ns", "ok", "dobrze",
]
LABELS = ["DE", "IT", "SSH"]


def tfidf_pipeline():
    return Pipeline([
        ("tfidf", TfidfVectorizer(lowercase=True, max_features=5000, ngram_range=(1, 2),
                                  min_df=2, max_df=0.8, stop_words=POLISH_STOPWORDS)),
        ("clf", LogisticRegression(max_iter=2000, class_weight="balanced")),
    ])


def strip_markers(text):
    return re.sub(r"\[(SLIDE|QUESTION|PROBLEM)=[^\]]*\]", " ", text)


def strip_markers_and_tags(text):
    text = strip_markers(text)
    text = re.sub(r"\[[^\]]*\]", " ", text)                 # [śmiech], [niewyraźne], ...
    text = re.sub(r"\([^)]*\d\d:\d\d[^)]*\)", " ", text)    # (ns - 01:26:55)
    return text


def check_tfidf(path):
    docs = pd.read_csv(path)
    X, y = docs["full_document"].fillna(""), docs["label"]
    cv = StratifiedKFold(n_splits=3, shuffle=True, random_state=42)
    rcv = RepeatedStratifiedKFold(n_splits=3, n_repeats=10, random_state=0)
    variants = {
        "oryginalne dokumenty": X,
        "bez znaczników": X.apply(strip_markers),
        "bez znaczników i tagów": X.apply(strip_markers_and_tags),
    }
    for name, Xv in variants.items():
        s = cross_val_score(tfidf_pipeline(), Xv, y, cv=cv, scoring="f1_macro")
        r = cross_val_score(tfidf_pipeline(), Xv, y, cv=rcv, scoring="f1_macro")
        pred = cross_val_predict(tfidf_pipeline(), Xv, y, cv=cv)
        diag = confusion_matrix(y, pred, labels=LABELS).diagonal().tolist()
        print(f"{name:28s} 3-fold: {s.mean():.3f} ± {s.std():.3f} | "
              f"10x3-fold: {r.mean():.3f} ± {r.std():.3f} | poprawni {dict(zip(LABELS, diag))}")


def check_llm(path):
    data = json.load(open(path, encoding="utf-8"))
    rows = []
    for pid, slides in data.items():
        for slide, answers in slides.items():
            for raw in answers:
                try:
                    p = json.loads(raw)["profile"]
                except (json.JSONDecodeError, KeyError, TypeError):
                    continue
                vals = [p.get(m) for m in ("engagement_level", "confidence_level", "communication_style")]
                if all(isinstance(v, (int, float)) for v in vals):
                    rows.append((pid, pid.split("_")[1], slide, *vals))
    df = pd.DataFrame(rows, columns=["pid", "group", "slide", "eng", "conf", "comm"])
    print(f"Uczestnicy z poprawnymi ocenami: {df.pid.nunique()} / {len(data)}, ocen slajdów: {len(df)}")
    print(df.groupby("group")[["eng", "conf", "comm"]].mean().round(3))

    per = df.groupby(["pid", "group"])[["eng", "conf", "comm"]].agg(["mean", "std"]).fillna(0).reset_index()
    X = per.drop(columns=["pid", "group"]).values
    y = per["group"].values
    model = make_pipeline(StandardScaler(), LogisticRegression(class_weight="balanced", max_iter=2000))
    pred = cross_val_predict(model, X, y, cv=StratifiedKFold(n_splits=3, shuffle=True, random_state=42))
    print(classification_report(y, pred, digits=2))


if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[1] not in {"tfidf", "llm"}:
        print(__doc__)
        sys.exit(1)
    (check_tfidf if sys.argv[1] == "tfidf" else check_llm)(sys.argv[2])
