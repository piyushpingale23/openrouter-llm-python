# OpenRouter LLM with Python

A simple Python project that connects to a Large Language Model (LLM) through [OpenRouter](https://openrouter.ai/) using the OpenAI Python SDK.

This project demonstrates how to configure an API client, send a prompt to an LLM, and print the generated response.

---

## 1. How It Works

```text
User Prompt
    |
    v
Python Application (src/main.py)
    |
    v
OpenAI Python SDK
    |
    | base_url = https://openrouter.ai/api/v1
    v
OpenRouter API
    |
    v
Selected LLM
(openai/gpt-4o-mini)
    |
    v
Generated Response
    |
    v
Python Application
```

### Components

- **Python:** Runs the application.
- **OpenAI Python SDK:** Provides the client library to construct and send chat completion requests.
- **OpenRouter:** Provides a unified API to access supported LLMs.
- **LLM:** Processes the prompt and generates a response.

The OpenAI Python SDK and OpenRouter are different components. The SDK is the client library, while OpenRouter is the API service.

**Note:** This project requires an OpenRouter API key, not an OpenAI API key.

---

## 2. Project Structure

```text
openrouter-llm-python/
├── src/
│   └── main.py
├── .env.example
├── .gitignore
├── requirements.txt
├── README.md
└── LICENSE
```

| File               | Description                                                      |
|--------------------|------------------------------------------------------------------|
| `src/main.py`      | Application entry point; sends a prompt and prints the response. |
| `requirements.txt` | Lists the Python dependencies.                                   |
| `.env.example`     | Example configuration for the API key.                           |
| `.gitignore`       | Excludes secrets and generated files from Git.                   |
| `README.md`        | Project documentation.                                           |
| `LICENSE`          | MIT License.                                                     |

---

## 3. Prerequisites

Before running the application, ensure you have:

- Ubuntu or another Linux distribution.
- Python 3.10 or newer.
- Git.
- An OpenRouter account and API key.
- Internet connectivity.

Create an API key from [OpenRouter](https://openrouter.ai/).

Check whether Python and Git are installed:

```bash
python3 --version
git --version
```

If Python virtual environment support or Git is missing on Ubuntu, install it:

```bash
sudo apt update
sudo apt install python3 python3-venv python3-pip git
```

---

## 4. Clone the Repository

Open a terminal and run:

```bash
git clone https://github.com/piyushpingale23/openrouter-llm-python.git
```

Navigate to the project directory:

```bash
cd openrouter-llm-python
```

---

## 5. Create a Virtual Environment

A virtual environment isolates this project's Python dependencies from other Python projects.

Create the environment:

```bash
python3 -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

After activation, your terminal prompt should display `(.venv)`.

Whenever you open a new terminal to work on this project, activate the environment again:

```bash
cd openrouter-llm-python
source .venv/bin/activate
```

---

## 6. Install Dependencies

Upgrade pip:

```bash
python -m pip install --upgrade pip
```

Install the dependencies listed in `requirements.txt`:

```bash
pip install -r requirements.txt
```

The main dependency is the OpenAI Python SDK. The SDK handles the HTTP request to OpenRouter, so a separate `requests` dependency is not required for this example.

---

## 7. Configure the OpenRouter API Key

The application reads the API key from the `OPENROUTER_API_KEY` environment variable. If the variable is not set, it securely prompts for the key when the program runs.

### Option A: Enter the key when prompted (recommended for beginners)

Run:

```bash
python src/main.py
```

When prompted:

```text
Enter your OpenRouter API key:
```

Paste your OpenRouter API key and press Enter.

The key will not be displayed while typing and will not be saved by the application.

### Option B: Set an environment variable

Alternatively, set the key in your current terminal session:

```bash
export OPENROUTER_API_KEY="your_openrouter_api_key"
```

Then run:

```bash
python src/main.py
```

Replace `your_openrouter_api_key` with your actual key.

The variable remains available in the current shell session and its child processes. You may unset it when you finish:

```bash
unset OPENROUTER_API_KEY
```

**Security:** Never hardcode your real API key in source code or commit it to GitHub. If a key is accidentally exposed, revoke it and generate a replacement.

---

## 8. Run the Application

Ensure your virtual environment is activated and your dependencies are installed.

Execute:

```bash
python src/main.py
```

The application sends the following prompt to the selected model:

```text
What was my last question?
```

The program prints the response returned by the model.

Example output:

```text
Client initialized. Model: openai/gpt-4o-mini

Model response:
...
```

The generated response may differ between requests.

**Important:** The model does not automatically have access to your ChatGPT conversation history. This application sends only the messages explicitly included in its API request.

---

## 9. Configuration

The following settings are defined in `src/main.py`:

| Setting       | Purpose                                                |
|---------------|--------------------------------------------------------|
| `MODEL_NAME`  | Identifies the model to use through OpenRouter.        |
| `base_url`    | Directs the OpenAI SDK to the OpenRouter API endpoint. |
| `temperature` | Controls the variability of generated responses.       |
| `top_p`       | Controls nucleus sampling.                             |
| `max_tokens`  | Limits the number of generated tokens in the response. |

For example:

```
MODEL_NAME = "openai/gpt-4o-mini"

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=get_api_key(),
)
```

You can change the model identifier to another model supported by OpenRouter.

Model availability, access requirements, and pricing may change. Check the current details on the [OpenRouter website](https://openrouter.ai/).

---

## 10. Troubleshooting

### Authentication error (401)

Verify that:

- The API key is an OpenRouter API key.
- The key has not been revoked.
- The environment variable contains the correct value.

### ModuleNotFoundError

Activate the virtual environment and install the dependencies:

```bash
source .venv/bin/activate
pip install -r requirements.txt
```

### Model or provider error

Check that the configured model identifier is valid and currently available through OpenRouter.

### Virtual environment creation fails

Install the required Ubuntu package:

```bash
sudo apt install python3-venv
```

Then recreate the virtual environment:

```bash
python3 -m venv .venv
```

---

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
