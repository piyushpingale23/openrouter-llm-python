import getpass
import os

from openai import OpenAI

MODEL_NAME = "openai/gpt-4o-mini"
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"


def get_api_key() -> str:
    """Read the API key from the environment"""
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        api_key = getpass.getpass("Enter your OpenRouter API key: ").strip()

    if not api_key:
        raise ValueError(
            "No API key provided. Set OPENROUTER_API_KEY or enter it when prompted."
        )

    return api_key


def main() -> None:
    """Create the client, send a prompt, and print the model response."""
    client = OpenAI(
        base_url=OPENROUTER_BASE_URL,
        api_key=get_api_key(),
    )
    print(f"Client initialized. Model: {MODEL_NAME}")

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": "What is Java?",
            }
        ],
        temperature=0.2,
        top_p=0.9,
        max_tokens=25,
    )

    answer = response.choices[0].message.content
    print("\nModel response:")
    print(answer if answer else "(The model returned an empty response.)")


if __name__ == "__main__":
    main()

# Basic Concepts:
#
# 1. LLM (Large Language Model):
#    An AI model trained on large amounts of data to understand and
#    generate human-like text. Examples include GPT, Claude, and Gemini.
#
# 2. OpenRouter (API Provider):
#    A platform that provides a unified API to access different LLMs
#    through a single endpoint. It handles communication with the
#    selected model and returns its response.
#
# 3. OpenAI Python SDK:
#    A Python library used to communicate with APIs that follow the
#    OpenAI API format. OpenRouter supports this format, so we can use
#    the OpenAI SDK to send requests to OpenRouter.
#
# 4. API Key:
#    A secret credential used to authenticate our application with
#    OpenRouter.
#
# 5. OpenAI Client:
#    The client object configured with OpenRouter's base URL and API key.
#    It allows our Python application to send requests to OpenRouter.
#
# 6. Model Name:
#    Identifies the LLM we want to use. Here, "openai/gpt-4o-mini"
#    specifies the selected model through OpenRouter.
#
# Execution Flow:
#
# 1. Read the OpenRouter API key from the environment variable.
#    If it is unavailable, securely prompt the user to enter it.
#
# 2. Initialize the OpenAI client with the OpenRouter base URL and API key.
#
# 3. Send the user's prompt ("What is Java?") to the selected LLM
#    using the chat completions API.
#
# 4. Configure the response using temperature, top_p, and max_tokens.
#
# 5. OpenRouter routes the request to the selected LLM.
#
# 6. The LLM generates a response, which OpenRouter returns to our
#    Python application through the API.
#
# 7. Extract the assistant's response from the API result and print it.
#
# Overall Flow:
# User Prompt
#     -> Python Application
#     -> OpenAI Python SDK
#     -> OpenRouter API
#     -> Selected LLM
#     -> OpenRouter API
#     -> Python Application
#     -> Display Response
