# Lab 6 - NLP Fundamentals: Tokenization, Embeddings & Chunking
Setup (Python 3.10+):
    python -m venv .venv
    .venv\Scripts\Activate.ps1          # Windows PowerShell   (macOS/Linux: source .venv/bin/activate)
    python -m pip install numpy scikit-learn sentence-transformers
    python -m pip freeze > requirements.txt
The first embedding run downloads sentence-transformers/all-MiniLM-L6-v2 (internet needed once). CPU only.

Dataset (synthetic): python create_dataset.py     # writes corpus.json (5 docs) and queries.json (10 queries)

Task 1: python task1_tokens.py ; python guided_chatbot.py ; python task1_chatbot_check.py
Task 2: python task2_chunks.py ; python task2_analysis.py ; python guided_embeddings.py ;
        python guided_suggestions.py --backend embedding --query "forgot login" ; python task2_semantic_compare.py
Task 3: python task3_retrieval.py       (full run; writes retrieval_log.csv)
        python document_chatbot.py      (interactive; add --tfidf to avoid the model)
Scenarios: scenario1_handbook.py ... scenario5_equipment.py ; guided examples: guided_*.py ; lab6_search.py is the shared helper.

Do not commit .venv or model caches. Text data is synthetic; document source: written by the student for this lab.
