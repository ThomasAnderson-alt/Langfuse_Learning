# Langfuse Project: Advanced AI Tracing and Application Examples

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/release/python-380/)
[![Langfuse](https://img.shields.io/badge/Langfuse-Observability-blue)](https://langfuse.com/)
[![LangChain](https://img.shields.io/badge/LangChain-Integration-green)](https://www.langchain.com/)
[![LangGraph](https://img.shields.io/badge/LangGraph-Workflow-orange)](https://github.com/langchain-ai/langgraph)

This repository provides a comprehensive collection of Python scripts demonstrating the practical application of the [Langfuse](https://langfuse.com/) tracing platform for building observable and robust AI systems. It includes examples of basic chatbot interaction, a sophisticated dialogue follow-up system, and a complete Retrieval-Augmented Generation (RAG) pipeline.

The projects leverage the Silicon Flow API (for OpenAI-compatible models) and showcase deep integration with Langfuse for end-to-end monitoring, debugging, and performance analysis.

## Key Features

- **End-to-End Tracing:** Full observability into AI application workflows with Langfuse.
- **Chatbot with Tracing:** A simple yet powerful example of tracing a chatbot conversation.
- **Dialogue Follow-up System:** An advanced system using LangGraph to manage multi-turn dialogues with single and multiple-choice questions.
- **Retrieval-Augmented Generation (RAG):** A complete RAG application built with LangChain, featuring document loading, embedding, and context-aware question-answering.
- **Modular and Extensible:** Code is well-structured, making it easy to understand, modify, and extend for your own projects.

## Project Structure

```text
Langfuse_Project/
├── Basic_Tracing.py                # Simple chatbot with Langfuse tracing
├── Basic_Tracing.md                # Documentation for Basic_Tracing.py
├── Dialogue_Followup_Langfuse.py   # Dialogue system with LangGraph and Langfuse
├── Dialogue_Followup_Langfuse.md   # Documentation for the dialogue system
├── PythonSDK.py                    # Basic Langfuse Python SDK usage demo
├── PythonSDK.md                    # Documentation for PythonSDK.py
├── RAG_Application.py              # RAG pipeline with LangChain and Langfuse
├── RAG_Application.md              # Documentation for the RAG application
├── book.txt                        # Sample text document for the RAG application
├── README.md                       # This file
└── images/
    ├── Observation_Results.png     # Screenshot of Langfuse observation results
    └── Trace_Results.png           # Screenshot of Langfuse trace results
```

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Git

### Installation

1. **Clone the repository:**

   ```sh
   git clone https://github.com/ThomasAnderson-alt/Langfuse-Learning.git
   cd Langfuse-Learning
   ```

2. **Create a virtual environment (recommended):**

   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install the required dependencies:**

   ```sh
   pip install openai langfuse langchain langgraph requests faiss-cpu
   ```

### Configuration

Before running the scripts, you need to set up your API keys. The scripts are designed to read these keys from environment variables.

Create a `.env` file in the root of the project directory and add your keys as follows:

```env
SILICONFLOW_API_KEY="your-siliconflow-api-key"
LANGFUSE_PUBLIC_KEY="your-langfuse-public-key"
LANGFUSE_SECRET_KEY="your-langfuse-secret-key"
LANGFUSE_HOST="https://cloud.langfuse.com"
```

Alternatively, you can set them directly in your terminal session.

## How It Works

This project is divided into four main examples, each demonstrating a different aspect of AI application development with Langfuse tracing.

### 1. Basic Tracing (`Basic_Tracing.py`)

This script shows the simplest way to integrate Langfuse into a Python application. It captures a single user-AI interaction in a chatbot, creating a trace that includes the user's question, the AI's response, and metadata about the model used.

### 2. Dialogue Follow-up System (`Dialogue_Followup_Langfuse.py`)

A more advanced example that uses **LangGraph** to create a stateful, multi-step workflow for handling dialogue. The system can ask single-choice or multiple-choice questions and intelligently interpret natural language answers. Each step in the workflow (displaying the question, collecting input, processing with AI, showing results) is traced as a nested observation in Langfuse, providing a detailed view of the entire process.

### 3. Langfuse Python SDK Demo (`PythonSDK.py`)

This script serves as a minimal, "Hello World" example for the Langfuse Python SDK. It demonstrates the core concepts of creating a trace and updating it with input and output, providing a clear starting point for custom integrations.

### 4. RAG Application (`RAG_Application.py`)

This is a complete Retrieval-Augmented Generation (RAG) pipeline built with **LangChain**. It demonstrates how to:

- Load and split text documents.
- Create vector embeddings and store them in a FAISS vector store.
- Retrieve relevant document chunks based on a user's question.
- Generate a context-aware answer using an LLM.

The entire pipeline is traced with Langfuse, offering deep insights into the performance of both the retrieval and generation steps.

## Usage

You can run each script individually from your terminal to see it in action. Make sure you have configured your environment variables as described in the **Configuration** section.

```sh
# Run the basic chatbot
python Basic_Tracing.py

# Run the dialogue follow-up demo
python Dialogue_Followup_Langfuse.py

# Run the simple SDK demo
python PythonSDK.py

# Run the RAG application
python RAG_Application.py
```

After running a script, check your Langfuse dashboard to see the generated traces and observations.

## Traces and Results

This repository includes screenshots of the Langfuse UI in the `images/` directory, showing what the traces and observations look like for these examples.

- **`Trace_Results.png`**: Shows a high-level view of the traces generated by the different scripts.
- **`Observation_Results.png`**: Provides a more detailed look at the nested observations within a single trace, such as the steps in the RAG or dialogue workflow.

These images illustrate how Langfuse helps you visualize and understand the inner workings of your AI applications.

## Contributing

Contributions are welcome! If you have suggestions for improvements or want to add new examples, please feel free to open an issue or submit a pull request.

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/YourFeature`).
3. Make your changes.
4. Commit your changes (`git commit -m 'Add some feature'`).
5. Push to the branch (`git push origin feature/YourFeature`).
6. Open a pull request.

## License

This project is licensed under the MIT License.
