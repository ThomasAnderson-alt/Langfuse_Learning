"""
Dialogue follow-up system with Langfuse tracing.
"""

import json
import time
import logging
from typing import Any, Dict, List, TypedDict
import requests
from langgraph.graph import StateGraph, END
from langfuse import Langfuse

# Configure logging
logging.basicConfig(level=logging.WARNING, format='%(asctime)s - %(levelname)s - %(message)s')

# API configuration constants
API_TIMEOUT = 30
SILICON_FLOW_BASE_URL = "https://api.siliconflow.cn/v1/chat/completions"
DEFAULT_MODEL_NAME = "Qwen/Qwen3-30B-A3B-Instruct-2507"

class DialogueState(TypedDict):
    """State structure for dialogue workflow."""
    question: str
    options: List[Dict[str, str]]
    question_type: str
    user_answer: str
    api_response: Dict[str, Any]
    parsed_result: Dict[str, Any]
    trace: Any  # Add trace to state

class VoiceFollowUp:
    """Main class for dialogue processing with AI and tracing."""

    def __init__(self, api_key: str, langfuse_public_key: str, langfuse_secret_key: str, model: str = DEFAULT_MODEL_NAME):
        """Initialize with API keys and model."""
        self.api_key = api_key
        self.model = model
        self.api_endpoint = SILICON_FLOW_BASE_URL

        # Initialize Langfuse
        self.langfuse = Langfuse(
            public_key=langfuse_public_key,
            secret_key=langfuse_secret_key
        )

        # Build workflow
        self.workflow = self._build_workflow()

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

    def _display_question_node(self, state: DialogueState) -> DialogueState:
        """Display question and options to user, and log observation as a nested step."""
        from langfuse import get_client
        langfuse = get_client()
        with langfuse.start_as_current_observation(
            name="display_question",
            as_type="generation",
            model=self.model,
            input={
                "question": state["question"],
                "options": state["options"],
                "question_type": state["question_type"]
            }
        ):
            print(f"\n{state['question_type'].title()}-Choice Question: {state['question']}")
            print("Available Options:")
            for option in state['options']:
                print(f"  {option['opt_code']}. {option['opt_content']}")
        return state

    def _collect_input_node(self, state: DialogueState) -> DialogueState:
        """Collect user input for the question and log observation as a nested step."""
        from langfuse import get_client
        langfuse = get_client()
        with langfuse.start_as_current_observation(
            name="collect_input",
            as_type="generation",
            model=self.model
        ) as obs:
            user_input = input("\nPlease enter your answer: ").strip()
            state["user_answer"] = user_input
            obs.update(output={"user_answer": user_input})
        return state

    def _process_api_node(self, state: DialogueState) -> DialogueState:
        """Process user answer via AI API and log observation as a nested step."""
        from langfuse import get_client
        langfuse = get_client()
        with langfuse.start_as_current_observation(
            name="process_api",
            as_type="generation",
            model=self.model,
            input={
                "question": state["question"],
                "options": state["options"],
                "user_answer": state["user_answer"],
                "question_type": state["question_type"]
            }
        ) as obs:
            print("Processing your answer...")
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
            obs.update(output={
                "api_response": api_result,
                "parsed_result": parsed_data
            })
            # Update state
            state.update({
                "api_response": api_result,
                "parsed_result": parsed_data
            })
        return state

    def _display_result_node(self, state: DialogueState) -> DialogueState:
        """Display the API processing results and log observation as a nested step."""
        from langfuse import get_client
        langfuse = get_client()
        data = state["parsed_result"]
        with langfuse.start_as_current_observation(
            name="display_result",
            as_type="generation",
            model=self.model,
            input=data
        ):
            print(f"\n{'='*30} RESULTS {'='*30}")
            print(f"Best Match Found!")
            print(f"Option: {data.get('option_code', 'N/A')} - {data.get('option_content', 'N/A')}")
        return state

    def _build_api_payload(self, question: str, options: List[Dict[str, str]], answer: str, question_type: str) -> Dict[str, Any]:
        """Build API request payload."""
        options_str = "\n".join(f"{opt['opt_code']}. {opt['opt_content']}" for opt in options)

        system_prompt = f"""You are an expert at matching user answers to predefined options.
Given a {question_type}-choice question and the user's natural language answer, identify which option(s) best matches the user's response.

CRITICAL MATCHING RULES:
1. Match based on EXACT keywords and synonyms, not semantic similarity
2. "runny nose" should match "Runny nose" NOT "Sneezing" 
3. "tired" or "fatigue" should match "General weakness"
4. Only select options that have clear keyword/synonym matches in the user's text
5. Be precise - don't assume related symptoms are the same

Return your response as a JSON object with this structure:
{{"option_code": "1", "option_content": "Option text"}}

For multiple options, use comma-separated values like "1,2,3"."""

        user_prompt = f"""Question: {question}
Available options:
{options_str}
User's answer: "{answer}"

Analyze the user's answer and match it to the most appropriate option(s) based on exact keyword matches:
- Look for direct keyword matches (e.g., "headache" matches "Headache")  
- Consider common synonyms (e.g., "tired" matches "General weakness")
- Do NOT match based on medical similarity (e.g., "runny nose" is not "Sneezing")
- Only select options that have clear textual evidence in the user's response

Return the result in JSON format."""

        return {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": 0.0,
            "max_tokens": 500
        }

    def process_question(self, question: str, options: List[Dict[str, str]], question_type: str) -> Dict[str, Any]:
        """Process a question through the workflow with Langfuse tracing using the correct SDK pattern."""
        from langfuse import get_client
        langfuse = get_client()
        with langfuse.start_as_current_observation(
            name="Dialogue Followup",
            as_type="generation",
            input={
                "question": question,
                "options": options,
                "question_type": question_type
            }
        ) as trace:
            initial_state = DialogueState(
                question=question,
                options=options,
                question_type=question_type,
                user_answer="",
                api_response={},
                parsed_result={},
                trace=trace
            )
            result = self.workflow.invoke(initial_state)
            # Log output at the end of the workflow
            trace.update(output=result)
        return result

def run_demo():
    """Run demo with example questions."""
    # Use environment variables for API keys in production
    API_KEY = "sk-lmzcznwaldljlkfyuauzbwijxlfaffkxasaeioyolscngoyi"
    LANGFUSE_PUBLIC_KEY = "pk-lf-e5f67ba8-e833-42c6-881d-7c78988b94d8"
    LANGFUSE_SECRET_KEY = "sk-lf-2cc66109-728f-4865-8926-eb703da3ef76"

    # Initialize client
    dialogue_client = VoiceFollowUp(API_KEY, LANGFUSE_PUBLIC_KEY, LANGFUSE_SECRET_KEY)

    print("\n" + "="*60)
    print("DIALOGUE FOLLOW-UP DEMO")
    print("="*60)

    # Single-choice question
    print("\nSingle-Choice Question")
    dialogue_client.process_question(
        "Do you drink alcohol regularly?",
        [
            {"opt_code": "1", "opt_content": "Frequently"},
            {"opt_code": "2", "opt_content": "Occasionally"},
            {"opt_code": "3", "opt_content": "Never"}
        ],
        "single"
    )

    # Pause between examples
    print(f"\n{'='*60}\nWaiting 5 seconds before the next question...")
    time.sleep(5)

    # Multiple-choice question
    print("\nMultiple-Choice Question")
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

    print("\n" + "="*60)
    print("Demo completed successfully!")

    # Flush traces
    dialogue_client.langfuse.flush()

if __name__ == "__main__":
    run_demo()
