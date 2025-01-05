import os
import PyPDF2
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Load environment variables
load_dotenv()


# Step 2: Function to Extract Text from Multiple PDFs
def extract_text_from_pdfs(pdf_directory):
    documents = []
    for filename in os.listdir(pdf_directory):
        if filename.lower().endswith(".pdf"):
            file_path = os.path.join(pdf_directory, filename)
            with open(file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = ""
                for page_num in range(len(reader.pages)):
                    page = reader.pages[page_num]
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text
                documents.append(Document(page_content=text, metadata={"source": filename}))
    return documents


# Step 3: Split Text into Chunks
def split_documents(documents, chunk_size=1024, chunk_overlap=64):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return text_splitter.split_documents(documents)

# Step 4: Create Embeddings and Vector Store
def create_vector_store(texts, persist_directory="db"):
    model_name = "hkunlp/instructor-large"  # The model you want to use
    embeddings = HuggingFaceEmbeddings(model_name=model_name)
    db = Chroma.from_documents(texts, embeddings, persist_directory=persist_directory)
    db.persist()
    return db

# Load vector store
def load_vector_store(persist_directory="db"):
    model_name = "hkunlp/instructor-large"
    embeddings = HuggingFaceEmbeddings(model_name=model_name)
    vector_store = Chroma(persist_directory=persist_directory, embedding_function=embeddings)
    return vector_store

# Retrieve relevant chunks
def retrieve_relevant_chunks(vector_store, query, k=5):
    """
    Retrieve the most relevant chunks from the vector store.
    """
    docs = vector_store.similarity_search(query, k=k)
    return docs

# View all contents of the vector store
def view_all_contents(vector_store):
    """
    Display all documents stored in the vector store along with their metadata.
    """
    print("\n*** All Stored Documents ***\n")
    # Assuming the Chroma vector store uses `get` to retrieve all documents.
    all_docs = vector_store.get()
    for i, doc in enumerate(all_docs['documents']):
        print(f"Document {i + 1}:\n{doc}\n")
        print(f"Metadata: {all_docs['metadatas'][i]}\n")
    print("\n*** End of Stored Documents ***\n")

# Test retrieval
def test_retrieval():
    persist_directory = input("Enter the path to the vector store directory (e.g., 'db'): ")  # Default: "db"
    vector_store = load_vector_store(persist_directory=persist_directory)
    
    
    print("Extracting text from PDFs...")
    documents = extract_text_from_pdfs(persist_directory)
    
    print("Splitting documents into chunks...")
    texts = split_documents(documents)
    
    print("Creating vector store with embeddings...")
    vector_store = create_vector_store(texts)
    
    while True:
        print("\nOptions:")
        print("1. Enter a query to retrieve relevant chunks.")
        print("2. View all contents of the vector store.")
        print("3. Exit.")
        
        choice = input("Select an option (1/2/3): ")
        
        if choice == '1':
            query = input("Enter a test query: ")
            print("Retrieving relevant chunks...")
            retrieved_docs = retrieve_relevant_chunks(vector_store, query)
            
            if not retrieved_docs:
                print("No relevant documents found!")
            else:
                print("\n*** Retrieved Chunks ***\n")
                for i, doc in enumerate(retrieved_docs):
                    print(f"Chunk {i + 1}:\n{doc.page_content}\n")
                    print(f"Metadata: {doc.metadata}\n")
                print("\n*** End of Retrieved Chunks ***\n")
        
        elif choice == '2':
            print("Displaying all contents of the vector store...")
            view_all_contents(vector_store)
        
        elif choice == '3':
            print("Exiting...")
            break
        
        else:
            print("Invalid option! Please select 1, 2, or 3.")

if __name__ == "__main__":
    test_retrieval()
