# Dialogue Follow-up System with Langfuse Tracing

## Overview

This Python application implements an AI-powered dialogue follow-up system that can process both single-choice and multiple-choice questions. The system uses the Silicon Flow API for AI processing and integrates with Langfuse for comprehensive tracing and monitoring. The application is built using LangGraph for workflow orchestration.

## System Architecture

The system is designed around a state-based workflow that processes user interactions through a series of defined nodes:

Display Question → Collect Input → Process API → Display Result

## Key Components

### 1. Core Classes and Data Structures

#### DialogueState (TypedDict)

```python
class DialogueState(TypedDict):
    """State structure for dialogue workflow."""
    question: str
    options: List[Dict[str, str]]
    question_type: str
    user_answer: str
    api_response: Dict[str, Any]
    parsed_result: Dict[str, Any]
    trace: Any  # Add trace to state
```

**Purpose**: This TypedDict defines the state structure that flows through the entire workflow. It maintains all necessary information about the current dialogue session including the question, available options, user responses, and API results.

#### VoiceFollowUp Class

The main class that orchestrates the entire dialogue processing system.

```python
class VoiceFollowUp:
    """Main class for dialogue processing with AI and tracing."""

    def __init__(self, api_key: str, langfuse_public_key: str, langfuse_secret_key: str, model: str = DEFAULT_MODEL_NAME):
```

**Purpose**: Initializes the dialogue system with:

- API credentials for Silicon Flow
- Langfuse credentials for tracing
- Model configuration
- Workflow setup

## Step-by-Step Functionality

### Step 1: System Initialization

```python
def __init__(self, api_key: str, langfuse_public_key: str, langfuse_secret_key: str, model: str = DEFAULT_MODEL_NAME):
    """Initialize with API keys and model."""
    self.api_key = api_key
    self.model = model
    self.api_endpoint = SILICON_FLOW_BASE_URL

    # Initialize Langfuse
    self.langfuse = Langfuse(
        public_key=langfuse_public_key,
        secret_key=langfuse_secret_key

     Integrates Langfuse for complete observability
     **Every workflow step is logged as a Langfuse observation:**
     - **display_question**: Logs the question and options shown to the user.
     - **collect_input**: Logs the user's input as an observation.
     - **process_api**: Logs the API request and the parsed AI response.
     - **display_result**: Logs the final result shown to the user.

     Each of these steps is wrapped in a Langfuse observation using the Python SDK's `start_as_current_observation` context manager with `as_type="generation"`. This provides a detailed trace tree in the Langfuse UI, allowing you to monitor, debug, and analyze every part of the dialogue workflow.
```

**What it does**:

1. Stores API credentials securely
2. Sets up the Silicon Flow endpoint for AI processing
3. Initializes Langfuse client for tracing and monitoring
4. Builds the complete workflow graph

### Step 2: Workflow Construction

```python
def _build_workflow(self) -> Any:
    """Build the LangGraph workflow."""
    workflow = StateGraph(DialogueState)

    # Define workflow nodes
    nodes = [
        ("display_question", self._display_question_node),
        ("collect_input", self._collect_input_node),
        ("process_api", self._process_api_node),
        ("display_result", self._display_result_node)
    ]

    for node_name, node_func in nodes:
        workflow.add_node(node_name, node_func)

    # Set entry point
    workflow.set_entry_point("display_question")

    # Define transitions
    edges = [
        ("display_question", "collect_input"),
        ("collect_input", "process_api"),
        ("process_api", "display_result"),
        ("display_result", END)
    ]

    for from_node, to_node in edges:
        workflow.add_edge(from_node, to_node)

    return workflow.compile()
```

**What it does**:

1. Creates a state graph using the DialogueState structure
2. Defines four processing nodes with their corresponding functions
3. Sets up the workflow sequence: display → collect → process → display results
4. Compiles the workflow into an executable graph

### Step 3: Question Display Node

