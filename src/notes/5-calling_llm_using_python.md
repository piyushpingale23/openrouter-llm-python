# Calling an LLM Using Python

---

## 1. What Are We Doing?

We are calling a Large Language Model (LLM) from a Python application using an API.

For example, we send the prompt `"Explain Java"` to an LLM and receive a generated response.

**Basic flow:**

```text
Python Application
        |
        | Prompt + Model Configuration
        v
   HTTP Request
        |
        v
   OpenRouter API
        |
        | Routes the request
        v
    Selected LLM
        |
        | Generates a response
        v
   OpenRouter API
        |
        | HTTP Response
        v
  Python Application
        |
        v
  Extract and Print Answer
```

Important concepts:

- **LLM:** The model that generates the answer.
- **API provider:** The service through which we access the model.
- **API:** An interface that allows applications to communicate.
- **HTTP request:** The request sent to the API.
- **HTTP response:** The result returned by the API.
- **Inference:** Using an already-trained model to generate an answer.

We are performing inference, not training the model.

---

## 2. OpenAI, OpenRouter, and the OpenAI Python SDK

These are three different things.

### 2.1 OpenAI

OpenAI develops AI models and provides APIs for accessing supported models.

### 2.2 OpenRouter

OpenRouter provides a unified API through which applications can access models from different providers.

For example:

```python
model="openai/gpt-4o-mini"
```

This model identifier tells OpenRouter which model to use, subject to availability.

### 2.3 OpenAI Python SDK

The OpenAI Python SDK is a Python client library that simplifies API communication.

It handles tasks such as:

- Constructing HTTP requests.
- Serializing request data.
- Sending requests.
- Parsing responses.
- Providing structured Python objects.

Although the SDK is designed for OpenAI APIs, it can also communicate with compatible API endpoints when configured appropriately.

### Overall relationship

```text
Python Application
        |
        v
OpenAI Python SDK
        |
        | base_url
        v
   OpenRouter API
        |
        v
    Selected LLM
```

The SDK is the client library, OpenRouter is the API provider, and the selected LLM generates the answer.

---

## 3. Install the Required Libraries

```bash
pip install openai requests
```

Explanation:

- `pip install`: Installs Python packages.
- `openai`: Provides the OpenAI Python SDK.
- `requests`: Provides functions for sending HTTP requests.

The `requests` library is not required if you use only the SDK approach.

In notebook environments such as Google Colab, you can use `!pip install` to run the installation command.

---

## 4. Configure the API Key

An API key is a secret credential used to authenticate API requests.

```python
import os
import getpass

if not os.environ.get("OPENROUTER_API_KEY"):
    os.environ["OPENROUTER_API_KEY"] = getpass.getpass(
        "Enter your OpenRouter API key: "
    )

print("OpenRouter API key loaded")
```

### 4.1 `os`

The `os` module provides access to operating-system-related functionality, including environment variables.

```
os.environ.get("OPENROUTER_API_KEY")
```

Checks whether the environment variable exists.

```
os.environ["OPENROUTER_API_KEY"] = "some_value"
```

Sets the environment variable for the current Python process.

### 4.2 `getpass`

```
getpass.getpass("Enter your OpenRouter API key: ")
```

Accepts secret input without displaying the typed characters in a normal terminal or notebook prompt.

### Why use environment variables?

Instead of hardcoding an API key in source code, we load it from an environment variable.

This reduces the risk of accidentally sharing the key when publishing or sharing source code.

Important:

- Do not commit API keys to GitHub.
- Do not print API keys in notebook output.
- Environment variables set this way are not necessarily persistent across sessions.
- Never share an active API key publicly.

---

# 5. Approach 1: Calling an LLM Using the OpenAI Python SDK

The SDK provides a high-level interface for making API requests.

## 5.1 Complete Example

```python
import os
import getpass
from openai import OpenAI

if not os.environ.get("OPENROUTER_API_KEY"):
    os.environ["OPENROUTER_API_KEY"] = getpass.getpass(
        "Enter your OpenRouter API key: "
    )

MODEL_NAME = "openai/gpt-4o-mini"

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"],
)

response = client.chat.completions.create(
    model=MODEL_NAME,
    messages=[
        {
            "role": "user",
            "content": "Explain Java in simple terms."
        }
    ],
    temperature=0.2,
    top_p=0.9,
    max_tokens=150,
)

answer = response.choices[0].message.content
print(answer)
```

## 5.2 Initialize the Client

```
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"],
)
```

### `base_url`

Specifies the API endpoint used by the SDK.

```python
base_url="https://openrouter.ai/api/v1"
```

This configures the client to communicate with OpenRouter instead of the default OpenAI API endpoint.

### `api_key`

