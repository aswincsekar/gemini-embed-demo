# Gemini Embeddings Smart Help Center

A production-ready help center implementation that leverages Google Gemini's task-specific embeddings to dramatically improve search accuracy for customer support queries.

## Key Features

- **Task-Specific Embeddings**: Uses different embedding strategies for documents (`RETRIEVAL_DOCUMENT`) vs user queries (`RETRIEVAL_QUERY`)
- **Smart Query Expansion**: Automatically expands user queries with synonyms and related terms
- **Confidence Scoring**: Provides confidence levels for search results
- **Category Filtering**: Filter results by article categories
- **Batch Processing**: Efficiently indexes large numbers of articles
- **Production Ready**: Includes error handling, logging, and environment-based configuration

## Quick Start

### 1. Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd gemini-embed-demo

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

Create a `.env` file in the project root:

```bash
# Copy the example file
cp env.example .env

# Edit .env and add your Gemini API key
GEMINI_API_KEY=your_actual_api_key_here
```

Get your API key from: [Google AI Studio](https://makersuite.google.com/app/apikey)

### 3. Run the Example

```bash
python example_usage.py
```

This will:
- Initialize a help center with sample articles
- Index them with document-specific embeddings
- Test various user queries
- Show how different task types improve retrieval

## Usage

### Basic Implementation

```python
from help_center import SmartHelpCenter

# Initialize
help_center = SmartHelpCenter()

# Index your articles
articles = [
    {
        "article_id": "001",
        "title": "Getting Started Guide",
        "content": "Full article content here...",
        "category": "basics"
    }
]
help_center.index_help_articles(articles)

# Answer user queries
result = help_center.answer_support_query("how do I get started?")
print(result['answer'])
```

### Advanced Features

```python
# Filter by category
result = help_center.answer_support_query(
    "payment issues",
    category_filter="billing"
)

# Get more results
result = help_center.answer_support_query(
    "export data",
    top_k=5  # Return top 5 articles
)

# Check confidence
if result['confidence'] == 'high':
    # Use the answer directly
    return result['answer']
else:
    # Maybe escalate to human support
    return "Let me connect you with a support agent..."
```

## Project Structure

```
gemini-embed-demo/
├── article.md           # Blog post explaining the concept
├── help_center.py       # Core SmartHelpCenter implementation
├── example_usage.py     # Demonstration with sample data
├── requirements.txt     # Python dependencies
├── env.example         # Example environment configuration
└── README.md           # This file
```

## How It Works

1. **Document Indexing**: Articles are embedded using `RETRIEVAL_DOCUMENT` task type, optimized for well-structured content
2. **Query Processing**: User queries are embedded using `RETRIEVAL_QUERY` task type, optimized for questions and fragments
3. **Similarity Search**: ChromaDB performs cosine similarity search to find relevant articles
4. **Response Generation**: Gemini generates a helpful response using the retrieved articles as context

## Performance Tips

- **Chunk Large Articles**: Use the `smart_chunk()` function for articles over 2000 words
- **Batch Indexing**: Index articles in batches of 100 for better performance
- **Query Expansion**: The system automatically expands queries with synonyms
- **Caching**: Consider caching frequently asked questions

## Requirements

- Python 3.8+
- Google Gemini API key
- 2GB RAM minimum (for ChromaDB)

## Common Issues

### API Key Not Found
```
Error: GEMINI_API_KEY not found in environment variables
```
**Solution**: Create a `.env` file with your API key

### Rate Limiting
```
Error: Resource exhausted
```
**Solution**: Implement exponential backoff or upgrade your API plan

### Memory Issues with Large Datasets
**Solution**: Use batch processing and consider persistent ChromaDB storage

## Contributing

Feel free to submit issues and enhancement requests!

## License

MIT License - feel free to use this in your own projects!
