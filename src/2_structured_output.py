import json
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, ValidationError

from openai import OpenAI

MODEL_NAME = "openai/gpt-4o-mini"

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=__import__("os").environ["OPENROUTER_API_KEY"],
)


# Schema Definition
class ConceptExplanation(BaseModel):
    model_config = ConfigDict(extra="forbid")

    topic: str = Field(
        description="Name of the concept being explained"
    )

    summary: str = Field(
        description="A concise explanation in beginner-friendly language"
    )

    difficulty: Literal[
        "beginner", "intermediate", "advanced"
    ]

    key_points: list[str] = Field(
        min_length=2,
        description="Important ideas the learner should remember",
    )

    example: str = Field(
        description="One practical example"
    )

    confidence: float = Field(
        ge=0,
        le=1,
        description="Confidence score between 0 and 1",
    )


if __name__ == "__main__":
    # Generate the JSON schema from the Pydantic model.
    schema = ConceptExplanation.model_json_schema()

    print("Generated JSON Schema:")
    print(json.dumps(schema, indent=2))

    # Request a structured response from the LLM.
    structured_response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an AI instructor. Explain concepts "
                    "clearly and return data matching the supplied "
                    "JSON schema."
                ),
            },
            {
                "role": "user",
                "content": "Explain Java in simple language.",
            },
        ],
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "concept_explanation",
                "strict": True,
                "schema": schema,
            },
        },
        temperature=0,
    )

    structured_text = (
        structured_response.choices[0].message.content
    )

    if not structured_text:
        raise RuntimeError("The LLM returned an empty response.")

    print("\nRaw structured response:")
    print(structured_text)

    # Validate the generated JSON against the Pydantic model.
    try:
        concept = ConceptExplanation.model_validate_json(
            structured_text
        )

        print("\nResponse passed Pydantic validation")
        print(concept.model_dump_json(indent=2))

    except ValidationError as exc:
        print("\nResponse failed Pydantic validation")
        print(exc)

# ============================================================
# Basic Concepts
# ============================================================
#
# 1. LLM (Large Language Model):
#    An AI model that understands and generates human-like text.
#    Here, we use openai/gpt-4o-mini to explain Java.
#
# 2. OpenRouter(API Provider):
#    A platform that provides a unified API to access different LLMs.
#    It routes our request to the selected model and returns its response.
#
# 3. OpenAI Python SDK:
#    A Python library used to communicate with APIs that follow the
#    OpenAI API format. OpenRouter supports this format, allowing us
#    to use the OpenAI SDK to communicate with its API.
#
# 4. Pydantic:
#    A Python library used for data validation, type checking,
#    constraints, and serialization.
#
# 5. Pydantic Response Model:
#    A Python class that inherits from Pydantic's BaseModel and defines
#    the expected structure of the data our application wants to receive.
#
#    Here, ConceptExplanation defines the fields expected in the LLM response:
#    topic, summary, difficulty, key_points, example, and confidence.
#
#    Each field has a data type and may have additional constraints.
#    For example:
#    - topic must be a string.
#    - difficulty must be one of the allowed Literal values.
#    - key_points must contain at least two items.
#    - confidence must be between 0 and 1.
#
# 6. JSON Schema:
#    A standard JSON-based definition describing the expected data structure,
#    including fields, data types, and constraints.
#
#    Pydantic can generate this schema from the ConceptExplanation class.
#    We send it to the LLM so the model knows the required response format.
#
# 7. Structured Output:
#    Instead of requesting an ordinary text response, we request a response
#    that follows the specified JSON Schema.
#
# ============================================================
# Execution Flow
# ============================================================
#
# Step 1: Initialize the OpenAI SDK client with the OpenRouter base URL
#         and the API key stored in the environment variable.
#
# Step 2: Define ConceptExplanation, our Pydantic Response Model.
#         It specifies the expected fields, data types, and constraints.
#
# Step 3: Call model_json_schema() to convert the Pydantic model
#         definition into a JSON Schema.
#
# Step 4: Send the user prompt ("Explain Java in simple language"),
#         system instructions, and JSON Schema to OpenRouter.
#
# Step 5: OpenRouter forwards the request to the selected LLM.
#         The LLM generates a response in the requested structured format.
#
# Step 6: Extract the generated JSON text from the API response.
#
# Step 7: Call model_validate_json() to parse the JSON and validate it
#         against the ConceptExplanation Pydantic model.
#
# Step 8: If validation succeeds, we get a ConceptExplanation Python object.
#         Call model_dump_json() to serialize that object back into JSON.
#
# Step 9: If validation fails, catch ValidationError and print the details.
#
# Important:
#    The JSON Schema guides the LLM to produce the requested structure.
#    Pydantic validates the response in our Python application.
#    These are separate responsibilities.
#
#    Successful validation confirms that the response follows the defined
#    structural rules. It does not guarantee that the explanation is factual.
#
# ============================================================
# Overall Flow
# ============================================================
#
# Define Pydantic Model
#          |
#          v
# Generate JSON Schema
#          |
#          v
# Send Prompt + Schema to OpenRouter
#          |
#          v
# OpenRouter Routes Request to LLM
#          |
#          v
# LLM Generates Structured JSON Response
#          |
#          v
# Extract JSON Text
#          |
#          v
# Pydantic Validates JSON
#          |
#     +----+----+
#     |         |
#     v         v
#  Success    Failure
#     |         |
#     v         v
# Python     ValidationError
# Object     Details
#     |
#     v
# Serialize and Print JSON