```
api_key=os.environ["OPENROUTER_API_KEY"]
```

Supplies the credential used to authenticate requests.

Initializing the client prepares it for API calls. It does not generate an answer by itself.

## 5.3 Select the Model

```python
MODEL_NAME = "openai/gpt-4o-mini"
```

The model identifier tells OpenRouter which model to use.

Available models depend on the provider's current offerings.

## 5.4 Send the Chat Completion Request

```
response = client.chat.completions.create(
    model=MODEL_NAME,
    messages=[
        {
            "role": "user",
            "content": "Explain Java in simple terms."
        }
    ],
    temperature=0.2,
    top_p=0.9,
    max_tokens=150,
)
```

This method sends the conversation and generation parameters to the API.

### `messages`

The `messages` parameter contains the conversation context supplied to the model.

Example:

```python
messages = [
    {"role": "user", "content": "What is Java?"},
    {
        "role": "assistant",
        "content": "Java is a programming language."
    },
    {"role": "user", "content": "What is its JVM?"}
]
```

The model can use the supplied earlier messages to answer the latest question.

Common roles:

| Role        | Meaning                                                         |
|-------------|-----------------------------------------------------------------|
| `system`    | Instructions defining the assistant's behavior, where supported |
| `user`      | User input or question                                          |
| `assistant` | An earlier assistant response                                   |
| `tool`      | Output from a tool in a tool-enabled interaction                |

**Important:** The API does not automatically receive your entire ChatGPT conversation history. You must supply the relevant history in `messages` if you want the model to use it.

### `temperature`

```python
temperature=0.2
```

Controls the randomness of generated text.

- Lower values generally produce more consistent responses.
- Higher values generally allow more variation.

A low temperature does not guarantee identical responses.

### `top_p`

```python
top_p=0.9
```

Controls token selection using nucleus sampling. The model considers a candidate set of likely next tokens based on their cumulative probability.

Generally, adjust either `temperature` or `top_p` rather than tuning both simultaneously.

### `max_tokens`

```python
max_tokens=150
```

Limits the generated completion length in tokens.

A token can represent a word, part of a word, punctuation, or another text unit.

The limit applies to the generated completion, not the entire conversation history. Parameter support and exact behavior can vary by model and endpoint.

## 5.5 Extract the Answer

```
answer = response.choices[0].message.content
print(answer)
```

Explanation:

- `response`: The complete response object.
- `choices`: The list of generated choices.
- `[0]`: Selects the first choice.
- `message`: Contains the generated assistant message.
- `content`: Contains the text response, when present.

The SDK parses the HTTP response into a Python object, so we do not need to manually parse JSON.

---

# 6. Approach 2: Calling an LLM Using Python `requests`

The `requests` library lets us construct and send HTTP requests directly.

Unlike the SDK approach, we explicitly define the URL, headers, and JSON payload.

## 6.1 Complete Example

```python
import os
import getpass
import requests

if not os.environ.get("OPENROUTER_API_KEY"):
    os.environ["OPENROUTER_API_KEY"] = getpass.getpass(
        "Enter your OpenRouter API key: "
    )

url = "https://openrouter.ai/api/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {os.environ['OPENROUTER_API_KEY']}",
    "Content-Type": "application/json",
}

payload = {
    "model": "openai/gpt-4o-mini",
    "messages": [
        {
            "role": "user",
            "content": "Explain Java in simple terms."
        }
    ],
    "temperature": 0.2,
    "top_p": 0.9,
    "max_tokens": 150,
}

response = requests.post(
    url,
    headers=headers,
    json=payload,
    timeout=60,
)

response.raise_for_status()

result = response.json()
answer = result["choices"][0]["message"]["content"]

print(answer)
```

## 6.2 URL

```python
url = "https://openrouter.ai/api/v1/chat/completions"
```

This is the endpoint that accepts chat completion requests.

The SDK builds the endpoint path internally. With `requests`, we provide the complete URL.

## 6.3 HTTP Headers

```
headers = {
    "Authorization": f"Bearer {os.environ['OPENROUTER_API_KEY']}",
    "Content-Type": "application/json",
}
```

Headers provide metadata about the HTTP request.

- **Authorization:** Supplies the Bearer token used to authenticate the request.
- **Content-Type:** Indicates that the request body is formatted as JSON.

## 6.4 Request Payload

The payload contains the information required by the API:

- Model identifier.
- Conversation messages.
- Generation parameters.

The payload is a normal Python dictionary. The `requests` library serializes it into JSON because we pass it through the `json` parameter.

## 6.5 Send the HTTP Request

```
response = requests.post(
    url,
    headers=headers,
    json=payload,
    timeout=60,
)
```

Explanation:

