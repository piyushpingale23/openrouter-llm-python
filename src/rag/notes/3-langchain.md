
# LangChain – Complete Notes

## 1. What is LangChain?

**LangChain is an open-source framework used to develop applications powered by Large Language Models (LLMs).**

It provides reusable components that help developers connect different parts of an LLM application.

For example:

- LLMs
- Prompt Templates
- Document Loaders
- Text Splitters
- Embedding Models
- Vector Databases
- Retrievers
- Output Parsers
- External Tools

### Simple Definition

LangChain is a framework that simplifies the development of LLM-powered applications by providing reusable components and integrations.

### Is LangChain a Python Library?

Yes. LangChain provides libraries for:

1. Python
2. JavaScript / TypeScript

For our RAG implementation, we will use Python.

---

## 2. Why Do We Need LangChain?

Suppose we want to develop an Employee Policy Chatbot.

We have the following documents:

```text
Employee_Handbook.pdf
Leave_Policy.pdf
Holiday_List.pdf
```

A user asks:

"What is the company's annual leave policy?"

To answer this question using RAG, our application needs to perform multiple operations:

1. Read PDF documents.
2. Extract text.
3. Split text into chunks.
4. Generate embeddings.
5. Store embeddings in a Vector Database.
6. Retrieve relevant chunks.
7. Construct a prompt.
8. Send the prompt to an LLM.
9. Return the generated answer.

Without LangChain, we need to write the integration logic for these operations ourselves.

LangChain provides reusable components and integrations to simplify this process.

### Important

LangChain is:
- Not an LLM.
- Not a Vector Database.
- Not an Embedding Model.

It is a framework that connects and orchestrates these components.

---

## 3. Where Does LangChain Fit into RAG?

Let's understand the architecture.

### Document Ingestion Flow

```text
Documents (PDF, DOCX, TXT)
          |
          v
   Document Loader
          |
          v
     Text Splitter
          |
          v
    Embedding Model
          |
          v
     Vector Store
          |
          v
      ChromaDB
```

### User Query Flow

```text
User Question
      |
      v
   Retriever
      |
      v
   Vector Store
      |
      v
Relevant Documents
      |
      v
  Prompt Template
      |
      v
       LLM
      |
      v
  Output Parser
      |
      v
   Final Answer
```

LangChain provides components to connect these operations.

---

## 4. Important LangChain Components

### 1. Document Loaders

Document Loaders are used to load data from different sources.

Supported sources include:

- PDF files
- Word documents
- Text files
- CSV files
- Websites
- Databases

Example:

```python
from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader("Leave_Policy.pdf")

documents = loader.load()
```

The loader extracts text from the PDF.

A loaded Document generally contains:

- `page_content`: Extracted text.
- `metadata`: Additional information about the document.

Example:

```python
Document(
    page_content="Employees are eligible for 20 annual leaves.",
    metadata={
        "source": "Leave_Policy.pdf",
        "page": 0
    }
)
```

**Responsibility:** Load data from external sources into the application.

---

### 2. Text Splitters

A document may contain thousands of words.

Sending the entire document to an LLM every time is inefficient.

Therefore, we divide the document into smaller pieces called **chunks**.

LangChain provides Text Splitters to perform this operation.

Example:

```python
from langchain_text_splitters import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

chunks = text_splitter.split_documents(documents)
```

Explanation:

- `chunk_size=500`: Each chunk targets approximately 500 characters.
- `chunk_overlap=50`: Adjacent chunks share approximately 50 characters.

Visualization:

```text
Original Document
        |
        v
+----------------------+
| Chunk 1              |
| 500 characters       |
+----------------------+
          |
          | 50 characters overlap
          v
+----------------------+
| Chunk 2              |
| 500 characters       |
+----------------------+
          |
          | 50 characters overlap
          v
+----------------------+
| Chunk 3              |
| 500 characters       |
+----------------------+
```

**Responsibility:** Divide large documents into smaller, manageable chunks.

