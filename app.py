from flask import Flask, request, render_template, jsonify
from werkzeug.utils import secure_filename
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain
from langchain_community.chat_models import ChatOpenAI
import os

app = Flask(__name__)

# Set up OpenAI API key
openai_api_key = os.getenv("OPENAI_API_KEY") 

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Initialize variables
documents = []
qa_chain = None
chat_history = []

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    global documents, qa_chain
    if 'file' not in request.files:
        return jsonify({"error": "No file part"})
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"})
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Load and process the document
        if filename.endswith('.pdf'):
            loader = PyPDFLoader(filepath)
        else:
            loader = TextLoader(filepath)
        
        documents.extend(loader.load())
        
        # Split the documents into chunks
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        texts = text_splitter.split_documents(documents)
        
        # Create embeddings and store in FAISS index
        embeddings = OpenAIEmbeddings()
        db = FAISS.from_documents(texts, embeddings)
        
        # Create a conversational chain
        qa_chain = ConversationalRetrievalChain.from_llm(
            ChatOpenAI(temperature=0.7),
            db.as_retriever(),
            return_source_documents=True
        )
        
        return jsonify({"message": "File uploaded and processed successfully"})
    return jsonify({"error": "File type not allowed"})

@app.route('/chat', methods=['POST'])
def chat():
    global qa_chain, chat_history
    if not qa_chain:
        return jsonify({"error": "No documents uploaded yet"})
    
    user_message = request.json.get('message', '')
    
    try:
        result = qa_chain({"question": user_message, "chat_history": chat_history})
        
        # Update chat history
        chat_history.append((user_message, result['answer']))
        
        return jsonify({
            "answer": result['answer']
        })
    except Exception as e:
        app.logger.error(f"An error occurred: {str(e)}")
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)