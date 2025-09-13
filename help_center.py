"""
Smart Help Center implementation using Gemini's task-specific embeddings.
This module provides a production-ready help center that uses different embedding
strategies for documents vs queries to improve retrieval accuracy.
"""

import os
import numpy as np
from typing import List, Dict, Optional
import chromadb
from google import genai
from google.genai import types
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class SmartHelpCenter:
    """A help center system powered by Gemini embeddings and ChromaDB."""
    
    def __init__(self, collection_name: str = "help_articles"):
        """
        Initialize the help center with Gemini embeddings and ChromaDB.
        
        Args:
            collection_name: Name for the ChromaDB collection
        """
        # Get API key from environment
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables. "
                           "Please create a .env file with your API key.")
        
        self.client = genai.Client(api_key=api_key)
        self.vector_db = chromadb.Client()
        
        # Create or get collection
        try:
            self.collection = self.vector_db.create_collection(
                name=collection_name,
                metadata={"hnsw:space": "cosine"}
            )
        except ValueError:
            # Collection already exists
            self.collection = self.vector_db.get_collection(name=collection_name)
    
    def index_help_articles(self, articles: List[Dict[str, str]], batch_size: int = 100):
        """
        Index help articles with proper document embeddings.
        
        Args:
            articles: List of dicts with 'title', 'content', 'article_id', and optional 'category'
            batch_size: Number of articles to process at once
        """
        if not articles:
            print("No articles to index.")
            return
        
        # Process in batches for better performance
        for i in range(0, len(articles), batch_size):
            batch = articles[i:i + batch_size]
            self._index_batch(batch, start_idx=i)
    
    def _index_batch(self, articles: List[Dict[str, str]], start_idx: int = 0):
        """Index a batch of articles."""
        documents_to_embed = []
        metadata_list = []
        
        for article in articles:
            # Validate required fields
            if not all(k in article for k in ['title', 'content', 'article_id']):
                print(f"Skipping article with missing fields: {article.get('article_id', 'unknown')}")
                continue
            
            # Combine title and content for richer embeddings
            full_text = f"{article['title']}\n\n{article['content']}"
            documents_to_embed.append(full_text)
            
            metadata_list.append({
                "article_id": article['article_id'],
                "title": article['title'],
                "category": article.get('category', 'general'),
                "char_count": len(full_text)
            })
        
        if not documents_to_embed:
            return
        
        # Generate embeddings optimized for document retrieval
        print(f"Indexing {len(documents_to_embed)} help articles...")
        try:
            response = self.client.models.embed_content(
                model="gemini-embedding-001",
                contents=documents_to_embed,
                config=types.EmbedContentConfig(
                    task_type="RETRIEVAL_DOCUMENT",
                    output_dimensionality=768
                )
            )
        except Exception as e:
            print(f"Error generating embeddings: {e}")
            return
        
        # Store in vector database
        embeddings = [emb.values for emb in response.embeddings]
        ids = [f"doc_{start_idx + i}" for i in range(len(documents_to_embed))]
        
        self.collection.add(
            embeddings=embeddings,
            documents=documents_to_embed,
            metadatas=metadata_list,
            ids=ids
        )
        
        print(f"Successfully indexed {len(documents_to_embed)} articles!")
    
    def answer_support_query(self, 
                            user_query: str, 
                            top_k: int = 3,
                            category_filter: Optional[str] = None) -> Dict:
        """
        Find relevant help articles for a user's support query.
        
        Args:
            user_query: The user's question
            top_k: Number of relevant articles to retrieve
            category_filter: Optional category to filter results
        
        Returns:
            Dict containing answer, relevant articles, and confidence score
        """
        # Expand query with synonyms
        expanded_query = self._expand_query(user_query)
        
        # Generate query embedding - note the different task type!
        try:
            query_response = self.client.models.embed_content(
                model="gemini-embedding-001",
                contents=[expanded_query],
                config=types.EmbedContentConfig(
                    task_type="RETRIEVAL_QUERY",
                    output_dimensionality=768
                )
            )
        except Exception as e:
            return {
                'answer': f"Error processing query: {e}",
                'relevant_articles': [],
                'confidence': 'error'
            }
        
        query_embedding = query_response.embeddings[0].values
        
        # Build where clause for filtering
        where_clause = {"category": category_filter} if category_filter else None
        
        # Search for relevant articles
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            where=where_clause
        )
        
        if not results['ids'][0]:
            return {
                'answer': "I couldn't find any relevant articles for your question.",
                'relevant_articles': [],
                'confidence': 'none'
            }
        
        # Format the response
        relevant_articles = []
        for i in range(len(results['ids'][0])):
            relevant_articles.append({
                'title': results['metadatas'][0][i]['title'],
                'article_id': results['metadatas'][0][i]['article_id'],
                'category': results['metadatas'][0][i]['category'],
                'relevance_score': 1 - results['distances'][0][i],
                'snippet': results['documents'][0][i][:200] + "..."
            })
        
        # Generate a helpful response using the retrieved context
        context = "\n\n---\n\n".join([doc for doc in results['documents'][0]])
        response = self._generate_support_response(user_query, context)
        
        return {
            'answer': response,
            'relevant_articles': relevant_articles,
            'confidence': self._calculate_confidence(results['distances'][0])
        }
    
    def _expand_query(self, user_query: str) -> str:
        """Expand user query with synonyms and related terms."""
        expansions = {
            "can't": "cannot unable",
            "doesn't work": "not working broken error fail",
            "payment": "billing charge subscription invoice",
            "login": "sign in signin authenticate",
            "password": "credential passphrase pwd",
            "export": "download save extract",
            "delete": "remove erase clear",
            "create": "make new add",
            "update": "edit modify change"
        }
        
        expanded = user_query.lower()
        for term, synonyms in expansions.items():
            if term in expanded:
                expanded += f" {synonyms}"
        
        return expanded
    
    def _generate_support_response(self, query: str, context: str) -> str:
        """Generate a helpful response using retrieved articles as context."""
        prompt = f"""Based on the following help articles, provide a clear and helpful answer to the user's question.
        
User Question: {query}

Relevant Help Articles:
{context}

Instructions:
- Provide a concise, friendly response that directly addresses the user's question
- Use information from the articles to give specific, actionable steps
- If the articles don't contain the exact answer, suggest related information that might help
- Keep the tone helpful and professional
- Format the response with clear steps if applicable"""
        
        try:
            response = self.client.models.generate_content(
                model="gemini-1.5-flash",
                contents=prompt
            )
            return response.text
        except Exception as e:
            return f"I found relevant articles but encountered an error generating a response: {e}"
    
    def _calculate_confidence(self, distances: List[float]) -> str:
        """Calculate confidence level based on retrieval distances."""
        if not distances:
            return "none"
        
        avg_distance = np.mean(distances)
        if avg_distance < 0.3:
            return "high"
        elif avg_distance < 0.6:
            return "medium"
        else:
            return "low"
    
    def get_statistics(self) -> Dict:
        """Get statistics about the indexed articles."""
        try:
            # Get all documents to count
            all_docs = self.collection.get()
            
            if not all_docs['metadatas']:
                return {
                    'total_articles': 0,
                    'categories': {},
                    'avg_article_length': 0
                }
            
            # Count by category
            categories = {}
            total_chars = 0
            
            for metadata in all_docs['metadatas']:
                cat = metadata.get('category', 'general')
                categories[cat] = categories.get(cat, 0) + 1
                total_chars += metadata.get('char_count', 0)
            
            return {
                'total_articles': len(all_docs['ids']),
                'categories': categories,
                'avg_article_length': total_chars / len(all_docs['ids']) if all_docs['ids'] else 0
            }
        except Exception as e:
            print(f"Error getting statistics: {e}")
            return {
                'total_articles': 0,
                'categories': {},
                'avg_article_length': 0
            }
    
    def clear_all_articles(self):
        """Clear all articles from the collection."""
        try:
            self.vector_db.delete_collection(name=self.collection.name)
            self.collection = self.vector_db.create_collection(
                name=self.collection.name,
                metadata={"hnsw:space": "cosine"}
            )
            print("All articles cleared successfully.")
        except Exception as e:
            print(f"Error clearing articles: {e}")


def smart_chunk(article: str, max_tokens: int = 500) -> List[str]:
    """
    Split article into smart chunks for better embedding.
    
    Args:
        article: The article text to chunk
        max_tokens: Maximum tokens per chunk (approximate)
    
    Returns:
        List of text chunks
    """
    # Split by headers first
    sections = article.split('\n## ')
    chunks = []
    
    for section in sections:
        # Rough token estimation (1 token ≈ 4 chars)
        if len(section) > max_tokens * 4:
            # Further split long sections by paragraphs
            paragraphs = section.split('\n\n')
            for para in paragraphs:
                if len(para) > max_tokens * 4:
                    # Split very long paragraphs by sentences
                    sentences = para.split('. ')
                    current_chunk = ""
                    for sentence in sentences:
                        if len(current_chunk) + len(sentence) < max_tokens * 4:
                            current_chunk += sentence + ". "
                        else:
                            if current_chunk:
                                chunks.append(current_chunk.strip())
                            current_chunk = sentence + ". "
                    if current_chunk:
                        chunks.append(current_chunk.strip())
                else:
                    chunks.append(para)
        else:
            chunks.append(section)
    
    return [chunk for chunk in chunks if chunk.strip()]