---

### 3. Embedding Models

An Embedding Model converts text into numerical vectors.

Example:

```text
Text:
"Employees are eligible for 20 annual leaves."

          |
          v

Embedding Model

          |
          v

Vector:
[0.21, 0.45, 0.78, 0.12, ...]
```

LangChain provides integrations with different embedding providers.

Example:

```python
from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small"
)

vector = embeddings.embed_query(
    "What is the annual leave policy?"
)
```

**Responsibility:** Convert text into numerical embeddings.

Note: The actual embedding generation is performed by the embedding model. LangChain provides the integration to use it.

---

### 4. Vector Stores

A Vector Store stores embeddings and provides vector-search functionality.

Examples:

- ChromaDB
- Pinecone
- Qdrant
- FAISS
- Weaviate

LangChain provides integrations to work with these vector stores.

Example using ChromaDB:

```python
from langchain_chroma import Chroma

vector_store = Chroma(
    collection_name="employee_policies",
    embedding_function=embeddings,
    persist_directory="./chroma_db"
)

vector_store.add_documents(chunks)
```

Explanation:

- `collection_name`: Name of the vector collection.
- `embedding_function`: Embedding model used by the vector store.
- `persist_directory`: Local directory used to persist ChromaDB data.
- `add_documents()`: Adds documents to the vector store.

Conceptually, LangChain coordinates embedding generation and storage through the vector store integration.

**Responsibility:** Store embeddings and support similarity search.

---

### 5. Retrievers

A Retriever is responsible for finding relevant documents based on a user query.

Suppose the user asks:

"What is the annual leave policy?"

The Retriever:

1. Takes the user query.
2. Converts the query into an embedding using the configured embedding model.
3. Searches the Vector Store.
4. Retrieves relevant documents.

Example:

```python
retriever = vector_store.as_retriever(
    search_kwargs={"k": 3}
)

relevant_documents = retriever.invoke(
    "What is the annual leave policy?"
)
```

Explanation:

- `k=3`: Retrieve up to three relevant documents.
- `invoke()`: Executes the retrieval operation.

**Responsibility:** Retrieve relevant documents from a data source.

---

### 6. Prompt Templates

After retrieving relevant documents, we need to provide them to the LLM along with the user's question.

A Prompt Template helps us create reusable prompts.

Example:

```python
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_template("""
Answer the question using only the provided context.

Context:
{context}

Question:
{question}
""")
```

Here:

- `{context}` contains retrieved document content.
- `{question}` contains the user's question.

Example of the final prompt:

```text
Answer the question using only the provided context.

Context:
Employees are eligible for 20 annual leaves.

Question:
What is the annual leave policy?
```

**Responsibility:** Construct a structured prompt for the LLM.

---

### 7. LLM Integration

Now we send the constructed prompt to an LLM.

LangChain supports integrations with different LLM providers.

Examples:

- OpenAI
- Anthropic
- Google Gemini
- Local models
- OpenAI-compatible APIs

Example:

```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)
```

The LLM receives the prompt and generates an answer.

Example:

```text
The annual leave policy provides employees
with 20 annual leaves.
```

**Responsibility:** Generate responses using the supplied context.

Note: LangChain connects to the model provider. The LLM itself performs the language generation.

---

### 8. Output Parsers

An Output Parser helps convert an LLM response into a desired format.

For example, we may want a plain string instead of an AI message object.

Example:

```python
from langchain_core.output_parsers import StrOutputParser

output_parser = StrOutputParser()
```

**Responsibility:** Process the model output into a usable format.

Output parsers can also help handle structured responses such as JSON.

---

## 5. What is a Chain in LangChain?

A **Chain** connects multiple operations into a single workflow.

Instead of manually calling every component and passing data between them, we can compose components together.

Example:

```text
Prompt Template
       |
       v
      LLM
       |
       v
 Output Parser
       |
       v
 Final Response
```

In modern LangChain, we can use the `|` operator to compose Runnable components.

