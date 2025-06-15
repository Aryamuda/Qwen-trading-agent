from abc import ABC, abstractmethod
from typing import List
from sentence_transformers import SentenceTransformer

class EmbeddingInterface(ABC):
    """
    Abstract Base Class for embedding model interfaces.
    """
    
    @abstractmethod
    def get_embedding_dimensions(self) -> int:
        """Returns the dimensionality of the embeddings."""
        pass

    @abstractmethod
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """
        Converts a list of documents into their vector embeddings.
        """
        pass

class HuggingFaceEmbedding(EmbeddingInterface):
    """
    Implementation of the EmbeddingInterface using HuggingFace's Sentence Transformers library.
    """
    
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        """
        Initializes the HuggingFace embedding model.
        
        Args:
            model_name: The name of the Sentence Transformer model to use.
        """
        print(f"Loading HuggingFace embedding model: '{model_name}'...")
        self.model_name = model_name 
        self.model = SentenceTransformer(self.model_name)
        print("Embedding model loaded successfully.")
        
    def get_embedding_dimensions(self) -> int:
        """
        Gets the embedding dimension of the loaded model.
        """
        return self.model.get_sentence_embedding_dimension()

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """
        Generates embeddings for a list of texts.
        """
        print(f"Generating embeddings for {len(texts)} document(s)...")
        embeddings = self.model.encode(texts, convert_to_tensor=False)
        print("Embeddings generated successfully.")
        return [embedding.tolist() for embedding in embeddings]
