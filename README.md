# DOCU QUERY AI 📄🤖

An interactive Streamlit-based AI application that allows you to query the contents of a PDF using natural language powered by Ollama LLM and LlamaIndex.

## 🚀 Features

- Upload any PDF document.
- Chat with your document using natural language.
- Powered by `LlamaIndex`, `LangChain`, and `Ollama LLM`.
- Uses HuggingFace for embeddings.
- Friendly and clean UI using Streamlit.

## 🛠️ Setup Instructions

1. **Clone the repository:**

```bash
git clone https://github.com/your-username/docuquery-ai.git
cd docuquery-ai
```

2. **Install dependencies**
 
```bash
pip install -r requirements.txt
```

3. **Run the app:**
   
```bash
streamlit run app.py
```

📁 **Directory Structure**
docuquery-ai/
├── data/               # Folder for uploaded PDFs
├── db/                 # Persisted vector index
├── app.py              # Main application file

🧠 **Technologies**
Streamlit
LangChain
LlamaIndex
Ollama
HuggingFace Transformers
