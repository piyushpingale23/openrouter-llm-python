# RAG (Retrieval-Augmented Generation) with Python and OpenRouter

## 1. Introduction

This package demonstrates how to build a basic **Retrieval-Augmented Generation (RAG)** application using Python, LangChain, FAISS, Hugging Face embeddings, and OpenRouter.

RAG combines two important capabilities:

1. **Retrieval:** Find relevant information from your own documents.
2. **Generation:** Send the retrieved information to an LLM, so it can generate an answer grounded in that information.

Instead of relying entirely on the LLMs training knowledge, a RAG application retrieves relevant content from an external knowledge base before generating an answer.

### What we will build

We will create a small knowledge base containing information about:

- Dogs
- Cats
- Birds
- Fish

We will then build a pipeline that accepts a question, searches the knowledge base, retrieves relevant text, and sends that text to an LLM through OpenRouter.

---

## 2. Project Structure

The current RAG package is organized as follows:

```text
src/
└── rag/
    ├── README.md
    │
    ├── data/
    │   ├── dogs.txt
    │   ├── cats.txt
    │   ├── birds.txt
    │   └── fish.txt
    │
    ├── 1_rag_document_loading.py
    ├── 2_rag_chunking.py
    ├── 3_rag_embeddings.py
    ├── 4_rag_vector_store.py
    ├── 5_rag_similarity_search.py
    ├── 6_rag_with_openrouter.py
    │
    └── vector_store/
        ├── index.faiss
        └── index.pkl
```

**Note:** The `vector_store/` directory is generated when you run the vector-store creation script. It is ignored by Git in the current project configuration.

The `.env` file and `requirements.txt` are located in the project root, outside the `rag/` directory.

---

## 3. Technologies Used

| Technology            | Purpose                                    |
|-----------------------|--------------------------------------------|
| Python                | Main programming language                  |
| LangChain             | Document processing and RAG components     |
| Hugging Face          | Loads the embedding model                  |
| Sentence Transformers | Converts text into embeddings              |
| FAISS                 | Stores and searches embeddings efficiently |
| OpenRouter            | Provides access to LLM APIs                |
| OpenAI Python SDK     | Communicates with OpenRouter               |
| python-dotenv         | Loads environment variables                |

### Important libraries

```text
faiss-cpu
sentence-transformers
langchain
langchain-community
langchain-text-splitters
langchain-huggingface
python-dotenv
openai
```

These dependencies should be added to the existing project-level `requirements.txt`, without removing your other project dependencies.

Install them using:

```bash
pip install -r requirements.txt
```

---

## 4. Understanding the RAG Pipeline

A typical RAG application has two major workflows:

### A. Indexing workflow

This workflow prepares documents, so they can be searched later.

```text
Original Documents
       |
       v
Document Loading
       |
       v
Text Chunking
       |
       v
Generate Embeddings
       |
       v
Store Embeddings in FAISS
       |
       v
Vector Database
```

### B. Question-answering workflow

This workflow retrieves relevant information and generates an answer.

```text
User Question
       |
       v
Convert Question into Embedding
       |
       v
Similarity Search in FAISS
       |
       v
Retrieve Relevant Chunks
       |
       v
Build Context
       |
       v
Send Context + Question to LLM
       |
       v
Generate Final Answer
```

The indexing workflow is generally performed when documents are added or updated. The question-answering workflow runs whenever a user asks a question.

---

# 5. Step-by-Step Implementation

## Step 1: Document Loading

**File:** `1_rag_document_loading.py`

### What is document loading?

Document loading is the process of reading data from files and converting it into a format that our RAG application can process.

In our example, we load `.txt` files from the `data/` directory.

LangChain provides a `Document` object to represent each document.

A document contains:

- `page_content`: Actual text content.
- `metadata`: Additional information about the document, such as its filename or source.

Example:

```
Document(
    page_content="Dogs are loyal and friendly animals.",
    metadata={"source": "dogs.txt"}
)
```

### What happens in this step?

1. Find all `.txt` files inside the data directory.
2. Read their contents.
3. Create a LangChain `Document` object for each file.
4. Store the filename in metadata.
5. Print the loaded documents.

### Run

```bash
python src/rag/1_rag_document_loading.py
```

### Expected result

You should see the contents of your text files and their corresponding source filenames.

---

## Step 2: Text Chunking

**File:** `2_rag_chunking.py`

### What is chunking?

Chunking means splitting large documents into smaller pieces of text.

Why do we need chunking?

- Large documents may exceed an LLMs context window.
- Smaller text sections can improve retrieval relevance.
- It helps retrieve only the information needed to answer a question.
- It reduces unnecessary context sent to the LLM.

We use LangChain's:

```
RecursiveCharacterTextSplitter
```

Example:

```
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=100,
    chunk_overlap=20
)
```

### Important parameters

| Parameter       | Meaning                                                              |
|-----------------|----------------------------------------------------------------------|
| `chunk_size`    | Maximum target size of each chunk, measured in characters by default |
| `chunk_overlap` | Number of overlapping characters between adjacent chunks             |

