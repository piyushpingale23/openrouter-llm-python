
# Vector Database

## 1. What is a Vector Database?

A **Vector Database** is a database designed to store, index, and search numerical vectors called **embeddings**.

An embedding is a numerical representation of text, images, audio, or other data.

For example:

Text:
"Spring Boot is used to develop Java backend applications."

An embedding model converts this text into a numerical vector:

[0.21, 0.45, 0.78, 0.12, ...]

A Vector Database stores these vectors and helps us find semantically similar information.

### Simple Definition

A Vector Database stores embeddings and retrieves the most relevant information based on vector similarity.

---

## 2. Why Do We Need a Vector Database?

Let's understand with an example.

Suppose we have the following documents:

1. Java is a programming language.
2. Spring Boot is used to develop Java backend applications.
3. Python is widely used for Machine Learning.
4. React is a JavaScript library for building user interfaces.

Now, a user asks:

"Which technology should I use to build a Java backend application?"

A traditional database generally searches using exact values or structured conditions.

However, the user query and document may use different words while expressing similar meanings.

A Vector Database can identify that:

"Spring Boot is used to develop Java backend applications."

is semantically relevant to the user's question.

### Traditional Database vs Vector Database

| Traditional Database                       | Vector Database                              |
|--------------------------------------------|----------------------------------------------|
| Stores structured data                     | Stores numerical vectors and associated data |
| Exact matching and filtering               | Semantic similarity search                   |
| Uses SQL queries (in relational databases) | Uses vector similarity search                |
| Example: MySQL, PostgreSQL                 | Example: ChromaDB, Pinecone, Qdrant          |

Note: Modern databases such as PostgreSQL with pgvector can support both traditional SQL operations and vector search.

---

## 3. How Does a Vector Database Work?

A Vector Database mainly performs two operations:

1. Store embeddings.
2. Search for similar embeddings.

Let's understand the complete flow.

### Step 1: Convert Text into Embeddings

Suppose we have three documents:

- Document 1: Java is a programming language.
- Document 2: Spring Boot is a Java framework.
- Document 3: Python is used for Machine Learning.

An embedding model converts each document into a numerical vector.

Example:

```text
Document 1 → [0.12, 0.45, 0.67, 0.21]
Document 2 → [0.18, 0.49, 0.71, 0.25]
Document 3 → [0.85, 0.12, 0.34, 0.91]
```

These vectors are illustrative. Actual embedding dimensions depend on the embedding model.

### Step 2: Store Embeddings in Vector Database

The Vector Database stores:

- Unique ID
- Embedding vector
- Original text or document reference
- Metadata

Example:

| ID | Text                                | Embedding                |
|----|-------------------------------------|--------------------------|
| 1  | Java is a programming language      | [0.12, 0.45, 0.67, 0.21] |
| 2  | Spring Boot is a Java framework     | [0.18, 0.49, 0.71, 0.25] |
| 3  | Python is used for Machine Learning | [0.85, 0.12, 0.34, 0.91] |

Metadata can contain information such as:

```json
{
  "source": "java-guide.pdf",
  "page": 10,
  "category": "Java"
}
```

### Step 3: User Asks a Question

User query:

```text
Which framework should I use for Java backend development?
```

The query is also converted into an embedding using the same compatible embedding model.

```text
Query → [0.17, 0.48, 0.70, 0.24]
```

### Step 4: Perform Similarity Search

The Vector Database compares the query embedding with the stored embeddings.

Illustrative similarity results:

| Document                            | Similarity Score |
|-------------------------------------|-----------------:|
| Java is a programming language      |             0.78 |
| Spring Boot is a Java framework     |             0.97 |
| Python is used for Machine Learning |             0.15 |

The Vector Database retrieves the most relevant documents.

### Step 5: Return Relevant Information

The Vector Database returns the matching text and metadata.

```text
Spring Boot is a Java framework.
```

In a RAG application, this retrieved information is passed to the LLM as context.

The LLM generates the final response using that context.

---

## 4. What is Similarity Search?

**Similarity Search** means finding vectors that are closest or most similar to a given query vector.

For example:

```text
Query:
"Java backend framework"

Stored documents:
1. Java is a programming language.
2. Spring Boot is a Java framework.
3. Python is used for Machine Learning.
```

The Vector Database identifies which stored vectors are most similar to the query vector.

Similarity is calculated using mathematical techniques.

### Common Similarity Metrics

#### 1. Cosine Similarity

Cosine Similarity measures the angle between two vectors.

Formula:

Cosine Similarity = (A · B) / (||A|| × ||B||)

Typical interpretation:

- 1: Same direction.
- 0: Perpendicular.
- -1: Opposite direction.

A higher cosine similarity generally indicates greater similarity.

#### 2. Euclidean Distance (L2 Distance)

Euclidean Distance measures the straight-line distance between two vectors.

Formula:

Distance = sqrt((A1-B1)^2 + (A2-B2)^2 + ...)

Example:

```text
A = [1, 2]
B = [4, 6]

Distance = sqrt((4-1)^2 + (6-2)^2)
         = sqrt(9 + 16)
         = 5
```

A smaller distance means the vectors are closer.

#### 3. Dot Product

Dot Product calculates the sum of the products of corresponding vector elements.

Formula:

A · B = A1*B1 + A2*B2 + ...

Example:

```text
A = [1, 2]
B = [3, 4]

Dot Product = (1*3) + (2*4)
            = 3 + 8
            = 11
```

Dot product can be affected by vector magnitude.

**Important:** The appropriate metric depends on the embedding model and whether its vectors are normalized.

---

## 5. What is a Vector Index?

Suppose we have 10 million embeddings in a Vector Database.

When a user searches for something, comparing the query against every stored vector can become expensive.