Example:

```python
chain = prompt | llm | output_parser

response = chain.invoke({
    "context": "Employees are eligible for 20 annual leaves.",
    "question": "What is the annual leave policy?"
})
```

Execution flow:

```text
Input Data
    |
    v
Prompt Template
    |
    v
LLM
    |
    v
Output Parser
    |
    v
Final Response
```

This composition style is commonly associated with LangChain Expression Language (LCEL).

**Important:** Older LangChain tutorials may use classes such as `LLMChain` and `RetrievalQA`. Modern LangChain applications commonly use Runnable composition and newer retrieval-chain patterns.

---

## 6. Complete RAG Flow Using LangChain

Let's connect everything.

Suppose we have an Employee Policy PDF.

### Phase 1: Document Ingestion

```text
Employee_Policy.pdf
        |
        v
Document Loader
        |
        v
Text Splitter
        |
        v
Embedding Model
        |
        v
Vector Store (ChromaDB)
```

Step-by-step:

1. Document Loader reads the PDF.
2. Text Splitter divides the document into chunks.
3. Embedding Model converts each chunk into a vector.
4. Vector Store stores vectors, text, and metadata.

This phase is generally performed before users start asking questions.

### Phase 2: Query and Retrieval

```text
User Question
      |
      v
   Retriever
      |
      v
   Vector Store
      |
      v
Relevant Documents
      |
      v
  Prompt Template
      |
      v
       LLM
      |
      v
  Output Parser
      |
      v
   Final Answer
```

Step-by-step:

1. User asks a question.
2. Retriever searches the Vector Store.
3. Relevant documents are returned.
4. Prompt Template combines the question and retrieved context.
5. LLM generates an answer.
6. Output Parser processes the response.

---

## 7. What is Runnable in LangChain?

A Runnable is a component that follows LangChain's standard execution interface.

Common Runnable operations include:

- `invoke()`: Execute with one input.
- `batch()`: Execute with multiple inputs.
- `stream()`: Receive output progressively.

Example:

```python
response = chain.invoke({
    "context": "Employees are eligible for 20 annual leaves.",
    "question": "What is the annual leave policy?"
})
```

Here, `invoke()` executes the composed chain.

### Why Are Runnables Useful?

Different components can follow a common interface.

For example:

```text
Prompt
  |
  v
LLM
  |
  v
Output Parser
```

Each component can be composed with another compatible Runnable.

This makes it easier to build reusable workflows.

---

## 8. LangChain vs LLM vs Vector Database

These are different components.

| Component       | Responsibility                            | Example             |
|-----------------|-------------------------------------------|---------------------|
| LangChain       | Connects and orchestrates components      | LangChain           |
| LLM             | Understands input and generates responses | GPT, Claude, Gemini |
| Embedding Model | Converts text into vectors                | OpenAI Embeddings   |
| Vector Database | Stores and searches vectors               | ChromaDB, Pinecone  |
| Retriever       | Retrieves relevant information            | LangChain Retriever |

### Simple Analogy

Think about building a Spring Boot application.

| RAG Application | Spring Boot Analogy                         |
|-----------------|---------------------------------------------|
| LangChain       | Application framework / orchestration layer |
| LLM             | External AI service                         |
| Embedding Model | External embedding service                  |
| Vector Database | Database                                    |
| Document Loader | Data ingestion component                    |
| Retriever       | Search/retrieval service                    |
| Prompt Template | Prompt construction component               |

This is only an analogy. LangChain and Spring Boot have different designs and responsibilities.

---

## 9. Can We Build RAG Without LangChain?

Yes. LangChain is optional.

We can build a RAG application using individual libraries and APIs.

### Without LangChain

```text
Python Application
       |
       v
PDF Library
       |
       v
Custom Chunking Logic
       |
       v
Embedding API
       |
       v
ChromaDB Client
       |
       v
Custom Retrieval Logic
       |
       v
LLM API
       |
       v
Final Answer
```

