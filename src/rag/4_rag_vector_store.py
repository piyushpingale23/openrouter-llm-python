# ============================================================
# STEP 1: IMPORT REQUIRED LIBRARIES
# ============================================================

# Path is used to work with folders and file paths.
# It helps us locate the data folder and save the vector store.
from pathlib import Path

# Document is a LangChain class used to store text along
# with additional information (metadata), such as the filename.
from langchain_core.documents import Document

# RecursiveCharacterTextSplitter divides large documents
# into smaller chunks, so they can be processed efficiently.
from langchain_text_splitters import RecursiveCharacterTextSplitter

# HuggingFaceEmbeddings converts text into numerical vectors.
# These vectors represent the meaning of the text.
from langchain_huggingface import HuggingFaceEmbeddings

# FAISS is a vector database that stores embeddings and
# helps us search for text with similar meaning.
from langchain_community.vectorstores import FAISS

# ============================================================
# STEP 2: DEFINE PROJECT DIRECTORIES
# ============================================================

# __file__ gives the path of this Python file.
# resolve() converts it into an absolute path.
# parent gives the folder containing this file (src/rag).
BASE_DIR = Path(__file__).resolve().parent

# Location of the folder containing our original text files.
DATA_DIR = BASE_DIR / "data"

# Location where the FAISS vector store will be saved.
# FAISS will create this folder if it does not already exist.
VECTOR_STORE_DIR = BASE_DIR / "vector_store"


# ============================================================
# STEP 3: LOAD DOCUMENTS
# ============================================================

def load_documents():
    # Create an empty list to store all loaded documents.
    documents = []

    # Find every .txt file inside the data folder.
    for file_path in DATA_DIR.glob("*.txt"):
        # Read the complete text file.
        # encoding="utf-8" supports standard Unicode text.
        content = file_path.read_text(encoding="utf-8")

        # Convert the text into a LangChain Document object.
        # page_content stores the actual text.
        # metadata stores additional information about the text.
        document = Document(
            page_content=content,
            metadata={
                "source": file_path.name
            }
        )

        # Add the Document object to our documents list.
        documents.append(document)

    # Return all loaded documents.
    return documents


# ============================================================
# STEP 4: SPLIT DOCUMENTS INTO SMALLER CHUNKS
# ============================================================

def create_chunks(documents):
    # Initialize the text splitter.
    splitter = RecursiveCharacterTextSplitter(

        # Maximum target size of each chunk, measured in characters.
        chunk_size=100,

        # Keep 20 characters from the previous chunk
        # in the next chunk to preserve some context.
        chunk_overlap=20
    )

    # Split the documents into smaller Document objects.
    # The original metadata, such as the source filename,
    # is carried over to the resulting chunks.
    chunks = splitter.split_documents(documents)

    # Return the list of chunks.
    return chunks


# ============================================================
# STEP 5: MAIN PROGRAM EXECUTION
# ============================================================

# This condition ensures that the code below runs only when
# this file is executed directly, not when it is imported.
if __name__ == "__main__":
    # --------------------------------------------------------
    # STEP 5.1: LOAD ORIGINAL DOCUMENTS
    # --------------------------------------------------------

    # Call load_documents() to read all .txt files.
    documents = load_documents()

    # Display how many documents were loaded.
    print("Total documents loaded:", len(documents))

    # --------------------------------------------------------
    # STEP 5.2: CREATE TEXT CHUNKS
    # --------------------------------------------------------

    # Divide the loaded documents into smaller chunks.
    chunks = create_chunks(documents)

    # Display the total number of chunks created.
    print("Total chunks created:", len(chunks))

    # --------------------------------------------------------
    # STEP 5.3: INITIALIZE THE EMBEDDING MODEL
    # --------------------------------------------------------

    # Load a pre-trained sentence-transformer model.
    # This model converts text into numerical vectors.
    embedding_model = HuggingFaceEmbeddings(

        # Model used to generate text embeddings.
        # It produces 384-dimensional vectors.
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    # --------------------------------------------------------
    # STEP 5.4: CREATE THE FAISS VECTOR STORE
    # --------------------------------------------------------

    # FAISS.from_documents() performs two important operations:
    #
    # 1. It generates embeddings for all the text chunks
    #    using our embedding model.
    #
    # 2. It stores those embeddings in a FAISS index,
    #    along with the associated documents and metadata.
    #
    # After this step, we can search for relevant chunks
    # using the meaning of a user's query.
    vector_store = FAISS.from_documents(

        # All the chunks that we want to store.
        documents=chunks,

        # Embedding model used to convert chunks into vectors.
        embedding=embedding_model
    )

    # --------------------------------------------------------
    # STEP 5.5: SAVE THE VECTOR STORE LOCALLY
    # --------------------------------------------------------

    # Save the FAISS index and its associated document data
    # inside the vector_store folder.
    #
    # This allows us to load the existing vector store later
    # without rebuilding it every time we run a search.
    vector_store.save_local(str(VECTOR_STORE_DIR))

    # --------------------------------------------------------
    # STEP 5.6: DISPLAY SUCCESS MESSAGE
    # --------------------------------------------------------

    # Inform the user that the vector store was created.
    print("\nFAISS vector store created successfully!")

    # Display the folder where the vector store was saved.
    print("Saved location:", VECTOR_STORE_DIR)

# ============================================================
# LIBRARY EXPLANATIONS
# ============================================================

# 1. pathlib
#    - Built-in Python library.
#    - Used to work with file and folder paths.
#    - Path() creates a path object.
#    - resolve() gets the absolute path.
#    - parent gets the containing folder.
#    - glob("*.txt") finds text files.
#    - read_text() reads a text file.
#
# 2. langchain_core.documents
#    - Provides the Document class.
#    - Document stores text and metadata together.
#    - page_content contains the actual text.
#    - metadata contains extra information, such as source filename.
#
# 3. langchain_text_splitters
#    - Provides tools to split large documents into smaller chunks.
#    - RecursiveCharacterTextSplitter tries to split text
#      at sensible boundaries.
#    - chunk_size controls the target maximum chunk size.
#    - chunk_overlap preserves some text between adjacent chunks.
#    - split_documents() splits a list of Document objects.
#
# 4. langchain_huggingface
#    - Integrates Hugging Face embedding models with LangChain.
#    - HuggingFaceEmbeddings loads a sentence-transformer model.
#    - The model converts text into numerical vectors.
#    - These vectors represent semantic meaning.
#
# 5. langchain_community.vectorstores
#    - Provides integrations with vector databases and search tools.
#    - FAISS is used to store and search numerical embeddings.
#    - FAISS.from_documents() creates a vector store from documents.
#    - save_local() saves the vector store to disk.
#
# Installation:
#    pip install langchain-core langchain-text-splitters
#    pip install langchain-huggingface sentence-transformers
#    pip install langchain-community faiss-cpu
