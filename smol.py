

from smol_agents import Agent
import PyPDF2
from transformers import pipeline

def extract_text_from_pdf(pdf_path):
    """Extracts text from a given PDF file."""
    try:
        with open(pdf_path, 'rb') as pdf_file:
            reader = PyPDF2.PdfReader(pdf_file)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
            return text
    except Exception as e:
        return f"Error reading PDF: {e}"

def answer_question_from_pdf(pdf_path, question):
    """Answers a question based on the content of a PDF."""
    # Extract text from the PDF
    pdf_text = extract_text_from_pdf(pdf_path)
    
    if not pdf_text.strip():
        return "No text found in the PDF."
    
    # Use a Hugging Face model for question answering
    qa_pipeline = pipeline("question-answering", model="distilbert-base-uncased-distilled-squad")
    
    # Provide the text and question to the model
    result = qa_pipeline(question=question, context=pdf_text)
    return result["answer"]

# Define the Smol Agent task
pdf_agent = Agent(tasks={
    "answer_question": answer_question_from_pdf
})

# Example usage
if __name__ == "__main__":
    pdf_file_path ="D:/PDF_CONNECT/pdf/2407.09025v1 (1).pdf"  # Replace with your PDF file path
    user_question = "What is the purpose of this document?"  # Replace with your question
    
    # Run the agent task
    answer = pdf_agent.run(task="answer_question", pdf_path=pdf_file_path, question=user_question)
    print(f"Answer: {answer}")