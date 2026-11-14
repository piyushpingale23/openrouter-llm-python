
# Retrieval-Augmented Generation (RAG)

## 1. What is RAG?

**RAG** stands for **Retrieval-Augmented Generation**.

RAG is a technique in which an application retrieves relevant information from an external knowledge source and provides that information to a Large Language Model (LLM) so that the LLM can generate an informed answer.

Let's break down the three words:

| Term       | Meaning                                                 |
|------------|---------------------------------------------------------|
| Retrieval  | Finding relevant information from external data.        |
| Augmented  | Adding retrieved information to the LLMs input.         |
| Generation | LLM generates an answer using the supplied information. |

**In simple words:** RAG searches our own data, provides relevant information to the LLM, and asks the LLM to answer the user's question using that information.

## 2. Why Do We Need RAG?

An LLM does not automatically know the private or newly updated information stored in our company documents, databases, or internal systems.

For example, imagine we are developing an HR chatbot for our company.

We have the following documents:

- `Leave_Policy.pdf` - Contains annual leave, sick leave, and casual leave information.
- `Employee_Handbook.docx` - Contains company rules and employee guidelines.
- `Holiday_List.xlsx` - Contains the company's holiday calendar.

An employee asks:

> How many sick leaves can I take in a year?

The LLM may not know our company's leave policy.

RAG solves this problem by retrieving the relevant information from our company documents and providing it to the LLM.

## 3. Two Major Phases of RAG

A basic RAG system has two major phases:

1. **Data Ingestion / Indexing:** Prepare documents and store them, so they can be searched.
2. **Query / Retrieval and Generation:** Find relevant information when a user asks a question and provide it to the LLM.

---

# Part A — Data Ingestion (Preparation Phase)

Suppose we have a PDF file named `Leave_Policy.pdf`.

Its content is:

```text
Company Leave Policy

1. Annual Leave

Employees are eligible for 20 annual leaves
per calendar year.

2. Sick Leave

Employees are eligible for 10 sick leaves
per calendar year.

3. Casual Leave

Employees are eligible for 7 casual leaves
per calendar year.
```

Before users ask questions, we need to prepare this document for retrieval.

## 4. Step 1 — Document Loading

First, our application needs to read documents and extract their content.

Documents can come from different sources:

- PDF files
- Word documents
- Excel files
- Text files
- Websites
- Databases
- Internal company systems

A **Document Loader** reads a document and extracts its content into text that our application can process.

### Visualization

```text
Leave_Policy.pdf
       |
       v
 Document Loader
       |
       v
 Extracted Text
```

**Important:** The document loader's primary responsibility is to extract content. It does not need to understand the meaning of the document.

## 5. Step 2 — Text Splitting (Chunking)

Suppose our PDF contains 100 pages.

Should we send all 100 pages to the LLM whenever someone asks a question?

No.

There are several problems:

- Too much information.
- Higher token consumption.
- Increased processing cost.
- Context window limitations.
- Irrelevant information can confuse the answer.

To solve this problem, we divide the document into smaller pieces.

These smaller pieces are called **Chunks**.

### Visualization

```text
Original Document
       |
       v
  Text Splitter
       |
       +------ Chunk 1
       |       Annual Leave Information
       |
       +------ Chunk 2
       |       Sick Leave Information
       |
       +------ Chunk 3
       |       Casual Leave Information
       |
       +------ Chunk 4
               Other Leave Guidelines
```

Now, instead of one large document, we have multiple smaller text chunks.

### Important Chunking Concepts

**1. Chunk Size**

Chunk size defines how much text is contained in one chunk.

For example:
- Chunk Size = 500 characters.
- Chunk Size = 500 tokens.

The unit depends on the configuration of the text splitter.

**2. Chunk Overlap**

Chunk overlap defines how much text is repeated between consecutive chunks.

Example:

```text
Original Text:

Employees are eligible for 20 annual leaves.
Employees are eligible for 10 sick leaves.
Employees are eligible for 7 casual leaves.
```

Without overlap:

```text
Chunk 1:
Employees are eligible for 20 annual leaves.

Chunk 2:
Employees are eligible for 10 sick leaves.

Chunk 3:
Employees are eligible for 7 casual leaves.
```

With overlap:

```text
Chunk 1:
Employees are eligible for 20 annual leaves.
Employees are eligible for 10 sick leaves.

Chunk 2:
Employees are eligible for 10 sick leaves.
Employees are eligible for 7 casual leaves.
```

