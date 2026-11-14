# ============================================================
# STEP 1: IMPORT REQUIRED LIBRARIES
# ============================================================

from pathlib import Path

# Document is used to represent text and its metadata.
from langchain_core.documents import Document

# RecursiveCharacterTextSplitter splits large documents
# into smaller chunks.
from langchain_text_splitters import RecursiveCharacterTextSplitter

# HuggingFaceEmbeddings converts text into numerical vectors.
from langchain_huggingface import HuggingFaceEmbeddings

# ============================================================
# STEP 2: DEFINE PROJECT AND DATA DIRECTORY PATHS
# ============================================================

# Get the absolute path of the directory containing this file.
BASE_DIR = Path(__file__).resolve().parent

# Define the directory containing our original text files.
DATA_DIR = BASE_DIR / "data"


# ============================================================
# STEP 3: LOAD DOCUMENTS
# ============================================================

def load_documents():
    # Create an empty list to store all loaded documents.
    documents = []

    # Find all text files inside the data directory.
    for file_path in DATA_DIR.glob("*.txt"):
        # Read the content of the current text file.
        content = file_path.read_text(encoding="utf-8")

        # Convert the text into a LangChain Document object.
        #
        # page_content:
        #     Contains the actual text.
        #
        # metadata:
        #     Contains additional information about the document.
        #     Here, we store the original filename.

        documents.append(
            Document(
                page_content=content,
                metadata={
                    "source": file_path.name
                }
            )
        )

    # Return all loaded documents.
    return documents


# ============================================================
# STEP 4: SPLIT DOCUMENTS INTO SMALLER CHUNKS
# ============================================================

def create_chunks(documents):
    # Initialize the text splitter.
    #
    # chunk_size=100:
    #     Each chunk has a target size of approximately
    #     100 characters.
    #
    # chunk_overlap=20:
    #     Adjacent chunks share approximately 20 characters.
    #
    # Why do we create chunks?
    #     Smaller text sections make semantic retrieval
    #     more focused and manageable.

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=100,
        chunk_overlap=20
    )

    # Split all documents into smaller Document objects.
    #
    # The original metadata is preserved in the chunks.

    return splitter.split_documents(documents)


# ============================================================
# STEP 5: EXECUTE THE CODE
# ============================================================

if __name__ == "__main__":
    # --------------------------------------------------------
    # Step 5.1: Load original documents
    # --------------------------------------------------------

    documents = load_documents()

    print("Total documents loaded:", len(documents))

    # --------------------------------------------------------
    # Step 5.2: Create smaller chunks
    # --------------------------------------------------------

    chunks = create_chunks(documents)

    print("Total chunks created:", len(chunks))

    # --------------------------------------------------------
    # Step 5.3: Initialize the embedding model
    # --------------------------------------------------------

    # HuggingFaceEmbeddings loads a pretrained embedding model.
    #
    # Model:
    #     sentence-transformers/all-MiniLM-L6-v2
    #
    # This model converts text into 384-dimensional vectors.
    #
    # The model may be downloaded from Hugging Face
    # the first time this code runs.

    embedding_model = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    # --------------------------------------------------------
    # Step 5.4: Generate an embedding for the first chunk
    # --------------------------------------------------------

    # Select the text content of the first chunk.
    first_chunk_text = chunks[0].page_content

    # Convert the text into a numerical embedding vector.
    #
    # embed_query() accepts a single text string and returns
    # its numerical vector representation.
    #
    # Here we use it to demonstrate embedding generation.
    # In our actual indexing step, we will embed all chunks.

    vector = embedding_model.embed_query(first_chunk_text)

    # --------------------------------------------------------
    # Step 5.5: Display the results
    # --------------------------------------------------------

    # Display the original text that was converted into a vector.
    print("\nOriginal text:")
    print(first_chunk_text)

    # Display the numerical embedding vector.
    print("\nEmbedding vector:")
    print(vector)

    # Display the number of dimensions in the vector.
    print("\nVector dimensions:")
    print(len(vector))

# ============================================================
# LIBRARY EXPLANATION
# ============================================================

# 1. pathlib
# ------------------------------------------------------------
# pathlib is a built-in Python library for working with
# files and directories.
#
# Path(__file__).resolve().parent
#     Gets the absolute directory path of this Python file.
#
# BASE_DIR / "data"
#     Creates the path to the data directory.
#
# DATA_DIR.glob("*.txt")
#     Finds all text files in the data directory.
#
# file_path.read_text(encoding="utf-8")
#     Reads the content of a text file.
#
# Installation: Not required. It comes with Python.


# 2. langchain-core
# ------------------------------------------------------------
# Document is a LangChain class used to represent documents.
#
# page_content:
#     Stores the actual text.
#
# metadata:
#     Stores additional information such as source filename.
#
# Installation:
#     pip install langchain-core
#
# Python import:
#     from langchain_core.documents import Document


# 3. langchain-text-splitters
# ------------------------------------------------------------
# RecursiveCharacterTextSplitter splits large text documents
# into smaller chunks.
#
# Important parameters:
#
# chunk_size:
#     Target maximum size of each chunk.
#
# chunk_overlap:
#     Amount of shared text between neighboring chunks.
#
# split_documents(documents):
#     Splits LangChain Document objects into smaller
#     Document objects while preserving metadata.
#
# Installation:
#     pip install langchain-text-splitters
#
# Python import:
#     from langchain_text_splitters import RecursiveCharacterTextSplitter


# 4. langchain-huggingface
# ------------------------------------------------------------
# HuggingFaceEmbeddings is a LangChain integration that
# allows us to use Hugging Face embedding models.
#
# model_name:
#     Specifies which pretrained embedding model to load.
#
# embed_query(text):
#     Converts a single text string into an embedding vector.
#
# embed_documents(texts):
#     Converts multiple text strings into embedding vectors.
#
# In our project, we use:
#
# sentence-transformers/all-MiniLM-L6-v2
#
# This model generates 384-dimensional embedding vectors.
#
# Installation:
#     pip install langchain-huggingface
#
# Python import:
#     from langchain_huggingface import HuggingFaceEmbeddings
#
# Additional dependency:
#     pip install sentence-transformers
