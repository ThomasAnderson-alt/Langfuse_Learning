# RAG_Application.py Documentation

## Overview

This Python script implements a complete Retrieval-Augmented Generation (RAG) application using LangChain and integrates comprehensive tracing with Langfuse. The system loads documents, creates vector embeddings, and provides question-answering capabilities based on the document content. It combines document retrieval with AI generation to provide accurate, context-aware answers.

## User's Goal

The goal is to build an intelligent document-based question-answering system that can retrieve relevant information from documents and generate accurate answers using AI. The system provides full traceability of the entire RAG pipeline, enabling monitoring, debugging, and optimization of the retrieval and generation processes.

## Step-by-Step Function Explanation

### 1. Import Libraries

```python
import os
import requests
from langchain.chains import RetrievalQA
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langfuse import get_client
from langfuse.langchain import CallbackHandler
```

- Core LangChain components for RAG pipeline
- Document processing and vector storage libraries
- Langfuse integration for tracing
- HTTP requests for API testing

### 2. Configuration Settings

```python
DOCUMENT_FILE = "data.txt"
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
LLM_MODEL = "inclusionAI/Ling-mini-2.0"
EMBEDDING_MODEL = "Qwen/Qwen3-Embedding-4B"
TEMPERATURE = 0.0
TOP_K_DOCUMENTS = 3
```

- Defines document processing parameters
- Specifies AI models for embedding and generation
- Configures retrieval settings

### 3. API Configuration

```python
SILICONFLOW_BASE_URL = "https://api.siliconflow.cn/v1"
SILICONFLOW_API_KEY = "sk-lmzcznwaldljlkfyuauzbwijxlfaffkxasaeioyolscngoyi"
LANGFUSE_PUBLIC_KEY = "pk-lf-e5f67ba8-e833-42c6-881d-7c78988b94d8"
LANGFUSE_SECRET_KEY = "sk-lf-2cc66109-728f-4865-8926-eb703da3ef76"
LANGFUSE_HOST = "https://cloud.langfuse.com"
```

- API endpoints and authentication keys
- Silicon Flow for AI models, Langfuse for tracing

### 4. Environment Setup Function

```python
def setup_environment():
    os.environ["SILICONFLOW_API_KEY"] = SILICONFLOW_API_KEY
    os.environ["OPENAI_API_KEY"] = SILICONFLOW_API_KEY
    os.environ["LANGFUSE_PUBLIC_KEY"] = LANGFUSE_PUBLIC_KEY
    os.environ["LANGFUSE_SECRET_KEY"] = LANGFUSE_SECRET_KEY
    os.environ["LANGFUSE_HOST"] = LANGFUSE_HOST
```

- Configures all necessary environment variables
- Sets up authentication for both AI and tracing services

### 5. Document Loading and Processing

```python
def load_and_process_documents(file_path: str):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Document file not found: {file_path}")

    loader = TextLoader(file_path)
    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )
    document_chunks = text_splitter.split_documents(documents)

    return document_chunks
```

- Validates document file existence
- Loads text documents using LangChain's TextLoader
- Splits documents into overlapping chunks for better retrieval

### 6. API Connection Testing

```python
def test_api_connection():
    try:
        response = requests.get(
            f"{SILICONFLOW_BASE_URL}/models",
            headers={"Authorization": f"Bearer {SILICONFLOW_API_KEY}"},
        )
        return response.status_code == 200
    except Exception as e:
        print(f"API connection test failed: {e}")
        return False
```

- Verifies API connectivity before processing
- Tests authentication and network connectivity
- Provides early error detection

### 7. Vector Store Creation

```python
def create_vector_store(document_chunks):
    embeddings = OpenAIEmbeddings(
        model=EMBEDDING_MODEL,
        base_url=SILICONFLOW_BASE_URL
    )
    vector_store = FAISS.from_documents(document_chunks, embeddings)
    return vector_store
```

- Creates embeddings for document chunks using specified model
- Builds FAISS vector database for efficient similarity search
- Enables fast retrieval of relevant document sections

### 8. QA Chain Creation

```python
def create_qa_chain(vector_store):
    llm = ChatOpenAI(
        model=LLM_MODEL,
        temperature=TEMPERATURE,
        base_url=SILICONFLOW_BASE_URL
    )

    retriever = vector_store.as_retriever(search_kwargs={"k": TOP_K_DOCUMENTS})

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=False
    )

    return qa_chain
```

- Initializes the language model for answer generation
- Creates retriever with configurable top-k document retrieval
- Builds the complete QA chain combining retrieval and generation

### 9. User Interaction Functions

```python
def get_user_question():
    return input("Enter your question: ").strip()

def display_results(result):
    print("\n" + "="*50)
    print("ANSWER:")
    print("="*50)
    print(result["result"])
```

- Handles user input collection
- Formats and displays answers in a user-friendly manner

### 10. Main Orchestration Function

```python
def main():
    print("Starting RAG Application with Langfuse Tracing")

    try:
        setup_environment()

        langfuse_handler = CallbackHandler()
        langfuse_client = get_client()

        with langfuse_client.start_as_current_observation(
            name="Langchain-Application",
            as_type='generation',
            model=LLM_MODEL,
            model_parameters={"temperature": str(TEMPERATURE)}
        ) as generation:
            generation.update_trace(user_id=USER_ID, session_id=SESSION_ID)

            # Document processing pipeline
            document_chunks = load_and_process_documents(DOCUMENT_FILE)
            vector_store = create_vector_store(document_chunks)
            qa_chain = create_qa_chain(vector_store)

            # Question answering
            question = get_user_question()
            generation.update_trace(input={"question": question})

            result = qa_chain.invoke(
                {"query": question},
                config={"callbacks": [langfuse_handler]}
            )

            generation.update_trace(output={"answer": result["result"]})
            display_results(result)

    except Exception as error:
        print(f"\nError occurred: {error}")
        generation.update_trace(output={"error": str(error)})

    finally:
        try:
            get_client().flush()
            print("\nTraces sent to Langfuse dashboard")
        except Exception as e:
            print(f"Error flushing traces: {e}")
```

- Orchestrates the entire RAG pipeline
- Initializes tracing and error handling
- Processes documents, creates vector store, handles questions
- Ensures proper cleanup and trace flushing

## How the Program Achieves the User's Goal

1. **Document-Based QA**: Combines document retrieval with AI generation to provide accurate, context-aware answers based on specific document content.

2. **Efficient Retrieval**: Uses vector embeddings and FAISS for fast similarity search, retrieving the most relevant document chunks for each question.

3. **AI-Generated Answers**: Leverages advanced language models to generate coherent, natural-sounding answers based on retrieved context.

4. **Comprehensive Tracing**: Every step of the RAG pipeline is traced with Langfuse, providing visibility into:

   - Document processing performance
   - Retrieval accuracy and speed
   - Generation quality and latency
   - User interaction patterns
   - Error rates and types

5. **Modular Architecture**: Clean separation of concerns allows easy modification of individual components (embedding models, retrievers, generators).

6. **Error Handling**: Robust error handling at each step prevents system failures and provides meaningful feedback.

7. **Scalability**: The design supports processing larger document collections and handling multiple concurrent users.

8. **Monitoring and Optimization**: Detailed tracing enables continuous improvement of the system's performance and accuracy.

This RAG application transforms static documents into interactive, intelligent knowledge bases that can answer complex questions while maintaining full observability through Langfuse tracing.