### What is chunk overlap?

Suppose a document contains:

```text
Dogs are loyal animals. They are friendly and intelligent.
Dogs need exercise, nutrition, and proper care.
```

Without overlap, a sentence or related idea could be split across two chunks.

Overlap preserves some text from the previous chunk in the next chunk, helping maintain context.

### Run

```bash
python src/rag/2_rag_chunking.py
```

### Expected result

You should see smaller text chunks generated from your original documents.

---

## Step 3: Generate Embeddings

**File:** `3_rag_embeddings.py`

### What are embeddings?

Embeddings are numerical representations of text.

An embedding model converts text into a list of floating-point numbers called a vector.

Example:

```text
"Dogs are loyal animals."
```

Might be represented conceptually as:

```text
[0.12, -0.34, 0.56, 0.21, ...]
```

The actual embedding contains many more dimensions.

### Why do we need embeddings?

Computers cannot directly perform semantic similarity comparisons on ordinary sentences in the same way they compare numerical vectors.

Embeddings represent the meaning of text numerically, allowing us to compare related pieces of text.

For example:

```text
Question: Which animals are loyal?
```

The embedding model can represent this question in a vector space where it may be close to text such as:

```text
Dogs are loyal and friendly animals.
```

### Embedding model used

We use:

```text
sentence-transformers/all-MiniLM-L6-v2
```

This model produces 384-dimensional embeddings.

### Code concept

```
from langchain_huggingface import HuggingFaceEmbeddings

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vector = embedding_model.embed_query(
    "Dogs are loyal animals."
)

print(len(vector))
```

Expected output:

```text
384
```

### Important methods

| Method              | Purpose                                          |
|---------------------|--------------------------------------------------|
| `embed_query()`     | Converts a user query into an embedding          |
| `embed_documents()` | Converts multiple document texts into embeddings |

### Run

```bash
python src/rag/3_rag_embeddings.py
```

**Note:** The first execution may download the embedding model from Hugging Face. You need an internet connection for the initial download.

---

## Step 4: Create a FAISS Vector Store

**File:** `4_rag_vector_store.py`

### What is a vector store?

A vector store is a system that stores embeddings and allows us to search for similar vectors.

We use FAISS.

FAISS stands for:

**Facebook AI Similarity Search.**

It is a library for efficient similarity search over vectors.

### What happens in this step?

1. Load documents.
2. Split documents into chunks.
3. Convert chunks into embeddings.
4. Store embeddings in FAISS.
5. Save the FAISS index locally.

### Important code concept

```
vector_store = FAISS.from_documents(
    documents=chunks,
    embedding=embedding_model
)
```

This creates a FAISS vector store from the document chunks.

To save it:

```
vector_store.save_local(
    str(VECTOR_STORE_DIR)
)
```

FAISS typically creates:

```text
vector_store/
├── index.faiss
└── index.pkl
```

- `index.faiss`: Stores the vector index.
- `index.pkl`: Stores associated document data and metadata.

### Run

```bash
python src/rag/4_rag_vector_store.py
```

### Expected result

A `vector_store/` directory should be created containing the saved index files.

**Important:** Re-run this script whenever you modify your source documents and want to rebuild the knowledge base.

---

## Step 5: Similarity Search

**File:** `5_rag_similarity_search.py`

### What is similarity search?

Similarity search finds documents whose embeddings are closest to the embedding of a user's question.

Example:

```text
User Question:
Which animals are loyal?
```

The application converts the question into an embedding and searches FAISS for similar document chunks.

### Important code concept

```
results = vector_store.similarity_search(
    query=query,
    k=3
)
```

Here:

- `query`: The user's question.
- `k=3`: Return the three most similar document chunks.

### What is semantic search?

Semantic search focuses on the meaning of a query rather than just matching exact keywords.

For example:

```text
Query: Which animals are good companions?
```

The system may retrieve:

```text
Dogs are loyal and friendly animals.
```

Even though the exact words are different, the meanings are related.

### Run

```bash
python src/rag/5_rag_similarity_search.py
```

Enter a question when prompted.

Example:

```text
Which animals are good companions?
```

### Expected result

You should see the top matching document chunks and their source filenames.

**Important:** Similarity search returns the requested number of results even if some are not very relevant. Returning three results does not guarantee that all three are good matches.

---

## Step 6: Complete RAG Application with OpenRouter

**File:** `6_rag_with_openrouter.py`

This is the final application that combines retrieval and LLM generation.

### What happens?

1. Load the saved FAISS vector store.
2. Accept a question from the user.
3. Retrieve the three most relevant document chunks.
4. Combine the retrieved chunks into a context.
5. Send the context and question to an LLM.
6. Print the final answer.

### OpenRouter

OpenRouter provides a unified API for accessing different LLMs.

We use the OpenAI Python SDK with OpenRouter's API endpoint.

