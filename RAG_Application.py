"""
RAG Application with Langfuse Tracing
"""

# Imports

import os
import requests
from langchain.chains import RetrievalQA
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langfuse import get_client
from langfuse.langchain import CallbackHandler

# Configuration

# Document Processing Settings
DOCUMENT_FILE = "data.txt"
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

# RAG Settings
LLM_MODEL = "inclusionAI/Ling-mini-2.0"
EMBEDDING_MODEL = "Qwen/Qwen3-Embedding-4B"  # Specify embedding model explicitly
TEMPERATURE = 0.0
TOP_K_DOCUMENTS = 3

# API Configuration
SILICONFLOW_BASE_URL = "https://api.siliconflow.cn/v1"
SILICONFLOW_API_KEY = "sk-lmzcznwaldljlkfyuauzbwijxlfaffkxasaeioyolscngoyi"

# Langfuse Configuration
LANGFUSE_PUBLIC_KEY = "pk-lf-e5f67ba8-e833-42c6-881d-7c78988b94d8"
LANGFUSE_SECRET_KEY = "sk-lf-2cc66109-728f-4865-8926-eb703da3ef76"
LANGFUSE_HOST = "https://cloud.langfuse.com"

# User Settings
USER_ID = "User123"
# Session Settings
SESSION_ID = "Session001"  # Static session ID for grouping traces

# Functions

def setup_environment():
    # Configure environment variables for API access.
    # Configure SiliconFlow API
    os.environ["SILICONFLOW_API_KEY"] = SILICONFLOW_API_KEY
    os.environ["OPENAI_API_KEY"] = SILICONFLOW_API_KEY

    # Configure Langfuse
    os.environ["LANGFUSE_PUBLIC_KEY"] = LANGFUSE_PUBLIC_KEY
    os.environ["LANGFUSE_SECRET_KEY"] = LANGFUSE_SECRET_KEY
    os.environ["LANGFUSE_HOST"] = LANGFUSE_HOST

def load_and_process_documents(file_path: str):
    # Load documents from file and split into chunks.
    # Validate file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Document file not found: {file_path}")
    
    try:
        # Load documents
        loader = TextLoader(file_path)
        documents = loader.load()
        
        if not documents:
            raise ValueError(f"No content found in {file_path}")
        
        
        # Split into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP
        )
        document_chunks = text_splitter.split_documents(documents)
        
        return document_chunks
        
    except Exception as e:
        print(f"Error processing documents: {e}")
        raise

def test_api_connection():
    # Test API connection to SiliconFlow.
    try:
        response = requests.get(
            f"{SILICONFLOW_BASE_URL}/models",
            headers={"Authorization": f"Bearer {SILICONFLOW_API_KEY}"},
        )
        timeout = 10
        return response.status_code == 200
    except Exception as e:
        print(f"API connection test failed: {e}")
        return False

def create_vector_store(document_chunks):
    # Create FAISS vector store from document chunks.
    try:
        embeddings = OpenAIEmbeddings(
            model=EMBEDDING_MODEL,
            base_url=SILICONFLOW_BASE_URL
        )
        vector_store = FAISS.from_documents(document_chunks, embeddings)
        return vector_store
    except Exception as e:
        print(f"Error creating vector store: {e}")
        raise

def create_qa_chain(vector_store):
    # Create RetrievalQA chain for question answering.
    try:
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
        
    except Exception as e:
        print(f"Error creating QA chain: {e}")
        raise

def get_user_question():
    # Get question from user input.
    return input("Enter your question: ").strip()

def display_results(result):
    # Display QA results to user.
    print("\n" + "="*50)
    print("ANSWER:")
    print("="*50)
    print(result["result"])

def main():
    # Orchestrate RAG pipeline execution.
    print("Starting RAG Application with Langfuse Tracing")
    print("="*60)

    try:
        # Setup environment and APIs
        setup_environment()

        # Initialize Langfuse tracing
        langfuse_handler = CallbackHandler()
        langfuse_client = get_client()


        # Start main trace with session_id
        with langfuse_client.start_as_current_observation(
            name="Langchain-Application",
            as_type='generation',
            model=LLM_MODEL,
            model_parameters={
                "temperature": str(TEMPERATURE)
            }
        ) as generation:
            generation.update_trace(user_id=USER_ID, session_id=SESSION_ID)

            try:
                # Document Processing Pipeline
                document_chunks = load_and_process_documents(DOCUMENT_FILE)

                vector_store = create_vector_store(document_chunks)

                qa_chain = create_qa_chain(vector_store)

                # Question Answering
                print("\nReady for questions!")
                question = get_user_question()

                if not question:
                    print("No question provided. Exiting...")
                    return

                # Update trace with input
                generation.update_trace(input={"question": question})

                result = qa_chain.invoke(
                    {"query": question},
                    config={"callbacks": [langfuse_handler]}
                )

                # Update trace with output
                generation.update_trace(output={
                    "answer": result["result"]
                })

                # Display results
                display_results(result)

                print("\nProcessing complete! Check Langfuse for detailed traces.")

            except Exception as error:
                print(f"\nError occurred: {error}")
                # Update trace with error
                generation.update_trace(output={"error": str(error)})
                # Error is automatically captured by Langfuse handler

    except Exception as error:
        print(f"\nCritical error: {error}")
        
    finally:
        # Ensure all traces are sent to Langfuse
        try:
            get_client().flush()
            print("\nTraces sent to Langfuse dashboard")
        except Exception as e:
            print(f"Error flushing traces: {e}")
            

# Main Execution

if __name__ == "__main__":
    main()