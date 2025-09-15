# 🚀 Langfuse Project: Advanced AI Tracing & RAG Examples

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/release/python-380/)
[![Langfuse](https://img.shields.io/badge/Langfuse-Observability-blue)](https://langfuse.com/)
[![LangChain](https://img.shields.io/badge/LangChain-Integration-green)](https://www.langchain.com/)
[![LangGraph](https://img.shields.io/badge/LangGraph-Workflow-orange)](https://github.com/langchain-ai/langgraph)

Welcome to the **Langfuse Project**! This repository demonstrates best practices for building observable, robust, and production-ready AI applications in Python. It features:

- 🤖 **Chatbot Tracing**
- 🗂️ **Dialogue Follow-up Workflows**
- 📚 **Retrieval-Augmented Generation (RAG)**
- 📊 **Comprehensive Tracing & Monitoring**

All examples use the [Langfuse](https://langfuse.com/) tracing platform and the Silicon Flow API (OpenAI-compatible) for LLMs.

---

## 🗂️ Project Structure

```text
Langfuse_Project/
├── Basic_Tracing.py                                  # Simple chatbot with Langfuse tracing
├── Basic_Tracing.md                                  # Documentation for Basic_Tracing.py
├── Basic_Tracing_Trace.json                          # Example trace output
├── Dialogue_Followup_Langfuse.py                     # Dialogue system with LangGraph and Langfuse
├── Dialogue_Followup_Langfuse.md                     # Documentation for the dialogue system
├── Dialogue_Followup_Langfuse_Single_Trace.json      # Single-choice trace
├── Dialogue_Followup_Langfuse_Multiple_Trace.json    # Multiple-choice trace
├── Langfuse_Project_Summarization.md                 # Project summary and comparison
├── PythonSDK.py                                      # Basic Langfuse Python SDK usage demo
├── PythonSDK.md                                      # Documentation for PythonSDK.py
├── PythonSDK_Trace.json                              # Example SDK trace output
├── RAG_Application.py                                # RAG pipeline with LangChain and Langfuse
├── RAG_Application.md                                # Documentation for the RAG application
├── RAG_Application_Trace.json                        # Example RAG trace output
├── book.txt                                          # Sample text document for RAG
├── data.txt                                          # Additional data for RAG
├── LICENSE                                           # MIT License
├── README.md                                         # This file
└── images/
    ├── Observation_Results.png                       # Screenshot of Langfuse observation results
    └── Trace_Results.png                             # Screenshot of Langfuse trace results
```

---

## ✨ Features

- **End-to-End Tracing:** Full observability into AI workflows with Langfuse.
- **Chatbot Example:** Minimal chatbot with trace logging.
- **Dialogue System:** Multi-step workflow with LangGraph and nested tracing.
- **RAG Pipeline:** Document retrieval, embedding, and LLM-based QA with full traceability.
- **Professional Documentation:** Each script is paired with a detailed `.md` file.
- **Visual Results:** Example traces and screenshots included.

---

## ⚡ Quickstart

### 🛠️ Prerequisites

- Python 3.8 or higher
- Git

### 📦 Installation

1. **Clone the repository:**

   ```sh
   git clone https://github.com/ThomasAnderson-alt/Langfuse-Learning.git
   cd Langfuse-Learning
   ```

2. **Create a virtual environment (recommended):**

   ```sh
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**

   ```sh
   pip install openai langfuse langchain langgraph requests faiss-cpu
   ```

### 🔑 Configuration

Set your API keys as environment variables or in a `.env` file:

```env
SILICONFLOW_API_KEY=your-siliconflow-api-key
LANGFUSE_PUBLIC_KEY=your-langfuse-public-key
LANGFUSE_SECRET_KEY=your-langfuse-secret-key
LANGFUSE_HOST=https://cloud.langfuse.com
```

---

## 🏗️ File & Folder Guide

| File/Folder                                      | Description                                          |
| ------------------------------------------------ | ---------------------------------------------------- |
| `Basic_Tracing.py`                               | Minimal chatbot with Langfuse tracing                |
| `Basic_Tracing.md`                               | Documentation for the chatbot example                |
| `Basic_Tracing_Trace.json`                       | Example trace output for chatbot                     |
| `Dialogue_Followup_Langfuse.py`                  | Dialogue system with LangGraph and Langfuse          |
| `Dialogue_Followup_Langfuse.md`                  | Documentation for dialogue system                    |
| `Dialogue_Followup_Langfuse_Single_Trace.json`   | Single-choice trace example                          |
| `Dialogue_Followup_Langfuse_Multiple_Trace.json` | Multiple-choice trace example                        |
| `Langfuse_Project_Summarization.md`              | Project summary and Langfuse vs LangGraph comparison |
| `PythonSDK.py`                                   | Basic Langfuse Python SDK usage demo                 |
| `PythonSDK.md`                                   | Documentation for SDK demo                           |
| `PythonSDK_Trace.json`                           | Example SDK trace output                             |
| `RAG_Application.py`                             | RAG pipeline with LangChain and Langfuse             |
| `RAG_Application.md`                             | Documentation for RAG application                    |
| `RAG_Application_Trace.json`                     | Example RAG trace output                             |
| `book.txt`                                       | Sample text (A Christmas Carol) for RAG demo         |
| `data.txt`                                       | Additional data for RAG demo                         |
| `images/`                                        | Screenshots of Langfuse UI                           |
| `LICENSE`                                        | MIT License                                          |

---

## 🧑‍💻 Usage

Run any script directly after configuration:

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

Check your Langfuse dashboard for generated traces and observations.

---

## 🖼️ Visual Results

| Screenshot                                             | Description                       |
| ------------------------------------------------------ | --------------------------------- |
| ![Trace Results](images/Trace_Results.png)             | High-level view of traces         |
| ![Observation Results](images/Observation_Results.png) | Nested observations in a workflow |

---

## 🤝 Contributing

Contributions are welcome! Please open an issue or submit a pull request.

1. Fork the repository
2. Create a new branch (`git checkout -b feature/YourFeature`)
3. Make your changes
4. Commit (`git commit -m 'Add some feature'`)
5. Push (`git push origin feature/YourFeature`)
6. Open a pull request

---

## 📄 License

This project is licensed under the MIT License.