```python
def _display_question_node(self, state: DialogueState) -> DialogueState:
    """Display question and options to user."""
    print(f"\n{state['question_type'].title()}-Choice Question: {state['question']}")
    print("Available Options:")
    for option in state['options']:
        print(f"  {option['opt_code']}. {option['opt_content']}")
    return state
```

**What it does**:

1. Formats and displays the question type (Single/Multiple-Choice)
2. Shows the main question text
3. Lists all available options with their codes
4. Returns the unchanged state to continue the workflow

### Step 4: Input Collection Node

```python
def _collect_input_node(self, state: DialogueState) -> DialogueState:
    """Collect user input for the question."""
    user_input = input("\nPlease enter your answer: ").strip()
    state["user_answer"] = user_input
    return state
```

**What it does**:

1. Prompts the user for their response
2. Collects and cleans the input (removes whitespace)
3. Updates the state with the user's answer
4. Passes the updated state to the next node

### Step 5: API Processing Node

```python
def _process_api_node(self, state: DialogueState) -> DialogueState:
    """Process user answer via AI API."""
    print("Processing your answer...")

    # Make API request
    response = requests.post(
        self.api_endpoint,
        headers={
            "Content-Type": "application/json; charset=utf-8",
            "Authorization": f"Bearer {self.api_key}"
        },
        json=self._build_api_payload(
            state["question"],
            state["options"],
            state["user_answer"],
            state["question_type"]
        ),
        timeout=API_TIMEOUT
    )
    response.raise_for_status()

    api_result = response.json()
    parsed_data = json.loads(api_result['choices'][0]['message']['content'])

    # Update state
    state.update({
        "api_response": api_result,
        "parsed_result": parsed_data
    })

    return state
```

**What it does**:

1. Builds a comprehensive API request payload
2. Sends the request to Silicon Flow's AI API with proper authentication
3. Handles the response and extracts the AI's analysis
4. Parses the JSON response from the AI
5. Updates the state with both raw API response and parsed results

### Step 6: API Payload Construction

```python
def _build_api_payload(self, question: str, options: List[Dict[str, str]], answer: str, question_type: str) -> Dict[str, Any]:
    """Build API request payload."""
    options_str = "\n".join(f"{opt['opt_code']}. {opt['opt_content']}" for opt in options)

    system_prompt = f"""You are an expert at matching user answers to predefined options.
Given a {question_type}-choice question and the user's natural language answer, identify which option(s) best matches the user's response.

Return your response as a JSON object with this structure:
{{"option_code": "1", "option_content": "Option text"}}

For multiple options, use comma-separated values like "1,2,3"."""

    user_prompt = f"""Question: {question}
Available options:
{options_str}
User's answer: "{answer}"

Please match the user's answer to the most appropriate option(s) and return the result in JSON format."""

    return {
        "model": self.model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.0,
        "max_tokens": 500
    }
```

**What it does**:

1. Formats all available options into a readable string
2. Creates a detailed system prompt that instructs the AI on its role
3. Builds a user prompt with the question, options, and user's natural language answer
4. Structures the complete API payload with model parameters
5. Sets temperature to 0.0 for consistent, deterministic responses

### Step 7: Results Display Node

```python
def _display_result_node(self, state: DialogueState) -> DialogueState:
    """Display the API processing results."""
    data = state["parsed_result"]
    print(f"\n{'='*30} RESULTS {'='*30}")
    print(f"Best Match Found!")
    print(f"Option: {data.get('option_code', 'N/A')} - {data.get('option_content', 'N/A')}")
    return state
```

**What it does**:

1. Extracts the parsed results from the state
2. Formats and displays the AI's analysis
3. Shows the matched option code and content
4. Uses safe dictionary access to handle missing data

### Step 8: Question Processing Interface

