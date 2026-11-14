
# ============================================================
# STEP 1: IMPORT REQUIRED LIBRARIES
# ============================================================

from pathlib import Path
from langchain_core.documents import Document


# ============================================================
# STEP 2: DEFINE PROJECT AND DATA DIRECTORY PATHS
# ============================================================

# __file__ gives the path of the current Python file.
# resolve() converts it into an absolute path.
# parent gives the directory containing this Python file.

BASE_DIR = Path(__file__).resolve().parent

# Our text files (dogs.txt, cats.txt, birds.txt, fish.txt)
# are stored inside the "data" directory.
#
# We construct the data directory path using BASE_DIR.
# This avoids hardcoding an absolute path.

DATA_DIR = BASE_DIR / "data"


# ============================================================
# STEP 3: CREATE A FUNCTION TO LOAD DOCUMENTS
# ============================================================

def load_documents():

    # Create an empty list.
    # We will store all loaded LangChain Document objects here.
    documents = []

    # Find all files ending with .txt inside the data directory.
    #
    # glob("*.txt") searches for files matching this pattern.
    # file_path represents the path of each matching file.

    for file_path in DATA_DIR.glob("*.txt"):

        # Read the complete content of the current text file.
        #
        # encoding="utf-8" helps correctly read text containing
        # different characters and symbols.

        content = file_path.read_text(encoding="utf-8")

        # Convert the text into a LangChain Document object.
        #
        # page_content:
        #     Stores the actual text from the file.
        #
        # metadata:
        #     Stores additional information about the document.
        #     Here, we store the original filename as its source.

        document = Document(
            page_content=content,
            metadata={
                "source": file_path.name
            }
        )

        # Add the Document object to our documents list.
        documents.append(document)

    # Return all loaded documents.
    # Other Python files can call this function and reuse the data.
    return documents


# ============================================================
# STEP 4: EXECUTE THE CODE
# ============================================================

# __name__ == "__main__" means:
# Run this section only when this file is executed directly.
#
# If another Python file imports load_documents(),
# this section will not execute automatically.

if __name__ == "__main__":

    # Call our function to load all text files.
    documents = load_documents()

    # Print the total number of documents loaded.
    print(f"Total documents loaded: {len(documents)}")

    # enumerate() gives us both:
    # 1. The document number (index)
    # 2. The actual Document object
    #
    # start=1 makes numbering begin from 1 instead of 0.

    for index, document in enumerate(documents, start=1):

        print(f"\nDocument {index}")

        # Print the source filename from document metadata.
        print("Source:", document.metadata["source"])

        # Print the actual document content.
        print("Content:")
        print(document.page_content)

        # Print a separator for readability.
        print("=" * 60)


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
#     Joins two paths safely.
#
# DATA_DIR.glob("*.txt")
#     Finds all .txt files in the specified directory.
#
# file_path.read_text(encoding="utf-8")
#     Reads the content of a text file.
#
# file_path.name
#     Returns only the filename, without the directory path.
#
# Installation: Not required. pathlib comes with Python.


# 2. langchain_core.documents.Document
# ------------------------------------------------------------
# Document is a LangChain class used to represent a document.
#
# It has two important fields:
#
# page_content:
#     Contains the actual text of the document.
#
# metadata:
#     Contains additional information such as filename,
#     source, category, or other useful attributes.
#
# We use Document objects because LangChain components
# can process them in later RAG steps.
#
# Installation:
#     pip install langchain-core
#
# Python import:
#     from langchain_core.documents import Document