The repeated content helps preserve context between consecutive chunks.

**Important:** Chunk size and overlap need to be selected carefully. Very small chunks may lose context, while very large chunks may contain unnecessary information.

## 6. Step 3 — Embedding Generation

An **Embedding Model** converts text into a numerical vector that represents aspects of its meaning.

You have already learned about embedding vectors. RAG uses the same concept.

### Example

```text
Chunk 1:
"Employees are eligible for 20 annual leaves."

                 |
                 v
           Embedding Model
                 |
                 v
      [0.12, 0.45, 0.87, 0.21, ...]
```

Similarly:

```text
Chunk 2:
"Employees are eligible for 10 sick leaves."

                 |
                 v
           Embedding Model
                 |
                 v
      [0.32, 0.65, 0.17, 0.91, ...]
```

Each chunk gets its own embedding vector.

### Why Do We Need Embeddings?

Consider these two questions:

1. How many sick leaves can I take?
2. What is the annual sick leave allowance?

The words are different, but their meanings are similar.

Embedding models help represent semantic similarity so that the application can find relevant information even when the exact words are different.

**Important:** The numerical values shown above are illustrative. Actual vectors depend on the embedding model.

## 7. Step 4 — Store Embeddings in a Vector Database

After generating embeddings, where should we store them?

We store them in a **Vector Database**.

A vector database is designed to store and search numerical vector representations efficiently.

Some popular vector databases and vector-search technologies are:

1. ChromaDB
2. Pinecone
3. Weaviate
4. Milvus
5. Qdrant
6. FAISS (Vector similarity-search library)

### Example

A simplified representation of a vector database:

| ID | Text Chunk                          | Embedding         |
|----|-------------------------------------|-------------------|
| 1  | 20 annual leaves per calendar year. | [0.12, 0.45, ...] |
| 2  | 10 sick leaves per calendar year.   | [0.32, 0.65, ...] |
| 3  | 7 casual leaves per calendar year.  | [0.52, 0.15, ...] |

A real vector database can also store metadata, such as:

- Document name
- Page number
- Document ID
- Department
- Access permissions

### Data Ingestion Visualization

```text
PDF / DOCX / TXT / Other Documents
                |
                v
          Document Loader
                |
                v
           Extracted Text
                |
                v
           Text Splitter
              (Chunks)
                |
                v
           Embedding Model
                |
                v
           Embedding Vectors
                |
                v
           Vector Database
                |
                v
         Prepared for Retrieval
```

This entire preparation process is called **Data Ingestion or Indexing**.

---

# Part B — Query, Retrieval and Generation

Our documents are now prepared and stored in the vector database.

Now imagine an employee asks:

> How many sick leaves can I take in a year?

Let's understand what happens internally.

## 8. Step 5 — Receive the User Query

The RAG application receives the user's question.

```text
User:

"How many sick leaves can I take in a year?"

                 |
                 v
            RAG Application
```

The application needs to find the relevant information from the vector database.

## 9. Step 6 — Generate Embedding for the User Query

Remember, during data ingestion, we converted every document chunk into an embedding vector.

Now we need to do something similar with the user's question.

We send the question to an embedding model.

### Visualization

```text
User Question:

"How many sick leaves can I take in a year?"

                 |
                 v
           Embedding Model
                 |
                 v
             Query Vector

       [0.31, 0.63, 0.19, 0.89, ...]
```

Now our question is also represented as a numerical vector.

**Why do we convert the user question into an embedding?**

Because our vector database contains document embeddings.

We need to compare the user's question embedding with the stored document embeddings to find semantically relevant information.

**Important:** The query embedding must be compatible with the document embeddings. Usually, we use the same embedding model for both.

## 10. Step 7 — Similarity Search (Retrieval)

Now we send the user's question embedding to the vector database.

The vector database compares the query embedding with the stored embeddings and finds the most semantically similar chunks.

### Example

User Question:

```text
How many sick leaves can I take in a year?
```

The vector database compares it with:

| Stored Chunk             | Illustrative Similarity |
|--------------------------|------------------------:|
| Annual Leave Information |                    0.35 |
| Sick Leave Information   |                    0.94 |
| Casual Leave Information |                    0.28 |

The sick leave chunk is the most relevant result in this illustration.

### Visualization

