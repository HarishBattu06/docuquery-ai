# Project Report: DOCUQUERY AI

## Objective

To build an AI-powered assistant that allows users to upload PDFs and interact with their content using natural language queries.

## Components

- **Streamlit**: For frontend UI and user interaction.
- **LlamaIndex**: Document indexing and vector store.
- **LangChain + Ollama**: For query handling with advanced LLMs.
- **HuggingFace Embeddings**: For creating document embeddings.

## Workflow

1. User uploads a PDF.
2. PDF content is loaded and embedded.
3. Query is passed through a prompt template.
4. LLM returns the result based on indexed content.

## Limitations

- Currently supports only one PDF at a time.
- No authentication or access control.

## Future Improvements

- Multi-PDF support.
- UI enhancements.
- Memory/Context retention for long conversations.
