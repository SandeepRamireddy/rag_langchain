from src.data_loader import load_all_documents
from src.vectorstore import FaissVectorStore


def train(data_dir: str = "rag_data", persist_dir: str = "faiss_store"):
    """Load documents, build embeddings, and save the FAISS index."""
    print("[TRAIN] Loading documents...")
    docs = load_all_documents(data_dir)
    print(f"[TRAIN] Loaded {len(docs)} documents.")

    store = FaissVectorStore(persist_dir)
    store.build_from_documents(docs)
    store.load()

    # Quick sanity check
    print(store.query("Give me professional summary from my resume?", top_k=3))
    print("[TRAIN] Training complete. Index saved to:", persist_dir)


if __name__ == "__main__":
    train()