To improve search performance, Vector Databases use a **Vector Index**.

A Vector Index organizes vectors so that similar vectors can be found efficiently.

Traditional database example:

```sql
CREATE INDEX idx_employee_id
ON employee(employee_id);
```

A traditional index helps retrieve records efficiently.

Similarly, a vector index helps retrieve similar vectors efficiently.

### Types of Vector Search

#### 1. Exact Search (Brute Force)

The query vector is compared with every stored vector.

```text
Query
  |
  v
Compare with Vector 1
Compare with Vector 2
Compare with Vector 3
Compare with Vector 4
...
Compare with Vector 10 Million
```

Advantages:
- Finds exact nearest neighbors.

Disadvantage:
- Can be slow for very large datasets.

#### 2. Approximate Nearest Neighbor (ANN)

ANN algorithms find very close matches without comparing every vector.

Advantages:
- Faster search.
- Suitable for large datasets.

Disadvantage:
- May not always return the exact nearest neighbors.

### Common ANN Indexing Techniques

1. HNSW
2. IVF
3. Product Quantization (PQ)

#### HNSW

HNSW stands for:

Hierarchical Navigable Small World.

It organizes vectors using a graph with multiple layers.

- Upper layers contain fewer nodes and help navigate quickly.
- Lower layers contain more nodes and help locate closer matches.

Think of it like Google Maps:

```text
Layer 1: Country
         |
Layer 2: State
         |
Layer 3: City
         |
Layer 4: Local Area
```

Instead of checking every location, we progressively narrow down the search.

---

## 6. What is Metadata in a Vector Database?

Metadata is additional information stored along with a vector.

Example:

```json
{
  "id": "doc-101",
  "text": "Spring Boot is a Java framework.",
  "embedding": [0.12, 0.45, 0.67, 0.21],
  "metadata": {
    "source": "java-guide.pdf",
    "page": 10,
    "category": "Java",
    "department": "Engineering"
  }
}
```

Metadata helps us filter search results.

Example:

Find similar documents only from the Engineering department.

This is called **Metadata Filtering**.

---

## 7. Popular Vector Databases and Libraries

### 1. ChromaDB
- Open-source vector database.
- Easy to use for local development and learning.
- Useful for RAG prototypes.

Website: https://www.trychroma.com/

### 2. Pinecone
- Managed cloud vector database.
- Designed for scalable vector search.
- Useful for production applications.

Website: https://www.pinecone.io/

### 3. FAISS
- Developed by Meta.
- Library for efficient similarity search.
- It is a vector search library, not a complete database by itself.

GitHub: https://github.com/facebookresearch/faiss

### 4. Qdrant
- Open-source vector database.
- Supports vector search and metadata filtering.

Website: https://qdrant.tech/

---

## 8. Role of Vector Database in RAG

Let's connect Vector Database with the RAG architecture.

### Document Ingestion Flow

```text
Documents
    |
    v
Document Loader
    |
    v
Text Extraction
    |
    v
Chunking
    |
    v
Embedding Model
    |
    v
Vector Database
    |
    v
Store Embeddings + Text + Metadata
```

### User Query Flow

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
Retrieve Top-K Relevant Chunks
    |
    v
Construct Prompt with Context
    |
    v
LLM
    |
    v
Final Answer
```

### Example

Suppose we upload an Employee Handbook PDF.

The system:
1. Reads the PDF.
2. Splits its content into chunks.
3. Converts chunks into embeddings.
4. Stores embeddings in a Vector Database.

Now the user asks:

"What is the company's leave policy?"

The system:
1. Converts the question into an embedding.
2. Searches the Vector Database.
3. Retrieves relevant leave-policy chunks.
4. Sends those chunks and the question to the LLM.
5. The LLM generates an answer based on the retrieved information.

---

## 9. Does a Vector Database Generate Embeddings?

Not necessarily.

Embedding generation and vector storage are conceptually separate responsibilities.

| Component       | Responsibility                               |
|-----------------|----------------------------------------------|
| Embedding Model | Converts text into numerical vectors         |
| Vector Database | Stores, indexes, and searches vectors        |
| LLM             | Generates answers using the provided context |

Some vector database products or integrations provide embedding functionality, but the underlying responsibilities remain distinct.

---

## 10. Important Terms

| Term               | Meaning                                                 |
|--------------------|---------------------------------------------------------|
| Vector             | Numerical representation of data                        |
| Embedding          | Vector generated from text, image, or other data        |
| Vector Database    | Database designed for vector storage and search         |
| Similarity Search  | Finding vectors similar to a query vector               |
| Cosine Similarity  | Measures the angle between vectors                      |
| Euclidean Distance | Measures the distance between vectors                   |
| Dot Product        | Calculates the product of corresponding vector elements |
| Vector Index       | Organizes vectors for efficient searching               |
| ANN                | Approximate Nearest Neighbor                            |
| HNSW               | Graph-based ANN indexing technique                      |
| Top-K              | Number of most relevant results to retrieve             |
| Metadata           | Additional information associated with a vector         |
| Metadata Filtering | Filtering vector search results using metadata          |

---

## 11. Quick Revision

1. A Vector Database stores and searches numerical embeddings.
2. An embedding model converts text into vectors.
3. Similarity Search finds vectors close to a query vector.
4. Cosine Similarity, Euclidean Distance, and Dot Product are common similarity metrics.
5. Vector Indexes improve search performance.
6. ANN techniques make large-scale vector search faster.
7. HNSW is a popular graph-based ANN technique.
8. Metadata provides additional information about stored vectors.
9. In RAG, the Vector Database retrieves relevant chunks for the LLM.
10. A Vector Database does not necessarily generate embeddings.
