# guided_suggestions.py - Run: python guided_suggestions.py [--backend embedding] [--query "forgot login"]
import argparse
from guided_chatbot import build_bot
p = argparse.ArgumentParser()
p.add_argument("--backend", choices=["tfidf", "embedding"], default="tfidf")
p.add_argument("--query", default="assignment upload")
a = p.parse_args()
engine = build_bot(a.backend)
print("Suggested questions for:", repr(a.query), "| backend:", a.backend)
for record, score in engine.search(a.query, k=3):
    if a.backend == "embedding" or score > 0:   # the >0 cutoff is for TF-IDF only
        print(record["question"], f"({score:.3f})")
