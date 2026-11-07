# task2_semantic_compare.py - 3 paraphrased queries, TF-IDF vs real embeddings, over sentence chunks
# Run: python task2_semantic_compare.py
import json
from task2_chunks import make_chunks
from lab6_search import Retriever

docs = json.load(open("corpus.json", encoding="utf-8"))
records = make_chunks(docs, "sentence")
paraphrases = ["How can I regain access to my account?",
               "How should I hand in my coursework?",
               "I was unwell, can I get more time?"]
for backend in ["tfidf", "embedding"]:
    print("=" * 60, "\nBackend:", backend)
    try:
        engine = Retriever(records, backend)
    except Exception as e:                       # e.g. model not downloaded
        print("Backend unavailable:", type(e).__name__, "-", e)
        continue
    for q in paraphrases:
        print("\nQuery:", q)
        hits = engine.search(q, k=3)
        if not hits:
            print("  No matching records.")
        for r, s in hits:
            print(f"  {r['id']} chars {r['start']}-{r['end']} score={s:.3f} | {r['text'][:90]}...")