```python
def process_question(self, question: str, options: List[Dict[str, str]], question_type: str) -> Dict[str, Any]:
    """Process a question through the workflow."""
    initial_state = DialogueState(
        question=question,
        options=options,
        question_type=question_type,
        user_answer="",
        api_response={},
        parsed_result={},
        trace=None
    )
    return self.workflow.invoke(initial_state)
```

**What it does**:

1. Creates an initial state with the provided question parameters
2. Initializes empty fields for user responses and API results
3. Invokes the complete workflow with the initial state
4. Returns the final processed state

## Demo Implementation

### Demo Function

```python
def run_demo():
    """Run demo with example questions."""
    # Use environment variables for API keys in production
    API_KEY = "sk-lmzcznwaldljlkfyuauzbwijxlfaffkxasaeioyolscngoyi"
    LANGFUSE_PUBLIC_KEY = "pk-lf-e5f67ba8-e833-42c6-881d-7c78988b94d8"
    LANGFUSE_SECRET_KEY = "sk-lf-2cc66109-728f-4865-8926-eb703da3ef76"

    # Initialize client
    dialogue_client = VoiceFollowUp(API_KEY, LANGFUSE_PUBLIC_KEY, LANGFUSE_SECRET_KEY)
```

**What it does**:

1. Sets up API credentials (should use environment variables in production)
2. Creates an instance of the VoiceFollowUp system
3. Demonstrates both single-choice and multiple-choice question processing

### Example Question Processing

#### Single-Choice Question

```python
dialogue_client.process_question(
    "Do you drink alcohol regularly?",
    [
        {"opt_code": "1", "opt_content": "Frequently"},
        {"opt_code": "2", "opt_content": "Occasionally"},
        {"opt_code": "3", "opt_content": "Never"}
    ],
    "single"
)
```

#### Multiple-Choice Question

```python
dialogue_client.process_question(
    "What are your symptoms?",
    [
        {"opt_code": str(i+1), "opt_content": symptom}
        for i, symptom in enumerate([
            "Headache", "Dizziness", "Blurred vision", "Sore throat", "Sneezing",
            "Runny nose", "Nasal congestion", "Chest tightness", "General weakness"
        ])
    ],
    "multiple"
)
```

## How the Program Achieves User Goals

### 1. Natural Language Understanding

- Accepts user responses in natural language rather than requiring specific option codes
- Uses AI to interpret and match responses to predefined options
- Handles both single and multiple selections intelligently

### 2. Workflow Orchestration

- Uses LangGraph to create a clear, maintainable workflow
- Each step has a specific responsibility and clear state transitions
- Easy to modify, extend, or debug individual components

### 3. Comprehensive Tracing

- Integrates Langfuse for complete observability
- Tracks all API calls, user interactions, and system responses
- Enables monitoring, debugging, and performance analysis

### 4. Robust Error Handling

- Implements timeout protection for API calls
- Uses proper HTTP status checking
- Gracefully handles missing data with fallback values

### 5. Flexible Question Types

- Supports both single-choice and multiple-choice questions
- Dynamically generates option lists
- Adapts AI prompts based on question type

## Configuration Constants

```python
# API configuration constants
API_TIMEOUT = 30
SILICON_FLOW_BASE_URL = "https://api.siliconflow.cn/v1/chat/completions"
DEFAULT_MODEL_NAME = "Qwen/Qwen3-30B-A3B-Instruct-2507"
```

These constants provide:

- Timeout protection for API calls
- Configurable API endpoint
- Default AI model selection

## Key Benefits

1. **User-Friendly**: Accepts natural language responses instead of rigid option codes
2. **Intelligent Matching**: Uses AI to understand intent and match to appropriate options
3. **Traceable**: Full observability through Langfuse integration
4. **Scalable**: Easy to add new question types or modify workflow steps
5. **Robust**: Proper error handling and timeout protection
6. **Maintainable**: Clear separation of concerns and well-documented code

This system effectively bridges the gap between natural human communication and structured data collection, making it ideal for surveys, medical questionnaires, customer feedback, and other applications requiring intelligent response processing.
