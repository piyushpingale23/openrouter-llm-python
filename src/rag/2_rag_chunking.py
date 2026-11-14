
# ============================================================
# STEP 1: IMPORT REQUIRED LIBRARIES
# ============================================================

from pathlib import Path

# RecursiveCharacterTextSplitter is used to split large text
# documents into smaller chunks.
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Document is a LangChain class used to store text and metadata.
from langchain_core.documents import Document


# ============================================================
# STEP 2: DEFINE PROJECT AND DATA DIRECTORY PATHS
# ============================================================

# __file__ gives the path of the current Python file.
# resolve() converts it into an absolute path.
# parent gives the directory containing this Python file.

BASE_DIR = Path(__file__).resolve().parent

# Our original text files are stored inside the data directory.
DATA_DIR = BASE_DIR / "data"


# ============================================================
# STEP 3: LOAD DOCUMENTS
# ============================================================

def load_documents():

    # Create an empty list to store loaded documents.
    documents = []

    # Find all .txt files inside the data directory.
    for file_path in DATA_DIR.glob("*.txt"):

        # Read the complete content of the current text file.
        content = file_path.read_text(encoding="utf-8")

        # Convert the text into a LangChain Document object.
        #
        # page_content:
        #     Stores the actual text.
        #
        # metadata:
        #     Stores additional information about the document.
        #     Here, we store the original filename.

        documents.append(
            Document(
                page_content=content,
                metadata={
                    "source": file_path.name
                }
            )
        )

    # Return the list containing all loaded documents.
    return documents


# ============================================================
# STEP 4: SPLIT DOCUMENTS INTO SMALLER CHUNKS
# ============================================================

def split_documents(documents):

    # Create a text splitter.
    #
    # chunk_size=100:
    #     Each chunk will contain approximately 100 characters.
    #
    # chunk_overlap=20:
    #     Adjacent chunks will share approximately 20 characters.
    #
    # Why do we need chunking?
    #     1. Large documents are difficult to search efficiently.
    #     2. Smaller chunks help retrieve specific information.
    #     3. It avoids sending unnecessary text to the LLM.

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=100,
        chunk_overlap=20
    )

    # Split each document into smaller chunks.
    #
    # split_documents() accepts LangChain Document objects.
    # It splits their page_content while preserving metadata.
    #
    # This means every generated chunk retains its source filename.

    chunks = text_splitter.split_documents(documents)

    # Return all generated chunks.
    return chunks


# ============================================================
# STEP 5: EXECUTE THE CODE
# ============================================================

# This block executes only when this Python file is run directly.
if __name__ == "__main__":

    # First, load all original text documents.
    documents = load_documents()

    # Next, split the loaded documents into smaller chunks.
    chunks = split_documents(documents)

    # Print the total number of original documents.
    print("Total documents:", len(documents))

    # Print the total number of generated chunks.
    print("Total chunks:", len(chunks))

    # Display every generated chunk.
    for index, chunk in enumerate(chunks, start=1):

        print(f"\nChunk {index}")

        # Display the original source filename.
        print("Source:", chunk.metadata["source"])

        # Display the actual text inside the chunk.
        print("Content:", chunk.page_content)

        # Print a separator for readability.
        print("-" * 60)


# ============================================================
# LIBRARY EXPLANATION
# ============================================================

# 1. pathlib
# ------------------------------------------------------------
# pathlib is a built-in Python library used to work with
# files and directories.
#
# Path(__file__).resolve().parent
#     Gets the absolute directory path of the current file.
#
# BASE_DIR / "data"
#     Creates the path to the data directory.
#
# DATA_DIR.glob("*.txt")
#     Finds all files ending with .txt.
#
# file_path.read_text(encoding="utf-8")
#     Reads the contents of a text file.
#
# file_path.name
#     Returns only the filename.
#
# Installation: Not required. It comes with Python.


# 2. langchain-text-splitters
# ------------------------------------------------------------
# RecursiveCharacterTextSplitter is used to divide large
# documents into smaller text chunks.
#
# Important parameters:
#
# chunk_size:
#     Defines the target maximum chunk size.
#
# chunk_overlap:
#     Defines how much text is shared between neighboring chunks.
#
# split_documents(documents):
#     Accepts Document objects and returns smaller Document objects.
#     It also preserves the original metadata.
#
# Installation:
#     pip install langchain-text-splitters
#
# Python import:
#     from langchain_text_splitters import RecursiveCharacterTextSplitter


# 3. langchain-core
# ------------------------------------------------------------
# Document is a LangChain class used to represent text documents.
#
# Important fields:
#
# page_content:
#     Stores the document's actual text.
#
# metadata:
#     Stores additional information such as source filename.
#
# We use Document objects because LangChain's text splitters
# and vector stores can process them directly.
#
# Installation:
#     pip install langchain-core
#
# Python import:
#     from langchain_core.documents import Document
