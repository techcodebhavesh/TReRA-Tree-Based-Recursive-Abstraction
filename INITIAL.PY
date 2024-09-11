import os
import PyPDF2
##from openai import OpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.schema import Document
from langchain.chains import RetrievalQA
from langchain_openai import OpenAI

# Step 1: Configure OpenAI Client to Point to Local LLM (Llama Studio)
client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

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

# Step 5: Initialize RetrievalQA Chain

def initialize_qa_chain(vector_store):
    # Assuming `OpenAI` from langchain is compatible with your local LLM
    llm = OpenAI(api_key="lm-studio", base_url="http://localhost:1234/v1", model="techcodebhavesh/AutoDashAnalyticsV1GGUF")
    
    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vector_store.as_retriever(),
        return_source_documents=True
    )
    return qa
# Step 6: Query the QA System
def query_qa_system(qa_chain, question):
    response = qa_chain({"query": question})
    return response

# Step 7: Main Function to Integrate All Steps
def main():
    pdf_directory = input("Enter the path to the PDF directory: ")  # e.g., "pdfs"
    
    print("Extracting text from PDFs...")
    documents = extract_text_from_pdfs(pdf_directory)
    
    print("Splitting documents into chunks...")
    texts = split_documents(documents)
    
    print("Creating vector store with embeddings...")
    vector_store = create_vector_store(texts)
    
    print("Initializing QA chain...")
    qa_chain = initialize_qa_chain(vector_store)
    
    print("Setup complete. You can now ask questions about the PDFs.")
    
    # Continuous Chat Loop
    history = [
        {"role": "system", "content": "You are an intelligent assistant. You always provide well-reasoned answers that are both correct and helpful."},
        {"role": "user", "content": "Hello, introduce yourself to someone opening this program for the first time. Be concise."},
    ]
    
    while True:
        question = input("Ask a question about the PDFs (type 'exit' to quit): ")
        if question.lower() == 'exit':
            break
        
        # Add the user's question to history
        history.append({"role": "user", "content": question})
        
        # Get the response from the QA system
        answer = query_qa_system(qa_chain, question)
        answer_text = answer['result']
        
        # Print the model's response
        print(f"LLM: {answer_text}\n")
        
        # Add the assistant's response to history
        history.append({"role": "assistant", "content": answer_text})

if __name__ == "__main__":
    main()