- `requests.post()`: Sends an HTTP POST request.
- `url`: Specifies the API endpoint.
- `headers`: Supplies authentication and content metadata.
- `json`: Supplies the request body as a Python dictionary to serialize.
- `timeout=60`: Limits how long the client waits before raising a timeout exception.

## 6.6 Check the HTTP Status

```
response.raise_for_status()
```

Raises an exception if the server returns an unsuccessful HTTP status code, generally in the 4xx or 5xx ranges.

Without this check, code might try to parse an error response as though it were a successful model response.

## 6.7 Parse the JSON Response

```
result = response.json()
```

Converts the JSON response body into Python data structures, typically dictionaries and lists.

Then:

```
answer = result["choices"][0]["message"]["content"]
print(answer)
```

Extracts the first choice's generated message content.

Unlike the SDK approach, we access the response using dictionary keys instead of object attributes.

---

# 7. Approach 3: Calling an LLM Using Raw HTTP with `curl`

An API can also be called directly using an HTTP command-line tool such as `curl`.

This approach is useful for testing APIs without writing a Python program.

```bash
curl https://openrouter.ai/api/v1/chat/completions \
  -X POST \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "openai/gpt-4o-mini",
    "messages": [
      {
        "role": "user",
        "content": "Explain Java in simple terms."
      }
    ],
    "temperature": 0.2,
    "max_tokens": 150
  }'
```

Explanation:

- `curl`: Sends an HTTP request from the command line.
- `-X POST`: Specifies the HTTP method.
- `-H`: Adds an HTTP header.
- `-d`: Supplies the request body.
- The response is returned in JSON format.

Replace `YOUR_API_KEY` with a valid key. Avoid exposing it in shared shell history or source files.

For real applications, prefer loading credentials from environment variables or a secret manager.

---

# 8. Comparing the Three Approaches

```text
                    Same LLM API
                         |
             +-----------+-----------+
             |           |           |
             v           v           v
         OpenAI SDK   requests      curl
             |           |           |
             v           v           v
         SDK handles  We handle    We handle
         much of the  HTTP in      HTTP from
         HTTP work    Python       command line
```

| Feature              | OpenAI Python SDK        | `requests`                                | `curl`                        |
|----------------------|--------------------------|-------------------------------------------|-------------------------------|
| Interface            | Python library           | Python library                            | Command-line tool             |
| Builds HTTP request  | Mostly handled by SDK    | Explicitly configured                     | Explicitly configured         |
| Parses response      | Structured Python object | You parse JSON                            | Usually displays raw response |
| Control over request | High-level interface     | More explicit control                     | More explicit control         |
| Best suited for      | Python applications      | Learning HTTP and custom API integrations | Quick API testing             |

All three approaches can communicate with the same API. The main difference is how much of the HTTP work each approach handles for you.

---

# 9. What Happens Behind the Scenes?

When we invoke the API, the communication is conceptually similar to this HTTP request:

```http
POST /api/v1/chat/completions HTTP/1.1
Host: openrouter.ai
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json
```

Request body:

```json
{
  "model": "openai/gpt-4o-mini",
  "messages": [
    {
      "role": "user",
      "content": "Explain Java"
    }
  ],
  "temperature": 0.2,
  "max_tokens": 150
}
```

The overall execution flow is:

1. The Python program prepares the prompt and configuration.
2. The client library or HTTP tool creates the HTTP request.
3. The request is sent to the API endpoint over HTTPS.
4. The API authenticates the request.
5. The provider routes the request to the selected model.
6. The model processes the supplied context and generates tokens.
7. The API returns a response, typically containing JSON.
8. The client parses the response.
9. The Python program extracts and displays the answer.

The actual model computation occurs on the provider's infrastructure, not inside the Python code running in your notebook.

---

# 10. Summary

Remember these key points:

1. **LLM:** Generates an answer using a trained model.
2. **API provider:** Makes the model accessible over an API.
3. **OpenAI Python SDK:** Provides a convenient, high-level interface for API calls.
4. **`requests`:** Allows direct construction and execution of HTTP requests in Python.
5. **`curl`:** Allows direct HTTP requests from the command line.
6. **API key:** Authenticates the request.
7. **Prompt:** The input supplied to the model.
8. **Messages:** Represent the conversation context sent with the request.
9. **Temperature and `top_p`:** Control aspects of text generation.
10. **`max_tokens`:** Limits the generated completion length.
11. **Inference:** Generates an answer using an existing trained model.
12. **Conversation history:** Must be supplied or maintained through an appropriate stateful mechanism.

The most important concept is that all three approaches ultimately send a request to an API. The SDK automates much of the HTTP work, while `requests` and `curl` give you more direct control over how the request is constructed and sent.
