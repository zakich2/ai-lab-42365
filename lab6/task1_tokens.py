# task1_tokens.py - whitespace vs Unicode word-like regex tokens (+ optional model subwords)
# Run: python task1_tokens.py
import re, sys
sys.stdout.reconfigure(encoding="utf-8")      # so Urdu prints on Windows consoles

samples = [
    "AI, search!",                                    # punctuation
    "I can't log in.",                                # contraction (straight apostrophe)
    "help@example.com",                               # email
    "CS4944 lab 6",                                   # identifier with digits
    "",                                               # empty string
    "\u06cc\u06c1 \u0627\u06cc\u06a9 \u0645\u062b\u0627\u0644 \u06c1\u06d2",   # Urdu: "this is an example"
]

print("original | whitespace tokens | count | word-like tokens | count")
for text in samples:
    ws = text.split()
    words = re.findall(r"\b\w+\b", text, flags=re.UNICODE)
    print(repr(text), "|", ws, len(ws), "|", words, len(words))
assert re.findall(r"\b\w+\b", "") == []

# Optional: model (sub-word) tokenizer for two English examples - needs the model download.
try:
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2", device="cpu")
    print("\nModel sub-word tokens (all-MiniLM-L6-v2):")
    for text in [samples[1], "CS4944 lab 6"]:
        toks = model.tokenizer.tokenize(text)
        print(repr(text), toks, len(toks))
except Exception as e:            # model unavailable: record the limitation in the report
    print("\nModel tokenizer unavailable:", type(e).__name__)
