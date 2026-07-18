from src.data_loader import load_all_documents
from src.vectorstore import FaissVectorStore
from src.search import RAGSearch

# Example usage
if __name__ == "__main__":
    
    #Training code is commented below since we already trained it
    # docs = load_all_documents("rag_data")
    # store = FaissVectorStore("faiss_store")
    # store.build_from_documents(docs)
    # store.load()
    #print(store.query("What is attention mechanism?", top_k=3))
    rag_search = RAGSearch()
    query = "Give me professional summary from my resume?"
    summary = rag_search.search_and_summarize(query, top_k=3)
    print("Professional Summary:", summary)