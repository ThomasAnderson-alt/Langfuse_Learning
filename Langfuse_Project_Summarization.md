# Langfuse Project Summarization

> **Note:** All examples assume proper environment configuration with API keys for Silicon Flow and Langfuse services.

---

## Basic_Tracing.py

This script implements a basic chatbot using the Silicon Flow API (OpenAI-compatible) and integrates Langfuse for tracing and monitoring. It allows users to ask questions and receive responses from an AI model, logging the entire process for analysis.

**Code Structure:**

- **Imports:** `from openai import OpenAI`, `from langfuse import get_client`, `import os`
- **Configuration:**
  - Sets `SILICONFLOW_API_KEY` and initializes the OpenAI client with `base_url="https://api.siliconflow.cn/v1"`
  - Sets Langfuse environment variables and gets the client
- **Main Flow:**
  - Starts a Langfuse observation with `start_as_current_observation`
  - Collects user input
  - Calls `client.chat.completions.create` with the user's question
  - Prints the response
  - Updates the trace with input and output
  - Flushes traces to Langfuse

**Terminal Output Example:**

```console
PS C:\LLM\Big Data_Project\Langfuse_Project> python Basic_Tracing.py
Enter your question: List all capitals of South Africa
South Africa has three capital cities... (full answer)
```

---

## Dialogue_Followup_Langfuse.py

This application implements an AI-powered dialogue follow-up system for both single-choice and multiple-choice questions. It uses the Silicon Flow API for AI processing, LangGraph for workflow orchestration, and Langfuse for comprehensive tracing.

**Code Structure:**

- **Imports:** `requests`, `langgraph.graph`, `langfuse`, `json`, `logging`, `time`, `TypedDict`, etc.
- **Constants:** `API_TIMEOUT`, `SILICON_FLOW_BASE_URL`, `DEFAULT_MODEL_NAME`
- **DialogueState:** A `TypedDict` defining the workflow state (question, options, type, user_answer, api_response, parsed_result, trace)
- **VoiceFollowUp class:**
  - `__init__`: Initializes API keys, Langfuse client, and builds the workflow
  - `_build_workflow`: Creates a LangGraph workflow with nodes: `display_question`, `collect_input`, `process_api`, `display_result`
  - `_display_question_node`: Prints question/options and logs a Langfuse observation
  - `_collect_input_node`: Gets user input and logs a Langfuse observation
  - `_process_api_node`: Calls the API, parses the result, logs a Langfuse observation
  - `_display_result_node`: Prints the result and logs a Langfuse observation
  - `_build_api_payload`: Constructs the API request with explicit matching rules
  - `process_question`: Runs the workflow for a question, wrapping the whole process in a top-level Langfuse observation
- **run_demo function:** Runs a demo with both single-choice and multiple-choice questions

**Terminal Output Example:**

```console
PS C:\LLM\Big Data_Project\Langfuse_Project> python Dialogue_Followup_Langfuse.py
... (demo of single and multiple-choice question flows)
```

---

## Langfuse_PythonSDK.py

This script demonstrates the basic usage of the Langfuse Python SDK for creating and managing traces (observations) in AI applications. It shows how to initialize the Langfuse client, create observations, and send trace data to the Langfuse dashboard.

**Code Structure:**

- **Imports:** `os`, `time`, `langfuse.get_client`
- **Configuration:** Sets Langfuse environment variables
- **main function:**
  - Gets the Langfuse client
  - Starts a trace with `start_as_current_observation`
  - Updates the trace with input and output
  - Flushes traces to Langfuse
- **Script entry point:** `if __name__ == "__main__": main()`

**Terminal Output Example:**

```console
PS C:\LLM\Big Data_Project\Langfuse_Project> python Langfuse_PythonSDK.py
Trace sent to Langfuse UI.
```

---

## RAG_Application.py

This script implements a Retrieval-Augmented Generation (RAG) application using LangChain and integrates tracing with Langfuse. It loads documents, creates vector embeddings, and provides question-answering based on document content.

**Code Structure:**

- **Imports:** LangChain modules, FAISS, Langfuse, os
- **Configuration:**
  - Document settings: `DOCUMENT_FILE`, `CHUNK_SIZE`, `CHUNK_OVERLAP`
  - RAG settings: `LLM_MODEL`, `EMBEDDING_MODEL`, `TEMPERATURE`, `TOP_K_DOCUMENTS`
  - API and Langfuse keys
  - User/session IDs
- **Functions:**
  - `setup_environment`: Sets environment variables for APIs
  - `load_and_process_documents`: Loads and splits documents into chunks
  - `create_vector_store`: Creates a FAISS vector store from chunks
  - `create_qa_chain`: Sets up the RetrievalQA chain
  - `get_user_question`: Gets user input
  - `display_results`: Prints the answer
  - `main`: Orchestrates the RAG pipeline, tracing, and error handling
- **Script entry point:** `if __name__ == "__main__": main()`

**Terminal Output Example:**

```console
PS C:\LLM\Big Data_Project\Langfuse_Project> python RAG_Application.py
Starting RAG Application with Langfuse Tracing
Ready for questions!
Enter your question: ...
ANSWER:
... (AI-generated answer)
Traces sent to Langfuse dashboard
```

---

## Conclusion

![Traces for all iterations](images/Trace_Results.png)
![Observations for all examples before](images/Observation_Results.png)

**Langfuse vs LangGraph:**

**Similarities:**

- Both are used in LLM application development and observability
- Can be integrated into Python workflows for tracing, debugging, and monitoring
- Support multi-step workflows and can be used together for advanced tracing

**Differences:**

- Langfuse is a tracing and observability platform, focused on logging, visualizing, and analyzing LLM application traces and metrics
- LangGraph is a workflow orchestration library for building stateful, multi-step LLM applications
- Langfuse is about monitoring and analytics; LangGraph is about structuring and executing workflows
- Langfuse integrates with many frameworks (including LangChain, LangGraph) for trace collection, while LangGraph is a framework for building the workflows themselves
