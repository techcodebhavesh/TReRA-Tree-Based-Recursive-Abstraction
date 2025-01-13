import os
import csv
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

# Function to extract text from PDFs
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

# Function to extract data from CSVs
def extract_data_from_csvs(csv_directory):
    documents = []
    for filename in os.listdir(csv_directory):
        if filename.lower().endswith(".csv"):
            file_path = os.path.join(csv_directory, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                header = next(reader)  # Read header
                rows = [", ".join(row) for row in reader]
                content = f"Header: {', '.join(header)}\nData:\n" + "\n".join(rows)
                documents.append(Document(page_content=content, metadata={"source": filename}))
    return documents

# Function to split text into chunks
def split_documents(documents, chunk_size=1024, chunk_overlap=64):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return text_splitter.split_documents(documents)

# Function to create vector store
def create_vector_store(texts, persist_directory="db"):
    model_name = "hkunlp/instructor-large"  # The model you want to use
    embeddings = HuggingFaceEmbeddings(model_name=model_name)
    db = Chroma.from_documents(texts, embeddings, persist_directory=persist_directory)
    db.persist()
    return db

# Function to retrieve relevant chunks
def retrieve_relevant_chunks(vector_store, query, k=5):
    docs = vector_store.similarity_search(query, k=k)
    return "\n".join([doc.page_content for doc in docs])

# Function to query Groq model with context
def query_groq_model_with_context(system_message, user_query, context):
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {user_query}"},
    ]
    chat_completion = client.chat.completions.create(
        messages=messages,
        model="llama3-8b-8192"
    )
    return chat_completion.choices[0].message.content

# Main Function
def main():
    analysis_type = input("What do you want to analyze? (pdf/csv/both): ").strip().lower()
    pdf_directory = input("Enter the path to the PDF directory: ")
    csv_directory = input("Enter the path to the CSV directory: ")

    documents = []
    if analysis_type in ["pdf", "both"]:
        print("Extracting text from PDFs...")
        documents.extend(extract_text_from_pdfs(pdf_directory))
    
    if analysis_type in ["csv", "both"]:
        print("Extracting data from CSVs...")
        documents.extend(extract_data_from_csvs(csv_directory))

    if not documents:
        print("No data to process. Exiting.")
        return

    print("Splitting documents into chunks...")
    texts = split_documents(documents)

    print("Creating vector store with embeddings...")
    vector_store = create_vector_store(texts)

    print("Setup complete. You can now ask questions.")
    system_message = "You are an intelligent assistant. Provide clear, concise, and accurate answers."
    while True:
        user_query = input("Ask a question (type 'exit' to quit): ")
        if user_query.lower() == 'exit':
            break
        
        print("Retrieving relevant chunks...")
        context = retrieve_relevant_chunks(vector_store, user_query)

        print("Querying Groq model...")
        answer = query_groq_model_with_context(system_message, user_query, context)
        print(f"Groq Llama: {answer}\n")

if __name__ == "__main__":
    main()
