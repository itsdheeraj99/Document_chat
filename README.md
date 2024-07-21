# Document Chat with LangChain and Flask

## Description

This project is a web application that allows users to upload documents (PDF or TXT), process them using LangChain, and then chat with an AI about the contents of these documents. The application uses Flask for the backend, LangChain for document processing and AI interactions, and a simple HTML frontend for user interaction.

Key features:
- Document upload (PDF and TXT support)
- Document processing with LangChain
- Interactive chat interface to query document contents
- Responsive web design

## Prerequisites

Before you begin, ensure you have the following:
- Python 3.7+
- pip (Python package manager)
- An OpenAI API key. To get your own API key, visit: https://platform.openai.com/api-keys

## Installation

Follow these steps to set up the project:

1. Clone the repository:
`git clone https://github.com/itsdheeraj99/Document_chat.git`

2. Create and activate a virtual environment:
`python -m venv venv`
`source venv/bin/activate`  
On Windows, use `venv\Scripts\activate`

3. Install the required packages:
`pip install -r requirements.txt`

4. Set up your OpenAI API key:
- Create a `.env` file in the project root
- Add the following line to the file:
  ```
  OPENAI_API_KEY=your_api_key_here
  ```

## Usage

To run the application:

1. Start the Flask server:
 Run `python app.py` or run `flask --app app run`

2. Open a web browser and navigate to `http://localhost:5000`

3. Use the interface to:
- Upload documents
- Ask questions about the uploaded documents
- View AI-generated responses

## Project Structure

- `app.py`: The main Flask application
- `templates/index.html`: The HTML template for the web interface
- `uploads/`: Directory where uploaded files are stored

## Contributing

Contributions to this project are welcome. 