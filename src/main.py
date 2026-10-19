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
