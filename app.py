from src.search import RAGSearch

# Inference only — run train.py first to build the FAISS index
if __name__ == "__main__":
    rag_search = RAGSearch()
    query = "Give me professional summary from my resume?"
    summary = rag_search.search_and_summarize(query, top_k=3)
    print("Professional Summary:", summary)