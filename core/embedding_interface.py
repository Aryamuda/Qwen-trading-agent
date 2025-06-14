# core/embedding_interface.py

from abc import ABC, abstractmethod
from typing import List
from sentence_transformers import SentenceTransformer

class EmbeddingInterface(ABC):
    """
    Abstract Base Class for embedding model interfaces.
    
    This ensures that the memory system can use any embedding model that conforms
    to this interface, promoting vendor independence as outlined in the blueprint.
    """
    
    @abstractmethod
    def get_embedding_dimensions(self) -> int:
        """Returns the dimensionality of the embeddings."""
        pass

    @abstractmethod
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """
        Converts a list of documents into their vector embeddings.
        
        Args:
            texts: A list of strings to embed.
            
        Returns:
            A list of vector embeddings, where each embedding is a list of floats.
        """
        pass

class HuggingFaceEmbedding(EmbeddingInterface):
    """
    Implementation of the EmbeddingInterface using HuggingFace's Sentence Transformers library.
    
    This class loads a pre-trained model to generate high-quality semantic embeddings locally.
    
    Dependencies:
        - pip install sentence-transformers
        - pip install torch
    """
    
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        """
        Initializes the HuggingFace embedding model.
        
        The first time this is run, it will download the specified model from HuggingFace.
        
        Args:
            model_name: The name of the Sentence Transformer model to use.
        """
        print(f"Loading HuggingFace embedding model: '{model_name}'...")
        self.model = SentenceTransformer(model_name)
        print("Embedding model loaded successfully.")
        
    def get_embedding_dimensions(self) -> int:
        """
        Gets the embedding dimension of the loaded model. This is crucial for initializing
        the vector database (ChromaDB) with the correct schema.
        """
        return self.model.get_sentence_embedding_dimension()

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """
        Generates embeddings for a list of texts.
        """
        print(f"Generating embeddings for {len(texts)} document(s)...")
        embeddings = self.model.encode(texts, convert_to_tensor=False)
        print("Embeddings generated successfully.")
        # The model by default returns numpy arrays, convert them to lists of floats for broader compatibility
        return [embedding.tolist() for embedding in embeddings]

# Example Usage:
if __name__ == '__main__':
    # This demonstrates the embedding process.
    # In the actual system, this will be called by the agent memory system.
    
    # The blueprint specifies 'all-MiniLM-L6-v2'
    embedding_model = HuggingFaceEmbedding(model_name='all-MiniLM-L6-v2')
    
    # Check if dimensionality is correct (should be 384 for this model)
    dims = embedding_model.get_embedding_dimensions()
    print(f"\nEmbedding Dimensions: {dims}")
    
    # Example analyst reports that would be stored in memory
    documents_to_embed = [
        "NVIDIA's Q4 earnings exceeded expectations, driven by strong demand in the data center and AI sectors.",
        "Regulatory concerns are growing over potential antitrust investigations into major tech firms, including NVIDIA.",
        "AMD announced a new line of GPUs that aim to compete directly with NVIDIA's flagship products."
    ]
    
    vector_embeddings = embedding_model.embed_documents(documents_to_embed)
    
    print("\n--- Generated Embeddings (showing first 5 dims of first vector) ---")
    print(vector_embeddings[0][:5])
    print("...")
    print(f"Total {len(vector_embeddings)} vectors generated.")
    print("-----------------------------------------------------------------")
