Tokenization → Embeddings → Positional Information → Attention (Q, K, V) → Decoder-only Architecture

---

## Tokenization:

- It is process of converting text into small units called as token, and then further is converted into token I'd.
- Why it needed - because computers does not understand the human language, it understands the numbers.
- Types of Tokenization: Word, Character, Sub-word.
- Every LLM has its own tokenization algorithms like Gpt has BPE (Byte Pair Encoding), etc.

---

## Embeddings:

- Embedding is the process of converting tokens into numerical vectors that the model can process further.
- A vector is an ordered list of numbers.
- In an embedding space, words or tokens with similar meanings tend to have vectors closer together, while those with different meanings may have vectors farther apart.
- cat = [0.24, -0.34, 0.21, 0.43] - The above example represents the token cat using a 4-dimensional embedding vector. Its values are learned by the model during training and help represent its meaning.

---

## Positional Information:

- Positional Information helps the model understand the order of tokens in a sequence.
- Cat eats fish and Fish eats cat contain the same words but have different meanings because the order of the tokens is different.
- Positional information helps the Transformer distinguish these sequences.

---

## Transformer Architecture

- A Transformer is a neural network architecture used in modern AI models to process sequential data, such as text, and learn relationships between tokens.
- The Transformer architecture uses attention mechanisms and other neural network components to process token representations. Encoder-only, decoder-only, and encoder–decoder are different ways of organizing the Transformer architecture for different tasks.

### 1. Attention Mechanism

Attention is a mechanism that helps a model determine which tokens are most relevant when processing a particular token.

- Instead of treating all tokens equally, the model assigns different attention weights to tokens based on their relevance.
- **Example:** In the sentence `"The cat drank milk"`, when processing the token `"drank"`, the model may assign higher attention weights to `"cat"` and `"milk"` because they are relevant to understanding the action and its context.
- Q, K, and V are used to calculate attention and combine information from tokens.
- **Q (Query):** Represents what information the current token is looking for.
- **K (Key):** Represents the information each token provides for matching against a query.
- **V (Value):** Contains the information that is combined according to the attention weights.

**How it works:**

`Q + K → Attention Scores → Softmax → Attention Weights`

`Attention Weights + V → Attention Output`

For example, when processing `"drank"`, the model calculates attention scores between its query and the keys of available tokens. After applying softmax, the resulting attention weights determine how much information is taken from each token's value vector.

Note: These weights are learned dynamically from the input representations; the example illustrates the concept rather than fixed attention weights.

### 2. Transformer Components

A Transformer contains several components, not just attention:

- **Self-attention:** Determines how tokens use information from other tokens in the sequence.
- **Feed-forward network (FFN):** Further processes each token's representation.
- **Positional information:** Helps the model represent the order of tokens.

### 3. Types of Transformer Architectures

#### 1. Encoder-only

**Flow:** Input tokens → Encoder layers → Contextual representations

- **Purpose:** Processes input text to build contextual representations.
- **Example:** BERT — used for text classification, sentiment analysis, and other language-understanding tasks.

#### 2. Decoder-only

**Flow:** Input tokens → Decoder layers → Next-token prediction

- **Purpose:** Generates text autoregressive by predicting the next token based on previously available tokens.
- **Example:** GPT — used for text generation and conversational AI.

#### 3. Encoder–Decoder

**Flow:** Input tokens → Encoder → Decoder → Output tokens

- **Purpose:** Processes an input sequence and generates a corresponding output sequence.
- **Example:** T5 — used for translation, summarization, and other text-to-text tasks.

### 4. Key Takeaways

- **Transformer:** The overall neural network architecture.
- **Attention:** A core mechanism within the Transformer that determines how information from different tokens is combined.
- **Q, K, and V:** Components used by the attention mechanism.
- **Encoder-only, decoder-only, and encoder–decoder:** Different Transformer architectural configurations.
- **GPT:** A family of decoder-only language models that predicts the next token to generate text.