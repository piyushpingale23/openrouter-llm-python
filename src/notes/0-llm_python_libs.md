# Python Libraries Used in LLM Projects

## 1. OpenAI SDK

Used to communicate with LLM APIs such as OpenRouter.

Sends prompts and receives AI-generated responses.

```python
from openai import OpenAI
```

## 2. Pydantic

Used to define data models and validate data types and constraints.

Helps ensure that an LLM response follows the expected structure.

```python
from pydantic import BaseModel, Field, ValidationError
```

## 3. Requests

Used to send HTTP requests (GET, POST, etc.) to external APIs.

Example: calling the OpenWeather API to fetch current weather.

```python
import requests
```

## 4. os

Used to interact with operating-system features.

Here, it reads environment variables to access API keys.

```python
import os
```

## 5. json

Used to convert Python objects into JSON strings and JSON strings into Python objects. Useful when working with JSON API responses.

```python
import json
```

## 6. typing

Used to provide type hints and define expected data types.

`Literal` restricts a value to a predefined set of allowed options.

Example: `Literal["beginner", "intermediate", "advanced"]`

```python
from typing import Literal
```