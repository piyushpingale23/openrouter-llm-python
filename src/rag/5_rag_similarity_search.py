# ============================================================
# STEP 1: IMPORT REQUIRED LIBRARIES
# ============================================================

# Path is used to work with file and folder paths.
from pathlib import Path

# HuggingFaceEmbeddings converts text into numerical vectors.
# We use the same embedding model that we used in Step 4.
from langchain_huggingface import HuggingFaceEmbeddings

# FAISS is our vector store.
# It allows us to load the previously saved embeddings
# and search for documents with similar meanings.
from langchain_community.vectorstores import FAISS

# ============================================================
# STEP 2: DEFINE PROJECT DIRECTORIES
# ============================================================

# __file__ gives the path of this Python file.
# resolve() converts it into an absolute path.
# parent gives the folder containing this file (src/rag).
BASE_DIR = Path(__file__).resolve().parent

# Define the location where our FAISS vector store
# was saved in Step 4.
VECTOR_STORE_DIR = BASE_DIR / "vector_store"


# ============================================================
# STEP 3: LOAD THE EXISTING FAISS VECTOR STORE
# ============================================================

def load_vector_store():
    # Initialize the same embedding model that was used
    # when creating the FAISS vector store in Step 4.
    #
    # IMPORTANT:
    # We should use the same embedding model for both
    # indexing documents and searching documents.
    embedding_model = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    # Load the previously saved FAISS vector store.
    #
    # str(VECTOR_STORE_DIR):
    #     Provides the folder path where FAISS files exist.
    #
    # embedding_model:
    #     Used to convert the user's question into an embedding
    #     compatible with the stored document embeddings.
    #
    # allow_dangerous_deserialization=True:
    #     Allows LangChain to load the associated pickle file.
    #     Only enable this for vector stores that you trust
    #     and have created yourself.
    vector_store = FAISS.load_local(
        str(VECTOR_STORE_DIR),
        embedding_model,
        allow_dangerous_deserialization=True
    )

    # Return the loaded vector store so other functions
    # can use it for similarity searches.
    return vector_store


# ============================================================
# STEP 4: PERFORM SIMILARITY SEARCH
# ============================================================

def similarity_search(vector_store, query):
    # Search the FAISS vector store for chunks that are
    # semantically similar to the user's question.
    results = vector_store.similarity_search(

        # The question entered by the user.
        query=query,

        # k=3 means return the 3 most similar chunks.
        k=3
    )

    # Return the retrieved Document objects.
    return results


# ============================================================
# STEP 5: MAIN PROGRAM EXECUTION
# ============================================================

# This condition ensures that the code below runs only
# when this Python file is executed directly.
if __name__ == "__main__":

    # --------------------------------------------------------
    # STEP 5.1: LOAD THE FAISS VECTOR STORE
    # --------------------------------------------------------

    # Load the vector store that we created in Step 4.
    # We do not need to recreate embeddings for all documents.
    vector_store = load_vector_store()

    print("FAISS vector store loaded successfully!")

    # --------------------------------------------------------
    # STEP 5.2: GET THE USER'S QUESTION
    # --------------------------------------------------------

    # input() waits for the user to enter a question.
    # strip() removes unnecessary spaces from the beginning
    # and end of the entered text.
    query = input("\nEnter your question: ").strip()

    # Check whether the user entered an empty question.
    if not query:
        print("Please enter a valid question.")

        # Stop program execution if the question is empty.
        raise SystemExit(1)

    # --------------------------------------------------------
    # STEP 5.3: PERFORM SIMILARITY SEARCH
    # --------------------------------------------------------

    # Pass the loaded vector store and user's question
    # to the similarity_search() function.
    #
    # FAISS compares the question embedding with stored
    # document embeddings and retrieves the closest matches.
    results = similarity_search(
        vector_store,
        query
    )

    # --------------------------------------------------------
    # STEP 5.4: DISPLAY RETRIEVED DOCUMENT CHUNKS
    # --------------------------------------------------------

    print("\nRetrieved Documents:\n")

    # Loop through the retrieved Document objects.
    # enumerate() provides a result number starting from 1.
    for index, document in enumerate(results, start=1):
        # Display the result number.
        print(f"Result {index}")

        # Display the original filename stored in metadata.
        print("Source:", document.metadata.get("source", "Unknown"))

        # Display the actual text content of the retrieved chunk.
        print("Content:")
        print(document.page_content)

        # Print a separator between results for readability.
        print("=" * 60)

# ============================================================
# LIBRARY EXPLANATIONS
# ============================================================

# 1. pathlib
#    - Built-in Python library.
#    - Used to work with file and folder paths.
#    - Path() creates a path object.
#    - resolve() gets the absolute path.
#    - parent gets the containing folder.
#
# 2. langchain_huggingface
#    - Integrates Hugging Face models with LangChain.
#    - HuggingFaceEmbeddings loads a text embedding model.
#    - The embedding model converts text into numerical vectors.
#    - We use the same model that was used to create
#      the original document embeddings.
#
# 3. langchain_community.vectorstores
#    - Provides integrations with vector databases.
#    - FAISS is used to store and search numerical embeddings.
#    - FAISS.load_local() loads a previously saved vector store.
#    - similarity_search() retrieves semantically similar documents.
#
# Important FAISS methods:
#    - from_documents(): Creates a vector store from documents.
#    - save_local(): Saves the vector store to disk.
#    - load_local(): Loads a saved vector store.
#    - similarity_search(): Searches for similar documents.
#
# Installation:
#    pip install langchain-huggingface sentence-transformers
#    pip install langchain-community faiss-cpu