```text
             User Query
                 |
                 v
          Query Embedding
                 |
                 v
          Vector Database
                 |
                 v
          Similarity Search
                 |
       +---------+---------+
       |         |         |
       v         v         v
    Chunk 1   Chunk 2   Chunk 3
    Annual     Sick      Casual
    Leave      Leave     Leave
       |         |         |
       v         v         v
     0.35      0.94      0.28
                 |
                 v
         Most Relevant Chunk
```

The database retrieves the most relevant chunks.

This process is called **Similarity Search or Vector Search**.

### Important Concepts

**1. Similarity Score**

A similarity score indicates how closely two vectors are related according to the selected similarity metric.

**2. Top-K**

Top-K defines how many of the highest-ranked chunks we want to retrieve.

For example:

```text
Top-K = 3
```

It means we want to retrieve the three highest-ranked chunks.

**3. Retrieval**

Retrieval means finding and returning relevant information from the knowledge source.

**Important:** Similarity search does not necessarily search for identical words. It searches for semantic similarity based on embedding representations.

Similarity scores and their interpretation depend on the metric being used. The example scores above are illustrative.

## 11. Step 8 — Send Retrieved Information to the LLM

Now we have retrieved the relevant information.

For example:

```text
Retrieved Context:

Employees are eligible for 10 sick leaves
per calendar year.
```

But we haven't generated the final answer yet.

We need to send this retrieved information along with the user's original question to the LLM.

How?

We construct a prompt.

### Example Prompt

```text
You are an HR assistant.

Use the following context to answer the question.

Context:

Employees are eligible for 10 sick leaves
per calendar year.

Question:

How many sick leaves can I take in a year?

Answer:
```

Notice something important.

We are providing two things to the LLM:

1. **Context:** Information retrieved from our documents.
2. **Question:** The actual question asked by the user.

The LLM now has the relevant information it needs to answer.

This process is called **Prompt Augmentation**.

## 12. Step 9 — LLM Generates the Final Answer

The LLM processes the prompt and generates the response.

### Visualization

```text
          Retrieved Context
                 +
           User Question
                 |
                 v
          Prompt Construction
                 |
                 v
                LLM
                 |
                 v
          Generated Answer
```

Example response:

> According to the company leave policy, you are eligible for 10 sick leaves per calendar year.

That's it!

The LLM generated an answer using information retrieved from the company's documents.

This completes the basic RAG process.

---

# 13. Complete RAG Architecture

Now let's combine everything.

There are two separate flows.

## Flow A — Document Preparation (Data Ingestion)

```text
PDF / DOCX / TXT / Other Sources
                |
                v
          Document Loader
                |
                v
           Extracted Text
                |
                v
           Text Splitter
              (Chunks)
                |
                v
           Embedding Model
                |
                v
           Embedding Vectors
                |
                v
           Vector Database
       (Vectors + Text + Metadata)
```

## Flow B — User Question and Answer Generation

```text
User Question
      |
      v
Embedding Model
      |
      v
Query Embedding
      |
      v
Vector Database
      |
      v
Similarity Search
      |
      v
Relevant Retrieved Chunks
      |
      v
Prompt Construction
(Context + User Question)
      |
      v
LLM
      |
      v
Generated Answer
```

**Important:**

- Document ingestion is generally performed before the user asks a question.
- Query-time retrieval and generation happen whenever the user submits a question.
- If the documents change, the application needs to update or re-index the affected content.

---

# 14. RAG vs. External Tool Calling

Since we have already learned external tool calling, let's understand the difference.

| External Tool Calling                               | RAG                                                                 |
|-----------------------------------------------------|---------------------------------------------------------------------|
| LLM requests execution of an external tool.         | Application retrieves relevant information from a knowledge source. |
| A tool can perform an operation or fetch live data. | Retrieval finds relevant context for the LLM.                       |
| Example: Call a weather API.                        | Example: Search company policy documents.                           |
| Can retrieve data or perform actions.               | Primarily supplies knowledge to the LLM.                            |

### Example 1 — External Tool Calling

```text
User:

What is the weather in Pune?

                 |
                 v
                LLM
                 |
                 v
          Weather API Call
                 |
                 v
          Weather Information
                 |
                 v
                LLM
                 |
                 v
            Final Answer
```

### Example 2 — RAG