```
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY
)
```

### Environment variables

The `.env` file is located in the root of the project:

```text
openrouter-llm-python/
├── .env
├── .env.example
├── requirements.txt
└── src/
```

Add the following variables to `.env`:

```env
OPENROUTER_API_KEY=your_actual_api_key
OPENROUTER_MODEL=openai/gpt-4o-mini
```

Replace the API key with your actual OpenRouter API key.

The model ID is an example. Make sure the model is currently available to your OpenRouter account.

### Loading environment variables

We use:

```
from dotenv import load_dotenv
import os

load_dotenv(PROJECT_ROOT / ".env")

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL")
```

### Important functions

| Function               | Responsibility                         |
|------------------------|----------------------------------------|
| `load_vector_store()`  | Loads the saved FAISS index            |
| `retrieve_documents()` | Retrieves relevant chunks              |
| `create_context()`     | Combines retrieved chunks into context |
| `generate_answer()`    | Sends context and question to the LLM  |
| `rag_pipeline()`       | Connects the complete RAG workflow     |

### System prompt

The system prompt instructs the LLM to:

- Answer using retrieved context.
- Avoid making up facts.
- Admit when the context does not contain enough information.
- Treat retrieved documents as reference data, not instructions.

This helps reduce unsupported answers, although prompt instructions alone cannot guarantee that hallucinations never happen.

### Run

```bash
python src/rag/6_rag_with_openrouter.py
```

Example question:

```text
What care do dogs need?
```

The application retrieves relevant chunks from the dog document and sends them to the LLM.

The LLM then generates an answer using the retrieved context.

---

# 6. Complete Execution Order

Run the scripts in the following order when setting up the package for the first time:

```bash
# Navigate to project root
cd ~/openrouter-llm-python

# Activate virtual environment
source .venv/bin/activate

# 1. Load documents
python src/rag/1_rag_document_loading.py

# 2. Split documents into chunks
python src/rag/2_rag_chunking.py

# 3. Generate embeddings
python src/rag/3_rag_embeddings.py

# 4. Create and save the FAISS vector store
python src/rag/4_rag_vector_store.py

# 5. Test similarity search
python src/rag/5_rag_similarity_search.py

# 6. Run the complete RAG application
python src/rag/6_rag_with_openrouter.py
```

You do not need to run steps 1–4 every time you ask a question.

Once the vector store is built, you can run:

```bash
python src/rag/5_rag_similarity_search.py
```

or:

```bash
python src/rag/6_rag_with_openrouter.py
```

Rebuild the vector store after changing the documents or the embedding configuration.

---

# 7. Important RAG Concepts

| Concept         | Explanation                                   |
|-----------------|-----------------------------------------------|
| Document        | Original information loaded from a file       |
| Chunk           | Smaller piece of a document                   |
| Chunk overlap   | Shared text between neighboring chunks        |
| Embedding       | Numerical representation of text              |
| Embedding model | Model that converts text into vectors         |
| Vector          | Numerical representation of an embedding      |
| Vector store    | Stores vectors and supports similarity search |
| FAISS           | Library used for vector similarity search     |
| Retrieval       | Finding relevant document chunks              |
| Context         | Retrieved information supplied to the LLM     |
| Generation      | LLM produces an answer                        |
| RAG             | Retrieval combined with generation            |

---

# 8. Security Best Practices

1. Never upload `.env` to GitHub.
2. Keep API keys private.
3. Add `.env` to `.gitignore`.
4. Commit `.env.example` without real secrets.
5. Never print your complete API key in application logs.
6. Only load trusted FAISS pickle files.
7. Do not treat retrieved document content as executable instructions.

Example `.env.example`:

```env
OPENROUTER_API_KEY=your_openrouter_api_key
OPENROUTER_MODEL=your_openrouter_model_id
```

---

# 9. Limitations of This Basic RAG Application

This project is a learning implementation, not a production-ready RAG system.

Some limitations:

- It uses only simple text documents.
- Chunk size and overlap are fixed.
- It retrieves a fixed number of chunks.
- It does not use a relevance threshold.
- It does not provide citations in the generated answer.
- It does not automatically detect document changes.
- It does not implement reranking.
- It does not include evaluation or monitoring.

These are useful opportunities for future improvements.

---

# 10. Final Summary

In this package, we implemented the essential building blocks of a RAG application.

The complete flow is:

```text
Documents
    |
    v
Document Loading
    |
    v
Chunking
    |
    v
Embeddings
    |
    v
FAISS Vector Store
    |
    v
User Query
    |
    v
Similarity Search
    |
    v
Retrieved Context
    |
    v
OpenRouter LLM
    |
    v
Final Answer
```

**The main idea to remember:**

RAG does not simply ask an LLM to answer a question. It first retrieves relevant information from an external knowledge base and then provides that information to the LLM to generate a grounded answer.

This is the foundation of many document-question-answering applications, knowledge assistants, and enterprise AI systems.
