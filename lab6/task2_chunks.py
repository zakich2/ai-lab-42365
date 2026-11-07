# task2_chunks.py - reusable chunking module (word windows + sentence-aware packing)
# Run tests: python task2_chunks.py
import re

def word_spans(text):
    return [(m.start(), m.end()) for m in re.finditer(r"\S+", text)]

def windows(text, size=40, overlap=10, offset=0):
    """Fixed windows of `size` whitespace-words; consecutive windows share `overlap` words."""
    if size <= 0 or not 0 <= overlap < size:
        raise ValueError("Require size > 0 and 0 <= overlap < size")
    spans = word_spans(text)
    result = []
    for i in range(0, len(spans), size - overlap):
        j = min(i + size, len(spans))
        result.append((offset + spans[i][0], offset + spans[j - 1][1]))
        if j == len(spans):
            break
    return result

def sentence_chunks(text, size=40):
    """Pack whole sentences up to `size` words. A sentence longer than `size` uses window fallback."""
    if size <= 0:
        raise ValueError("size must be positive")
    # Teaching splitter: sentence-ending punctuation followed by whitespace.
    cuts = [0] + [m.end() for m in re.finditer(r"[.!?]\s+", text)] + [len(text)]
    out, pending, count = [], None, 0

    def trim(a, b):                       # drop trailing whitespace from a span
        while b > a and text[b - 1].isspace():
            b -= 1
        return (a, b)

    for a, b in zip(cuts, cuts[1:]):
        segment = text[a:b]
        n = len(segment.split())
        if not n:
            continue
        if n > size:                      # long sentence: flush pending, then fallback split
            if pending is not None:
                out.append(trim(*pending))
            out.extend(windows(segment, size, 0, a))
            pending, count = None, 0
        elif pending is not None and count + n <= size:
            pending, count = (pending[0], b), count + n
        else:
            if pending is not None:
                out.append(trim(*pending))
            pending, count = (a, b), n
    if pending is not None:
        out.append(trim(*pending))
    return out

def make_chunks(docs, strategy):
    """strategy: '0' or '10' (window overlap) or 'sentence'. Returns chunk dicts with offsets."""
    result = []
    for doc_id, text in docs.items():
        spans = sentence_chunks(text) if strategy == "sentence" else windows(text, 40, int(strategy))
        for i, (a, b) in enumerate(spans):
            result.append(dict(id=f"{doc_id}:{i}", doc=doc_id, start=a, end=b, text=text[a:b]))
    return result

if __name__ == "__main__":
    assert windows("") == []
    assert windows("short text") == [(0, 10)]
    try:
        windows("a b", 2, 2)
    except ValueError:
        pass
    else:
        raise AssertionError("Invalid overlap was accepted")
    long = " ".join(["word"] * 95) + "."
    assert all(len(long[a:b].split()) <= 40 for a, b in sentence_chunks(long))
    print("long 95-word sentence ->", len(sentence_chunks(long)), "fallback chunks")
    assert sentence_chunks("") == []
    docs = {"example": "Reset your password. Keep recovery codes private."}
    for strategy in ["0", "10", "sentence"]:
        for c in make_chunks(docs, strategy):
            assert c["text"] == docs[c["doc"]][c["start"]:c["end"]]
            print(strategy, c)
    print("All chunking tests passed")
