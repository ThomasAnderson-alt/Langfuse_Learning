# Import libraries
from openai import OpenAI
from langfuse import get_client
import os

# Configure Silicon Flow
# Set the API key and the *new* base URL for the client
os.environ["SILICONFLOW_API_KEY"] = "sk-lmzcznwaldljlkfyuauzbwijxlfaffkxasaeioyolscngoyi"

client = OpenAI(
    api_key=os.getenv("SILICONFLOW_API_KEY"),
    base_url="https://api.siliconflow.cn/v1"  # <- This is the critical change
)

# Configure Langfuse
os.environ["LANGFUSE_PUBLIC_KEY"] = "pk-lf-e5f67ba8-e833-42c6-881d-7c78988b94d8"
os.environ["LANGFUSE_SECRET_KEY"] = "sk-lf-2cc66109-728f-4865-8926-eb703da3ef76"
os.environ["LANGFUSE_HOST"] = "https://cloud.langfuse.com"

langfuse = get_client()

# Start Langfuse trace
with langfuse.start_as_current_observation( # start_as_current_generation will be deprecated in the future, so use start_as_current_observation instead
    name="Basic Chatbot Interaction",
    as_type="generation",
    model="zai-org/GLM-4.5V",
    model_parameters={
        "temperature": "0.0"
    }
) as trace:
    # Get user input
    user_question = input("Enter your question: ")
    
    # Make the API call to Silicon Flow instead of OpenAI
    completion = client.chat.completions.create(
        model="zai-org/GLM-4.5V",
        messages=[
            {"role": "user", "content": user_question}
        ]
    )

    # Get the response
    response_content = completion.choices[0].message.content
    print(response_content)

    # Update the Langfuse trace with the output
    trace.update( input=user_question, output=response_content)

# Ensure data is flushed
langfuse.flush()