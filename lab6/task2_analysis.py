# task2_analysis.py - compare chunking strategies on corpus.json (counts, sizes, duplication, survival)
# Run: python task2_analysis.py    (run create_dataset.py first)
import json
from task2_chunks import make_chunks, windows, sentence_chunks

docs = json.load(open("corpus.json", encoding="utf-8"))
queries = json.load(open("queries.json", encoding="utf-8"))
evidence = {q["doc"]: q["evidence"] for q in queries if q["doc"]}
# rule + exception pairs that must stay together in ONE chunk
PAIRS = {
    "late": ("Late submission is normally penalized",
             "Illness extensions require medical evidence before the deadline."),
    "contractor": ("Contractors can work remotely only if the signed contract permits it.",
                   "Employee rules do not apply to contractors"),
}

orig_words = sum(len(t.split()) for t in docs.values())
print("Documents:", len(docs), "| original words:", orig_words)
print("\nstrategy | chunks | avg words | max words | duplicate words | evidence kept | rule+exception kept")
for strategy in ["0", "10", "sentence"]:
    chunks = make_chunks(docs, strategy)
    sizes = [len(c["text"].split()) for c in chunks]
    dup = sum(sizes) - orig_words
    kept = sum(any(evidence[d] in c["text"] for c in chunks if c["doc"] == d) for d in evidence)
    pair_kept = sum(any(a in c["text"] and b in c["text"] for c in chunks if c["doc"] == d)
                    for d, (a, b) in PAIRS.items())
    print(f"{strategy} | {len(chunks)} | {sum(sizes)/len(sizes):.1f} | {max(sizes)} | {dup} | "
          f"{kept}/{len(evidence)} | {pair_kept}/{len(PAIRS)}")

print("\nPer-document evidence survival (True = full evidence sentence inside one chunk)")
for strategy in ["0", "10", "sentence"]:
    chunks = make_chunks(docs, strategy)
    row = {d: any(evidence[d] in c["text"] for c in chunks if c["doc"] == d) for d in evidence}
    print(strategy, row)

print("\n=== Required boundary tests ===")
print("empty text            : windows =", windows(""), "| sentence =", sentence_chunks(""))
short = "Only a short note."
print("shorter than budget   : windows =", windows(short), "| sentence =", sentence_chunks(short))
try:
    windows("a b c d", 3, 3)
except ValueError as e:
    print("invalid overlap       : ValueError ->", e)
long_sentence = " ".join(["word"] * 95) + "."
print("95-word sentence      : sentence chunks =", len(sentence_chunks(long_sentence)),
      "| words per chunk =", [len(long_sentence[a:b].split()) for a, b in sentence_chunks(long_sentence)])
abbrev = "Dr. Khan teaches AI. Prof. Ali teaches ML."
print("abbreviation failure  :", [abbrev[a:b] for a, b in sentence_chunks(abbrev, 3)])
