# 🚀 Langfuse Project: Advanced AI Tracing & RAG Examples

![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python)
![Langfuse](https://img.shields.io/badge/Langfuse-Observability-blue?style=for-the-badge&logo=langfuse)
![LangChain](https://img.shields.io/badge/LangChain-Integration-green?style=for-the-badge&logo=langchain)
![LangGraph](https://img.shields.io/badge/LangGraph-Workflow-orange?style=for-the-badge&logo=langgraph)

## 📖 About The Project

The **Langfuse Project** demonstrates best practices for building observable, robust, and production-ready AI applications in Python. It features:

- 🤖 **Chatbot Tracing**
- 📂 **Dialogue Follow-up Workflows**
- 📚 **Retrieval-Augmented Generation (RAG)**
- 📊 **Comprehensive Tracing & Monitoring**

All examples use the [Langfuse](https://langfuse.com/) tracing platform and the Silicon Flow API (OpenAI-compatible) for LLMs.

## 🚀 Getting Started

Follow these steps to set up and run the project.

### Prerequisites

- Python 3.8 or higher
- Git

### Installation

1. **Clone the repository**

   ```sh
   git clone https://github.com/ThomasAnderson-alt/Langfuse_Project.git
   ```

2. **Navigate to the project directory**

   ```sh
   cd Langfuse_Project
   ```

3. **Create and activate a virtual environment**

   ```sh
   python -m venv venv
   .\venv\Scripts\activate
   ```

4. **Install dependencies**

   ```sh
   pip install -r requirements.txt
   ```

## ⚙️ Usage

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

## 📂 Project Structure

```plaintext
Langfuse_Project/
├── Basic_Tracing.py                  # Simple chatbot with Langfuse tracing
├── Dialogue_Followup_Langfuse.py     # Dialogue system with LangGraph and Langfuse
├── PythonSDK.py                      # Basic Langfuse Python SDK usage demo
├── RAG_Application.py                # RAG pipeline with LangChain and Langfuse
├── README.md                         # Project documentation
├── requirements.txt                  # Project dependencies
├── LICENSE                           # MIT License
├── images/                           # Screenshots of Langfuse UI
│   ├── Observation_Results.png       # Screenshot of Langfuse observation results
│   └── Trace_Results.png             # Screenshot of Langfuse trace results
```

## 🏗️ System Structure

The **Langfuse Project** is organized into distinct modules to ensure clarity and scalability. Below is an overview of the system structure:

1. **Tracing Module**: Demonstrates tracing capabilities using Langfuse (`Basic_Tracing.py`, `Dialogue_Followup_Langfuse.py`).
2. **SDK Module**: Provides examples of using the Langfuse Python SDK (`PythonSDK.py`).
3. **RAG Module**: Implements a Retrieval-Augmented Generation pipeline with LangChain and Langfuse (`RAG_Application.py`).
4. **Documentation Module**: Includes detailed Markdown files explaining the purpose and usage of each script.

This structure allows developers to focus on specific functionalities while maintaining a cohesive project design.

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.

Project Link: [https://github.com/ThomasAnderson-alt/Langfuse_Project](https://github.com/ThomasAnderson-alt/Langfuse_Project)
