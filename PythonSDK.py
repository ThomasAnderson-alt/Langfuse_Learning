"""
A simple Langfuse application using the Python SDK with proper traces and observations.
This example uses environment variables for authentication, following the recommended SDK usage.
"""

# Install the Langfuse SDK if not already installed:
# pip install langfuse

import os
import time
from langfuse import get_client

# Set your Langfuse credentials (or set these in your environment)
os.environ["LANGFUSE_PUBLIC_KEY"] = "pk-lf-e5f67ba8-e833-42c6-881d-7c78988b94d8"  # Replace with your public key
os.environ["LANGFUSE_SECRET_KEY"] = "sk-lf-2cc66109-728f-4865-8926-eb703da3ef76"  # Replace with your secret key
os.environ["LANGFUSE_HOST"] = "https://cloud.langfuse.com"  # Or your self-hosted URL

def main():
    langfuse = get_client()
    # Start a trace (observation)
    with langfuse.start_as_current_observation(
        name="Simple PythonSDK Trace",
        as_type="generation",
        model="demo-model",
        model_parameters={"temperature": "0.0"}
    ) as trace:
        # Add input observation
        user_input = "Hello, Langfuse!"
        trace.update(input=user_input)

        # Simulate processing
        time.sleep(1)
        result = "Hello, user! This is a response from Langfuse demo."

        # Add output observation
        trace.update(output=result)

    # Ensure all traces are sent to Langfuse UI
    langfuse.flush()
    print("Trace sent to Langfuse UI.")

if __name__ == "__main__":
    main()