# Important LLM Terms (Simple + Practical)

## 1. Latency

### Meaning

Latency is the time taken for a request to receive a response.

```text
Request sent → Response received
```

### Java Analogy

Similar to API response time:

```
POST /generate-answer
```

If the request takes 2 seconds to complete:

```text
Total latency = 2 seconds
```

### Types

#### Time to First Token

The time taken before the first output token arrives.

Example:

```text
You ask a question → After 1.2 seconds, the first token appears
```

#### Full Response Latency

The total time taken to generate and receive the complete response.

Example:

```text
The complete answer arrives in 5 seconds
```

**Important:** Lower latency generally means a faster user experience.

---

## 2. Context Window

### Meaning

The context window is the maximum amount of tokenized information a model can process in a single context.

Think of it as the model's **working context**, not permanent memory.

```text
System Instructions
+ User Prompt
+ Conversation History
+ Tool Results
→ Context Window
```

### Example

If a model supports a context window of 128K tokens, the input context and, depending on the model's limits, the generated output must fit within the applicable token limits.

The context may include:

- System instructions
- Current prompt
- Previous messages
- Tool outputs
- Other supplied information

### Java Analogy

Similar to a limited-capacity buffer, although a context window is not technically the same thing as a Java buffer.

If the available context limit is exceeded, the application or API may reject the request, truncate content, or manage the history by removing or summarizing older messages.

**Important:** The model does not automatically remember every previous conversation. Information outside the supplied context may not be available to it.

---

## 3. Temperature

### Meaning

Temperature controls the randomness of token selection during text generation.

### Example

Question:

```text
Describe Java in one sentence.
```

#### Low Temperature (e.g., 0.1)

Often produces more predictable wording:

```text
Java is a widely used programming language for enterprise applications.
```

#### Higher Temperature (e.g., 1.2)

May produce more varied wording:

```text
Java is the dependable workhorse behind many enterprise applications.
```

These are illustrative examples, not guaranteed outputs.

### Simple Rule

```text
Lower temperature → Generally more predictable output
Higher temperature → Generally more varied output
```

Temperature does not directly control intelligence or guarantee factual accuracy.

---

## 4. Tokens

### Meaning

Tokens are small units of text processed by a language model. A token can represent a whole word, part of a word, punctuation, or another text unit.

Tokens are not exactly the same as words.

### Example

Depending on the tokenizer:

```text
"playing" → ["play", "ing"]
```

Another word might be represented as a single token or several tokens.

The exact tokenization depends on the model's tokenizer.

### Why Are Tokens Important?

Tokens affect:

- Context-window usage
- Input and output limits
- API pricing, where billing is token-based
- The amount of text a model processes or generates

---

## 5. Prompt

### Meaning

A prompt is the input or instruction provided to a model to guide its response.

It is similar to the data or instructions included in an API request.

### Example

```text
Explain Java Streams with a practical example.
```

This is a prompt.

A prompt can contain instructions, questions, background information, examples, and formatting requirements.

---

## 6. Prompt Engineering

### Meaning

Prompt engineering is the process of designing and improving prompts to guide an LLM toward more useful and relevant outputs.

### Example

**Bad prompt:**

```text
Explain Java.
```

**Better prompt:**

```text
Explain Java Streams with practical examples for an
experienced Java developer. Include common interview questions.
```

The better prompt specifies the topic, audience, and expected content.

### Use Cases

- Generating code
- Preparing for interviews
- Summarizing documents
- Extracting structured information
- Creating technical documentation

---

## 7. Hallucination

### Meaning

A hallucination occurs when an LLM generates information that is incorrect, fabricated, or unsupported, sometimes presenting it confidently.

### Example

```text
Java was invented in 1999 by Elon Musk.
```

This statement is false. Java was developed at Sun Microsystems, with James Gosling playing a leading role, and was publicly released in 1995.

### How Can We Reduce Hallucinations?

- Provide reliable context.
- Retrieve relevant information from trusted sources.
- Use tools such as search engines and calculators when appropriate.
- Validate important claims against authoritative sources.
- Ask the model to identify uncertainty rather than guess.

**Important:** Tool calling and RAG can reduce some hallucinations, but neither guarantees that every answer will be correct.

---

## 8. Fine-Tuning

### Meaning

Fine-tuning is the process of further training an already-trained model on a selected dataset to adapt its behavior or performance to particular tasks.

### Examples

- Adapting a model to a banking support workflow
- Improving classification of domain-specific requests
- Teaching a model a consistent response style
- Adapting a model to specialized terminology

### Important Distinction

Fine-tuning is not simply uploading documents or adding information to a prompt.

- **Prompting:** Provides instructions at inference time.
- **RAG:** Retrieves relevant external information at inference time.
- **Fine-tuning:** Updates model parameters through additional training.

Fine-tuning alone does not guarantee that the model will learn or reliably recall every fact in the training data.

---

