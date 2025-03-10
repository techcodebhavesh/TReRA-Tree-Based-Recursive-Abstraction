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

prcode = ""

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
    def __init__(self, model_name="llama-3.3-70b-versatile", template_dir="templates"):
        self.model_name = model_name
        self.client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        self.template_dir = template_dir

    def load_template(self, prcode):
        """Reads the appropriate template file based on prcode."""
        template_file = os.path.join(self.template_dir, f"{prcode}.txt")
        if not os.path.exists(template_file):
            template_file = os.path.join(self.template_dir, "default.txt")  # Fallback template
        
        with open(template_file, "r", encoding="utf-8") as file:
            return file.read()

    def answer_question(self, context, question):
        global prcode
        template_content = self.load_template(prcode)
        
        # Replace placeholders
        prompt = template_content.replace("{{context}}", context).replace("{{question}}", question)
        
        print(f"Executing {prcode.capitalize() if prcode else 'Default'}")
        messages = [{"role": "user", "content": prompt}]
        
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

processed_text_directory = '../processed_output'  # Path to the folder containing processed text files
combined_text = load_text_files(processed_text_directory)
RA.add_documents(combined_text)

@app.route('/ask', methods=['POST'])
def ask_question():
    global prcode
    data = request.get_json()
    question = data.get('question')
    prcode = data.get('prcode')
    
    if not question:
        return jsonify({'error': 'Question is required'}), 400

    answer = RA.answer_question(question=question)
    prcode=None
    return jsonify({'answer': answer})

if __name__ == '__main__':
    app.run(debug=False)