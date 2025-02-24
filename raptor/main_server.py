from flask import Flask, request, jsonify
from flask_cors import CORS

from raptor import RetrievalAugmentation 
from raptor import BaseSummarizationModel, BaseQAModel, BaseEmbeddingModel, RetrievalAugmentationConfig
from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer, pipeline
from groq import Groq
import os
import umap
import torch

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Define the Summarization Model
class GEMMASummarizationModel(BaseSummarizationModel):
    def __init__(self, model_name="llama-3.3-70b-versatile"):
        self.model_name = model_name
        self.client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

    def summarize(self, context, max_tokens=1024):
        messages = [
            {
                "role": "user",
                "content": f"Write a summary of the following, including as many key details as possible: {context}",
            }
        ]
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            max_tokens=max_tokens,
            temperature=0.7,
            top_p=0.95,
        )
        summary = response.choices[0].message.content.strip()
        return summary

# Define the QA Model
class GEMMAQAModel(BaseQAModel):
    def __init__(self, model_name="llama-3.3-70b-versatile"):
        self.model_name = model_name
        self.client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

    def answer_question(self, context, question,prcode):
        if(prcode=="te_code"):
            messages = [
                {
                    "role": "user",
                    "content": f"Given Context: {context} Give the  TE CODE required as per the context only to the question {question} in a clear manner. Present the response in Markdown format with excellent UI/UX design, using headings, bullet points, and well-formatted sections for readability. Incorporate relevant charts, diagrams, and visual elements to enhance understanding and navigation. Ensure the explanation is detailed yet concise, making it easy for the reader to grasp the process intuitively.",
                }
            ]
        elif(prcode=="flowchart"):
            messages = [
                {
                    "role": "user",
                    "content": f"Given Context: {context} Give the  step-by-step best full mermaid js code to the question {question} in a clear and easy-to-follow manner. Present the response in Markdown format with excellent UI/UX design, using headings, bullet points, and well-formatted sections for readability. Incorporate relevant charts, diagrams, and visual elements to enhance understanding and navigation. Ensure the explanation is detailed yet concise, making it easy for the reader to grasp the process intuitively.",
                }
            ]
        elif(prcode=="detailed_answer"):
            messages = [
                {
                    "role": "user",
                    "content": f"Given Context: {context} Give the  step-by-step best full answer to the question {question} in a clear and easy-to-follow manner. Present the response in Markdown format with excellent UI/UX design, using headings, bullet points, and well-formatted sections for readability. Incorporate relevant charts, diagrams, and visual elements to enhance understanding and navigation. Ensure the explanation is detailed yet concise, making it easy for the reader to grasp the process intuitively.",
                }
            ]
        elif(prcode=="bi_capable"):
            messages = [
                {
                    "role": "user",
                    "content": f"Given Context: {context} Give the  step-by-step best full mermaid js code for the charts to the question {question} in a clear and easy-to-follow manner.Give the charts and some counters as well  for some numbers. Present the response in Markdown format with excellent UI/UX design, using headings, bullet points, and well-formatted sections for readability. Incorporate relevant charts, diagrams, and visual elements to enhance understanding and navigation. Ensure the explanation is detailed yet concise, making it easy for the reader to grasp the process intuitively.",
                }
            ]
        else:
            messages = [
                {
                    "role": "user",
                    "content": f"Given Context: {context} Give the  step-by-step best full answer to the question {question} in a clear and easy-to-follow manner. Present the response in Markdown format with excellent UI/UX design, using headings, bullet points, and well-formatted sections for readability. Incorporate relevant charts, diagrams, and visual elements to enhance understanding and navigation. Ensure the explanation is detailed yet concise, making it easy for the reader to grasp the process intuitively.",
                }
            ]
        # Remove unsupported arguments (e.g., top_k, top_p)
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            max_tokens=1024,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()


# Define the Embedding Model
class SBertEmbeddingModel(BaseEmbeddingModel):
    def __init__(self, model_name="sentence-transformers/multi-qa-mpnet-base-cos-v1"):
        self.model = SentenceTransformer(model_name)

    def create_embedding(self, text):
        return self.model.encode(text)
    
os.environ["GROQ_API_KEY"] = "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"

# Configure Retrieval Augmentation
RAC = RetrievalAugmentationConfig(
    summarization_model=GEMMASummarizationModel(),
    qa_model=GEMMAQAModel(),
    embedding_model=SBertEmbeddingModel()
)

RA = RetrievalAugmentation(config=RAC)

# Load processed text files
def load_text_files(directory):
    combined_text = ""
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            with open(os.path.join(directory, filename), 'r', encoding='utf-8') as file:
                combined_text += file.read() + "\n"
    return combined_text

processed_text_directory = 'D:/PDF_CONNECT/processed_output'  # Path to the folder containing processed text files
combined_text = load_text_files(processed_text_directory)
RA.add_documents(combined_text)

@app.route('/ask', methods=['POST'])
def ask_question():
    data = request.get_json()
    question = data.get('question')
    
    if not question:
        return jsonify({'error': 'Question is required'}), 400

    answer = RA.answer_question(question=question)
    return jsonify({'answer': answer})

if __name__ == '__main__':
    app.run(debug=False)
