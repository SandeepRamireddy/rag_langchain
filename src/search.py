import os
from dotenv import load_dotenv
from src.vectorstore import FaissVectorStore
from langchain_groq import ChatGroq

load_dotenv()
from langchain.chat_models import init_chat_model

model = init_chat_model("google_genai:gemini-3-flash-preview")
class RAGSearch:
    def __init__(self, persist_dir: str = "faiss_store", embedding_model: str = "all-MiniLM-L6-v2", llm_model: str = "google_genai:gemini-3-flash-preview"):
        self.vectorstore = FaissVectorStore(persist_dir, embedding_model)
        # Load or build vectorstore
        faiss_path = os.path.join(persist_dir, "faiss.index")
        meta_path = os.path.join(persist_dir, "metadata.pkl")
        if not (os.path.exists(faiss_path) and os.path.exists(meta_path)):
            from .data_loader import load_all_documents
            docs = load_all_documents("rag_data")
            self.vectorstore.build_from_documents(docs)
        else:
            self.vectorstore.load()
        self.llm = init_chat_model(llm_model)
        print(f"[INFO] LLM initialized: {llm_model}")

    def classify_query(self, query: str) -> str:
        """Use the LLM to decide whether the query needs document retrieval.

        Returns 'rag' if the query is about the uploaded documents,
        or 'generic' if it can be answered from general knowledge.
        """
        classification_prompt = (
            "You are a query classifier. Given the user's question, decide whether it "
            "requires searching through uploaded documents (return 'rag') or can be "
            "answered from general knowledge (return 'generic').\n\n"
            "Examples of 'rag' queries: 'What is my professional summary?', "
            "'Summarize the uploaded report', 'What does the document say about X?'\n\n"
            "Examples of 'generic' queries: 'What is Python?', 'Hi', 'Tell me a joke', "
            "'Explain machine learning', 'What is 2+2?'\n\n"
            f"User question: {query}\n\n"
            "Respond with ONLY the single word 'rag' or 'generic', nothing else."
        )
        response = self.llm.invoke([classification_prompt])
        result = response.text().strip().lower()
        # Fallback: if the LLM returns something unexpected, default to 'rag'
        if result not in ("rag", "generic"):
            return "rag"
        return result

    def answer_generic(self, query: str) -> str:
        """Answer a generic question directly using the LLM without document retrieval."""
        prompt = (
            "You are SuperB, a helpful, friendly and intelligent AI assistant. "
            "Answer the user's question clearly and concisely.\n\n"
            f"User question: {query}\n\nAnswer:"
        )
        response = self.llm.invoke([prompt])
        return response.text()

    def search_and_summarize(self, query: str, top_k: int = 5) -> str:
        """Search documents and generate a contextual answer."""
        results = self.vectorstore.query(query, top_k=top_k)
        texts = [r["metadata"].get("text", "") for r in results if r["metadata"]]
        context = "\n\n".join(texts)
        if not context:
            return "No relevant documents found."
        prompt = (
            f"Based on the following document context, answer the user's question.\n\n"
            f"Question: {query}\n\n"
            f"Context:\n{context}\n\n"
            f"Provide a clear, well-structured answer based on the context above:"
        )
        response = self.llm.invoke([prompt])
        return response.text()

# Example usage
if __name__ == "__main__":
    rag_search = RAGSearch()
    query = "what is my professional summary"
    summary = rag_search.search_and_summarize(query, top_k=3)
    print("Summary:", summary)