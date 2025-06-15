import chromadb
from sentence_transformers import SentenceTransformer
import chromadb.utils.embedding_functions as embedding_functions
from datetime import datetime, timezone

# 1. Setup
print("Loading sentence-transformer model...")
model_name = "all-MiniLM-L6-v2"
embedding_model = SentenceTransformer(model_name)
print("Model loaded.")

# Create a ChromaDB embedding function using the loaded model
chroma_embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name=model_name
)

# Initialize the ChromaDB client
client = chromadb.PersistentClient(path="./test_db")

# Get or create a collection, passing the embedding function
collection = client.get_or_create_collection(
    name="test_collection_with_date",
    embedding_function=chroma_embedding_function
)

# 2. Save Data with a Timestamp
print("\n--- Adding document with datetime metadata ---")

utc_timestamp = int(datetime.now(timezone.utc).timestamp())
print(f"Generated UTC timestamp to be saved: {utc_timestamp}")

collection.add(
    documents=[
        "Analysis for NVDA showed positive sentiment from social media and strong technicals."
    ],
    metadatas=[
        {"stock": "NVDA", "decision": "BUY", "date_utc": utc_timestamp}
    ],
    ids=["memo_with_date"]
)
print("Document added successfully.")


# 3. Query Data and Verify the Timestamp
print("\n--- Querying memory ---")
results = collection.query(
    query_texts=["What was the analysis for the stock with positive sentiment?"],
    n_results=1
)

print("\nQuery: 'What was the analysis for the stock with positive sentiment?'")

if results and results['metadatas']:
    retrieved_metadata = results['metadatas'][0][0]
    print(f"Found best match: {results['documents'][0][0]}")
    print(f"Retrieved Metadata: {retrieved_metadata}")
    
    # Verify the timestamp
    retrieved_timestamp = retrieved_metadata.get('date_utc')
    print(f"Successfully retrieved UTC timestamp: {retrieved_timestamp}")
    if isinstance(retrieved_timestamp, int):
        print("SUCCESS: The timestamp was stored and retrieved correctly as a number.")
    else:
        print("ERROR: The timestamp was not stored or retrieved correctly.")
else:
    print("No results found.")

