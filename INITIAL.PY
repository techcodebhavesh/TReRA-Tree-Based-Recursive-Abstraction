import os
import PyPDF2
from dotenv import load_dotenv
from groq import Groq
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.schema import Document

# Load environment variables
load_dotenv()

# Step 1: Configure Groq Client
groq_client = Groq()

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

def retrieve_relevant_chunks(vector_store, query, k=5):
    """
    Retrieve the most relevant chunks from the vector store.
    """
    docs = vector_store.similarity_search(query, k=k)
    return "\n".join([doc.page_content for doc in docs])


# Step 5: Query Groq Model
def query_groq_model_with_context(system_message, user_query, context):
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))  # Initialize the Groq client
    
    print("*** Groq Model Query ***")
    print("Context:", context)
    print("Question:", user_query)
    print("System Message:", system_message)
    print("Querying Groq model...")
    print("*** Groq Model Query ***")
    
    # Construct the prompt messages
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {user_query}"},
    ]
    
    # Call the Groq API for chat completions
    chat_completion = client.chat.completions.create(
        messages=messages,
        model="llama3-8b-8192"  # Specify the model you want to use
    )
    
    # Extract and return the response content
    return chat_completion.choices[0].message.content



# Step 6: Main Function to Integrate All Steps
def main():
    pdf_directory = input("Enter the path to the PDF directory: ")  # e.g., "pdfs"
    
    print("Extracting text from PDFs...")
    documents = extract_text_from_pdfs(pdf_directory)
    
    print("Splitting documents into chunks...")
    texts = split_documents(documents)
    
    print("Creating vector store with embeddings...")
    vector_store = create_vector_store(texts)
    
    print("Setup complete. You can now ask questions about the PDFs.")
    
    # Continuous Chat Loop
    system_message = "You are an intelligent assistant. Provide clear, concise, and accurate answers."
    while True:
        user_query = input("Ask a question about the PDFs (type 'exit' to quit): ")
        if user_query.lower() == 'exit':
            break
        
        print("Retrieving relevant chunks...")
        context = retrieve_relevant_chunks(vector_store, user_query)
        
        print("Querying Groq model...")
        answer = query_groq_model_with_context(system_message, user_query, context)
        
        print(f"Groq Llama: {answer}\n")


if __name__ == "__main__":
    main()
