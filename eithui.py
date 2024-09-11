import os
import PyPDF2
import streamlit as st
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

# Streamlit Interface
def main():
    st.title("PDF QA System")

    # Session state to keep track of `qa_chain`
    if 'qa_chain' not in st.session_state:
        st.session_state.qa_chain = None

    st.sidebar.header("Upload PDF Directory")
    pdf_directory = st.sidebar.text_input("Enter the path to the PDF directory:", value="pdfs")

    if st.sidebar.button("Process PDFs"):
        if not os.path.isdir(pdf_directory):
            st.sidebar.error("Invalid directory path. Please check and try again.")
        else:
            st.sidebar.text("Processing PDFs...")
            documents = extract_text_from_pdfs(pdf_directory)
            texts = split_documents(documents)
            vector_store = create_vector_store(texts)
            st.session_state.qa_chain = initialize_qa_chain(vector_store)
            st.sidebar.text("Setup complete. You can now ask questions.")

    question = st.text_input("Ask a question about the PDFs:")
    if st.button("Get Answer"):
        if st.session_state.qa_chain:
            if question:
                answer = query_qa_system(st.session_state.qa_chain, question)
                st.write(f"**Answer:** {answer['result']}")
            else:
                st.write("Please enter a question.")
        else:
            st.write("Please process PDFs first.")

if __name__ == "__main__":
    main()