```text
User:

What is our company's leave policy?

                 |
                 v
          Embedding Model
                 |
                 v
          Vector Database
                 |
                 v
         Retrieve Relevant Data
                 |
                 v
          Context + Question
                 |
                 v
                LLM
                 |
                 v
            Final Answer
```

**Important:** RAG and external tool calling can also be combined in a single application.

---

# 15. Does RAG Train the LLM?

This is a very important interview question.

**No. RAG does not train or fine-tune the LLM.**

RAG retrieves external information and provides it to the LLM at query time.

It does not change the LLMs model weights.

### RAG vs. Fine-tuning

| RAG                                                            | Fine-tuning                                                       |
|----------------------------------------------------------------|-------------------------------------------------------------------|
| Retrieves external information at query time.                  | Further trains a model using additional examples.                 |
| Does not change model weights.                                 | Updates model weights.                                            |
| Useful for company documents and frequently updated knowledge. | Useful for adapting model behaviour, style, or task performance.  |
| Knowledge can be updated by updating the external data store.  | New training data generally requires another fine-tuning process. |

### Simple Analogy

Think of an LLM as a student.

- **Fine-tuning:** Teaching the student differently through additional training.
- **RAG:** Giving the student a reference book before asking a question.

This is a simplified analogy, but it captures the main difference.

---

# 16. RAG Learning Roadmap

After understanding the fundamentals, we should study the following concepts in sequence.

| No. | Topic                           | What We Will Learn                                                       |
|-----|---------------------------------|--------------------------------------------------------------------------|
| 1   | RAG Fundamentals                | What RAG is, why it is needed, and its architecture.                     |
| 2   | Document Loading                | Reading PDF, DOCX, TXT, and other files.                                 |
| 3   | Chunking Strategies             | Chunk size, chunk overlap, fixed-size and recursive splitting.           |
| 4   | Embedding Models                | Embedding dimensions, model selection, and vector generation.            |
| 5   | Vector Databases                | ChromaDB, FAISS, Pinecone, metadata, and vector storage.                 |
| 6   | Similarity Search               | Cosine similarity, distance metrics, Top-K, and similarity thresholds.   |
| 7   | Retrieval Techniques            | Semantic search, keyword search, hybrid search, and reranking.           |
| 8   | Prompt Augmentation             | Combining retrieved context with user questions.                         |
| 9   | RAG Implementation Using Python | Building an end-to-end RAG application.                                  |
| 10  | Advanced RAG                    | Query transformation, multi-query retrieval, and parent-child retrieval. |
| 11  | RAG Evaluation                  | Retrieval quality, answer relevance, faithfulness, and accuracy.         |

---

# 17. Quick Revision — Important Terms

| Term                | Meaning                                            |
|---------------------|----------------------------------------------------|
| RAG                 | Retrieval-Augmented Generation                     |
| Document Loader     | Extracts content from documents.                   |
| Chunk               | A smaller piece of extracted text.                 |
| Chunk Size          | Amount of text contained in a chunk.               |
| Chunk Overlap       | Text shared between consecutive chunks.            |
| Embedding Model     | Converts text into numerical vectors.              |
| Embedding Vector    | Numerical representation of text.                  |
| Vector Database     | Stores and searches vectors.                       |
| Query Embedding     | Vector representation of the user's question.      |
| Similarity Search   | Finds vectors similar to the query vector.         |
| Top-K               | Number of highest-ranked results to retrieve.      |
| Retrieval           | Finds relevant chunks from the knowledge source.   |
| Context             | Retrieved information supplied to the LLM.         |
| Prompt Augmentation | Combines retrieved context with the user question. |
| Generation          | LLM generates the final response.                  |

---

# 18. Final Mental Model

Remember this architecture:

```text
YOUR DOCUMENTS
      |
      v
  CHUNKING
      |
      v
  EMBEDDINGS
      |
      v
 VECTOR DATABASE
      |
      v
  RETRIEVAL
      |
      v
 RELEVANT CONTEXT
      |
      v
     LLM
      |
      v
 FINAL ANSWER
```

**RAG = Your Documents + Embeddings + Vector Database + Retrieval + LLM = Context-aware AI Application.**

The most important things to remember:

1. During ingestion, we convert document chunks into embeddings and store them.
2. During a query, we convert the user's question into an embedding.
3. We search the vector database to retrieve relevant chunks.
4. We provide the retrieved chunks and user's question to the LLM.
5. The LLM generates the final answer using the supplied context.