## 9. Embedding

### Meaning

An embedding is a numerical vector representing an item such as text, an image, or another type of data.

Text embeddings are often used to represent semantic relationships between pieces of text.

### Example

```text
"cat" → [0.21, -0.44, 0.73, ...]
```

This list of numbers is called an embedding vector.

### Use Cases

- Semantic search
- Retrieval-Augmented Generation (RAG)
- Recommendation systems
- Similarity comparison
- Clustering related documents

**Important:** An embedding is not a human-readable definition of a word. Its numerical dimensions are learned representations.

---

## 10. RAG (Retrieval-Augmented Generation)

### Meaning

RAG combines information retrieval with LLM-based answer generation.

Instead of relying only on the model's learned knowledge, the application retrieves relevant external information and supplies it as context.

### Flow

```text
User Asks a Question
        |
        v
Retrieve Relevant Documents
        |
        v
Provide Retrieved Context to LLM
        |
        v
LLM Generates an Answer
        |
        v
Return Answer to User
```

### Example

Suppose a company has thousands of internal documents.

A user asks:

```text
What is our company's leave policy?
```

The application retrieves relevant policy documents and provides their contents to the LLM. The LLM then generates an answer based on the supplied context.

### Use Cases

- Enterprise chatbots
- Internal knowledge assistants
- Document question-answering systems
- Customer support applications

RAG can improve access to current or private information, but the generated answer still needs appropriate validation.

---

## 11. Top-p and Top-k

### Meaning

Top-p and top-k are sampling strategies that restrict the candidate tokens considered during generation.

They are related to temperature but control token selection differently.

### Top-k

The model considers only the \(k\) highest-probability candidate tokens.

Example:

```text
Top-k = 3

Candidate tokens:
1. Java
2. Python
3. JavaScript

Other candidates are excluded from this selection.
```

This is a simplified illustration.

### Top-p

The model considers the smallest set of likely tokens whose cumulative probability reaches a specified threshold \(p\).

For example:

```text
Top-p = 0.9

Consider the most likely tokens until their
cumulative probability reaches approximately 90%.
```

The candidate set can vary depending on the model's predicted probabilities.

### Simple Rule

```text
Top-k → Limits the number of candidate tokens
Top-p → Limits candidates using cumulative probability
Temperature → Changes the sampling distribution
```

Exact support and behavior depend on the model and API.

---

## 12. System Prompt

### Meaning

A system prompt provides high-level instructions that guide an assistant's behavior, where the API supports this message role.

### Example

```text
You are a Java expert assistant.
Explain concepts clearly and provide practical examples.
```

### Purpose

It can define:

- The assistant's role
- Response style
- Rules and constraints
- The intended audience
- Task-specific behavior

System instructions do not guarantee that the model will always follow them.

Also, system prompts are not necessarily hidden in every application. Their visibility depends on how the application is designed.

---

## 13. Tool Calling

### Meaning

Tool calling allows an LLM-powered application to use external tools, such as APIs, search engines, databases, or calculators.

The model can request a tool call, and the application executes the corresponding operation when permitted.

### Example

```text
User: What is 125 × 48?
        |
        v
LLM Requests Calculator Tool
        |
        v
Application Executes Calculation
        |
        v
Tool Returns: 6000
        |
        v
LLM Generates Final Answer
```

### Common Tools

- Web search
- Database queries
- Calculators
- External APIs
- Code execution tools

**Important:** The model does not necessarily execute tools by itself. The application or agent framework usually handles tool execution and returns the result to the model.

---

## 14. Streaming

### Meaning

Streaming allows a response to be delivered incrementally as it is generated instead of waiting for the entire response to finish.

### Example

Without streaming:

```text
Request sent
    |
    | Wait for the complete answer
    v
Complete answer received
```

With streaming:

```text
Request sent
    |
    v
First token received
    |
    v
More tokens received
    |
    v
Complete answer received
```

### Java Analogy

Similar in concept to processing or delivering data incrementally rather than waiting for an entire result. It is not exactly the same as Java Stream API processing.

### Benefits

- Faster perceived response time
- Earlier display of useful information
- Better user experience for long responses

Streaming does not necessarily reduce the total time needed to generate the answer.

---

# Summary

```text
Latency          = Time taken to receive a response
Context Window   = Maximum token context the model can process
Temperature      = Controls randomness in token selection
Tokens           = Units of text processed by the model
Prompt           = Input or instructions provided to the model
Prompt Engineering = Designing effective prompts
Hallucination    = Incorrect or unsupported generated information
Fine-Tuning      = Further training to adapt a model
Embedding        = Numerical vector representation
RAG              = Retrieval + LLM-based generation
Top-k            = Select from a limited number of likely tokens
Top-p            = Select from tokens within a cumulative probability threshold
System Prompt    = High-level instructions for the assistant
Tool Calling     = Using external tools through an application
Streaming        = Receiving output incrementally
```