In this approach, we write the integration code ourselves.

### With LangChain

```text
Python Application
       |
       v
LangChain Components
       |
       +---- Document Loader
       |
       +---- Text Splitter
       |
       +---- Embedding Model
       |
       +---- Vector Store
       |
       +---- Retriever
       |
       +---- Prompt Template
       |
       +---- LLM
       |
       v
Final Answer
```

### Why Use LangChain?

- Provides reusable integrations.
- Reduces repetitive integration code.
- Makes it easier to connect different model providers and vector databases.
- Provides reusable prompt and retrieval components.
- Helps compose complex LLM workflows.

### When Might We Avoid It?

- When the application is very small.
- When direct API integration is simpler.
- When we need complete control over every operation.
- When framework abstractions add unnecessary complexity.

---

## 10. LangChain vs LangGraph

You may also hear about LangGraph.

| LangChain                                     | LangGraph                                             |
|-----------------------------------------------|-------------------------------------------------------|
| Framework for building LLM applications       | Framework for building stateful, multi-step workflows |
| Provides integrations and reusable components | Provides graph-based workflow orchestration           |
| Useful for standard RAG pipelines             | Useful for complex agentic RAG and workflows          |
| Connects prompts, models, retrievers, etc.    | Manages state, nodes, edges, and execution flow       |

For now, focus on LangChain fundamentals. LangGraph can be explored after implementing a basic RAG application.

---

## 11. Python Installation

LangChain is available as Python packages.

Install the core package:

```bash
pip install langchain
```

For our basic RAG implementation, we will also need integration packages:

```bash
pip install langchain-community
pip install langchain-text-splitters
pip install langchain-chroma
pip install langchain-openai
```

### Package Responsibilities

| Package                    | Purpose                                            |
|----------------------------|----------------------------------------------------|
| `langchain`                | Main LangChain framework                           |
| `langchain-community`      | Community integrations, including document loaders |
| `langchain-text-splitters` | Document chunking                                  |
| `langchain-chroma`         | ChromaDB integration                               |
| `langchain-openai`         | OpenAI and compatible model integrations           |

Note: These packages are separate because LangChain keeps many integrations modular.

---

## 12. Important LangChain Terms

| Term            | Meaning                                                |
|-----------------|--------------------------------------------------------|
| Document Loader | Loads data from external sources                       |
| Document        | Text content with associated metadata                  |
| Text Splitter   | Splits documents into chunks                           |
| Embedding Model | Converts text into vectors                             |
| Vector Store    | Stores and searches vectors                            |
| Retriever       | Retrieves relevant documents                           |
| Prompt Template | Creates structured prompts                             |
| Chat Model      | Connects to an LLM                                     |
| Output Parser   | Processes model output                                 |
| Chain           | Connects multiple operations                           |
| Runnable        | Component that follows LangChain's execution interface |
| LCEL            | LangChain Expression Language                          |
| `invoke()`      | Executes a Runnable with an input                      |
| `batch()`       | Executes a Runnable with multiple inputs               |
| `stream()`      | Streams output progressively                           |
| Top-K           | Number of relevant results to retrieve                 |

---

## 13. Quick Revision

1. LangChain is an open-source framework for developing LLM-powered applications.
2. LangChain provides Python and JavaScript/TypeScript libraries.
3. LangChain is not an LLM.
4. LangChain is not a Vector Database.
5. Document Loaders read documents from different sources.
6. Text Splitters divide large documents into smaller chunks.
7. Embedding Models convert text into numerical vectors.
8. Vector Stores store and search embeddings.
9. Retrievers find relevant documents based on a query.
10. Prompt Templates construct prompts for LLMs.
11. LLMs generate answers using supplied context.
12. Output Parsers process generated responses.
13. Chains connect multiple operations into one workflow.
14. Runnables provide a common execution interface.
15. We can build RAG without LangChain.
16. LangGraph is useful for more complex stateful workflows.

---