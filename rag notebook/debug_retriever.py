"""
Debug script to diagnose why RAG retriever returns 0 documents.
Run this in a cell in your notebook AFTER running the VectorStore and EmbeddingManager cells.
"""

# ==========================================
# STEP 1: Check what's in the collection
# ==========================================
print("=" * 60)
print("STEP 1: Collection Info")
print("=" * 60)
count = vectorstore.collection.count()
print(f"Total documents in collection: {count}")

# Get collection metadata (includes distance function)
collection_metadata = vectorstore.collection.metadata
print(f"Collection metadata: {collection_metadata}")

# Check the distance function
if collection_metadata and 'hnsw:space' in collection_metadata:
    print(f"Distance function: {collection_metadata['hnsw:space']}")
else:
    print("Distance function: L2 (DEFAULT) <-- THIS IS THE PROBLEM!")

# ==========================================
# STEP 2: Raw query to see actual distances
# ==========================================
print("\n" + "=" * 60)
print("STEP 2: Raw ChromaDB Query Results")
print("=" * 60)
query = "Professional summary"
query_embedding = embedding_manager.generate_embeddings([query])[0]

results = vectorstore.collection.query(
    query_embeddings=[query_embedding.tolist()],
    n_results=5,
    include=["documents", "distances", "metadatas"]
)

print(f"\nQuery: '{query}'")
print(f"Number of results returned by ChromaDB: {len(results['documents'][0])}")

for i, (doc, dist) in enumerate(zip(results['documents'][0], results['distances'][0])):
    similarity_current = 1 - dist  # Your current formula
    similarity_fixed = 1 / (1 + dist)  # Better formula for L2
    print(f"\n--- Result {i+1} ---")
    print(f"  Distance (raw):                {dist:.6f}")
    print(f"  Score (your formula: 1-dist):   {similarity_current:.6f}  {'✓ PASSES >= 0.0' if similarity_current >= 0.0 else '✗ FILTERED OUT (< 0.0)'}")
    print(f"  Score (fixed formula):          {similarity_fixed:.6f}")
    print(f"  Content preview: {doc[:120]}...")

# ==========================================
# STEP 3: Check for duplicate documents
# ==========================================
print("\n" + "=" * 60)
print("STEP 3: Duplicate Check")
print("=" * 60)
all_data = vectorstore.collection.get(include=["documents", "metadatas"])
unique_contents = set(all_data['documents'])
print(f"Total documents: {len(all_data['documents'])}")
print(f"Unique documents: {len(unique_contents)}")
if len(all_data['documents']) > len(unique_contents):
    print(f"⚠️  DUPLICATES FOUND: {len(all_data['documents']) - len(unique_contents)} duplicate entries!")
    print("   This means add_documents was run multiple times.")

# Count sources
from collections import Counter
sources = [m.get('source_file', 'unknown') for m in all_data['metadatas']]
source_counts = Counter(sources)
print(f"\nDocuments per source file:")
for source, cnt in source_counts.most_common():
    print(f"  {source}: {cnt} chunks")
