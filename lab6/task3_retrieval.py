# task3_retrieval.py - evaluate 3 chunking strategies x 2 retrieval methods (Hit@3, MRR@3, time, CSV log)
# Run: python task3_retrieval.py            (full run, needs the sentence-transformers model)
#      python task3_retrieval.py --tfidf-only   (lexical baseline only, no model)
import csv, json, sys, time
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from task2_chunks import make_chunks

TFIDF_ONLY = "--tfidf-only" in sys.argv

def evaluate(scores, chunks, items):
    """Hit@3 and MRR@3 over ANSWERABLE queries only. Relevant = right doc AND full evidence in chunk."""
    hits, reciprocal, failed = [], [], []
    for row, q in zip(scores, items):
        if q["doc"] is None:
            continue
        top = np.argsort(-row, kind="stable")[:3]
        good = [rank for rank, i in enumerate(top, 1)
                if chunks[i]["doc"] == q["doc"] and q["evidence"] in chunks[i]["text"]]
        hits.append(bool(good)); reciprocal.append(1 / good[0] if good else 0)
        if not good:
            failed.append(q["query"])
    if not hits:
        return None, None, failed
    return float(np.mean(hits)), float(np.mean(reciprocal)), failed

def main():
    docs = json.load(open("corpus.json", encoding="utf-8"))
    items = json.load(open("queries.json", encoding="utf-8"))
    assert docs and items
    for q in items:
        assert q["split"] in {"dev", "test"}
        if q["doc"] is not None:
            assert q["evidence"] and q["evidence"] in docs[q["doc"]]
    query_texts = [q["query"] for q in items]
    model = None
    if not TFIDF_ONLY:
        from sentence_transformers import SentenceTransformer
        t = time.perf_counter()
        model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2", device="cpu")
        print("Model load seconds", round(time.perf_counter() - t, 3))
    logs = []
    print("strategy | method | split | Hit@3 | MRR@3 | chunks | encode_s | search_s | failed queries")
    for strategy in ["0", "10", "sentence"]:
        chunks = make_chunks(docs, strategy)
        texts = [c["text"] for c in chunks]
        if model is not None:                                    # token-length audit
            lengths = [len(model.tokenizer(x, truncation=False)["input_ids"]) for x in texts + query_texts]
            print(f"[audit] strategy={strategy} max tokens={max(lengths)} limit={model.max_seq_length}")
            if max(lengths) > model.max_seq_length:
                raise ValueError("Model limit exceeded; rechunk or shorten query")
        for method in (["tfidf"] if TFIDF_ONLY else ["tfidf", "embedding"]):
            t = time.perf_counter()
            if method == "tfidf":
                vec = TfidfVectorizer(); C = vec.fit_transform(texts); Q = vec.transform(query_texts)
            else:
                C = model.encode(texts, normalize_embeddings=True)
                Q = model.encode(query_texts, normalize_embeddings=True)
            encode_s = time.perf_counter() - t
            t = time.perf_counter()
            scores = (Q @ C.T).toarray() if method == "tfidf" else Q @ C.T
            search_s = time.perf_counter() - t
            for split in ["dev", "test"]:
                idx = [i for i, q in enumerate(items) if q["split"] == split]
                hit, mrr, failed = evaluate(scores[idx], chunks, [items[i] for i in idx])
                print(strategy, method, split, hit, None if mrr is None else round(mrr, 3), len(chunks),
                      round(encode_s, 4), round(search_s, 5), failed, sep=" | ")
            for row, q in zip(scores, items):
                for rank, i in enumerate(np.argsort(-row, kind="stable")[:3], 1):
                    c = chunks[i]
                    logs.append(dict(strategy=strategy, method=method, query=q["query"], split=q["split"],
                                     rank=rank, score=round(float(row[i]), 4), chunk_id=c["id"], doc=c["doc"],
                                     start=c["start"], end=c["end"], text=c["text"], answerable=q["doc"] is not None))
    with open("retrieval_log.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(logs[0])); w.writeheader(); w.writerows(logs)
    print("Wrote retrieval_log.csv with", len(logs), "rows")
    # unanswerable queries: top-1 hit still returned for every configuration
    print("\nUnanswerable queries - top-1 result per configuration (shows why a score is not an answer):")
    for r in logs:
        if not r["answerable"] and r["rank"] == 1:
            print(r["strategy"], r["method"], repr(r["query"]), r["chunk_id"], r["score"])

if __name__ == "__main__":
    main()
