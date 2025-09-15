# Langfuse Project: AI Tracing & RAG Examples

This repository demonstrates practical usage of the [Langfuse](https://langfuse.com/) tracing platform in Python AI applications, including chatbot tracing, dialogue follow-up, and Retrieval-Augmented Generation (RAG) with full observability. It features integration with Silicon Flow (OpenAI-compatible) APIs and Langfuse for monitoring, debugging, and quality assurance.

## Table of Contents

- [Project Structure](#project-structure)
- [File Summaries](#file-summaries)
- [Setup & Requirements](#setup--requirements)
- [Usage](#usage)
- [Traces & Results](#traces--results)
- [References](#references)

---

## Project Structure

```
Langfuse_Project/
├── Basic_Tracing.py
├── Basic_Tracing.md
├── Basic_Tracing_Trace.json
├── Dialogue_Followup_Langfuse.py
├── Dialogue_Followup_Langfuse.md
├── Dialogue_Followup_Langfuse_Single_Trace.json
├── Dialogue_Followup_Langfuse_Multiple_Trace.json
├── Langfuse_Project_Summarization.md
├── PythonSDK.py
├── PythonSDK.md
├── PythonSDK_Trace.json
├── RAG_Application.py
├── RAG_Application.md
├── RAG_Application_Trace.json
├── data.txt
├── images/
│   ├── Observation_Results.png
│   └── Trace_Results.png
```

---

## File Summaries

### 1. `Basic_Tracing.py` / `Basic_Tracing.md` / `Basic_Tracing_Trace.json`

- **Purpose:** Minimal chatbot using Silicon Flow API and Langfuse for tracing. Logs user input, model response, and trace data for observability.
- **Trace Example:** See `Basic_Tracing_Trace.json` for a sample trace of a user asking about South Africa's capitals.

### 2. `Dialogue_Followup_Langfuse.py` / `Dialogue_Followup_Langfuse.md` / `Dialogue_Followup_Langfuse_Single_Trace.json` / `Dialogue_Followup_Langfuse_Multiple_Trace.json`

- **Purpose:** Dialogue follow-up system supporting single/multiple-choice questions, workflow orchestration with LangGraph, and full traceability with Langfuse.
- **Trace Examples:**
  - `Dialogue_Followup_Langfuse_Single_Trace.json`: Single-choice question trace.
  - `Dialogue_Followup_Langfuse_Multiple_Trace.json`: Multiple-choice question trace.

### 3. `PythonSDK.py` / `PythonSDK.md` / `PythonSDK_Trace.json`

- **Purpose:** Demonstrates basic Langfuse Python SDK usage for creating and managing traces (observations) in AI applications.
- **Trace Example:** See `PythonSDK_Trace.json` for a simple trace of a demo input/output.

### 4. `RAG_Application.py` / `RAG_Application.md` / `RAG_Application_Trace.json`

- **Purpose:** Complete Retrieval-Augmented Generation (RAG) pipeline using LangChain, with document loading, embedding, retrieval, and answer generation. All steps are traced with Langfuse.
- **Trace Example:** See `RAG_Application_Trace.json` for a sample RAG pipeline trace.

### 5. `data.txt`

- **Purpose:** Sample document for RAG application. Contains basic explanations of AI, Machine Learning, and Deep Learning.

### 6. `images/`

- **Observation_Results.png:** Screenshot of Langfuse observation results.
- **Trace_Results.png:** Screenshot of Langfuse trace results.

### 7. `Langfuse_Project_Summarization.md`

- **Purpose:** High-level summary and documentation of all project scripts and their tracing logic.

---

## Setup & Requirements

- Python 3.8+
- Install dependencies:

  ```sh
  pip install -r requirements.txt
  # or install individually:
  pip install langfuse openai langchain langgraph
  ```

- Set environment variables for Silicon Flow and Langfuse API keys (see code comments).

## Usage

- Run any script directly, e.g.:

  ```sh
  python Basic_Tracing.py
  python Dialogue_Followup_Langfuse.py
  python PythonSDK.py
  python RAG_Application.py
  ```

- Follow prompts in the console. Traces will be sent to your Langfuse dashboard.

## Traces & Results

- Example trace outputs are provided as `.json` files for each script.
- Visual results can be found in the `images/` folder.

## References

- [Langfuse Documentation](https://langfuse.com/docs)
- [Silicon Flow API](https://api.siliconflow.cn/)
- [LangChain](https://python.langchain.com/)

---

_This repository is for educational and demonstration purposes. Replace API keys with your own for production use._