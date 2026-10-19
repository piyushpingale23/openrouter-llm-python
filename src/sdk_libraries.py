# OpenAI SDK:
# Used to communicate with LLM APIs such as OpenRouter.
# Sends prompts and receives AI-generated responses.
from openai import OpenAI


# Pydantic:
# Used to define data models and validate data types and constraints.
# Helps ensure that an LLM response follows the expected structure.
from pydantic import BaseModel, Field, ValidationError


# Requests:
# Used to send HTTP requests (GET, POST, etc.) to external APIs.
# Example: calling the OpenWeather API to fetch current weather.
import requests


# os:
# Used to interact with operating-system features.
# Here, it reads environment variables to access API keys.
import os


# json:
# Used to convert Python objects into JSON strings and JSON strings
# into Python objects. Useful when working with JSON API responses.
import json


# typing:
# Used to provide type hints and define expected data types.
# Literal restricts a value to a predefined set of allowed options.
# Example: Literal["beginner", "intermediate", "advanced"]
from typing import Literal