import streamlit as st
from dotenv import load_dotenv
from llama_index.core import StorageContext, load_index_from_storage, VectorStoreIndex, SimpleDirectoryReader, Settings, ChatPromptTemplate
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from langchain.chat_models import ChatOllama
import os
import base64

# Load environment variables
load_dotenv()

# Ollama LLM configuration (using LangChain)
ollama_llm = ChatOllama(
    model="llama3.2:1b",  
)
# Embedding model (still using HuggingFace embeddings)
embed_model = HuggingFaceEmbeddings(
    model_name="BAAI/bge-large-en-v1.5"
)

# Configure LlamaIndex Settings
Settings.llm = ollama_llm
Settings.embed_model = embed_model

# Storage paths
PERSIST_DIR = "./db"
DATA_DIR = "data"

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(PERSIST_DIR, exist_ok=True)

def displayPDF(file):
    """Embed PDF file in Streamlit app."""
    with open(file, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="600" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

def data_ingestion():
    """Load and index documents from the data directory."""
    documents = SimpleDirectoryReader(DATA_DIR).load_data()
    storage_context = StorageContext.from_defaults()
    index = VectorStoreIndex.from_documents(documents, storage_context=storage_context)
    index.storage_context.persist(persist_dir=PERSIST_DIR)

def handle_query(query):
    """Retrieve answer from the index for a given query."""
    storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
    index = load_index_from_storage(storage_context)

    chat_text_qa_msgs = [
        (
            "user",
            """You are a Q&A assistant. Created by Harish an AI Automation Engineer. Your primary objective is to provide accurate and helpful answers based on the instructions and context provided.
            If a question falls outside the given context or scope, kindly guide the user to ask questions that align with the provided context.

            Context:
            {context_str}

            Question:
            {query_str}
            """
        )
    ]

    text_qa_template = ChatPromptTemplate.from_messages(chat_text_qa_msgs)
    query_engine = index.as_query_engine(text_qa_template=text_qa_template)
    answer = query_engine.query(query)

    if hasattr(answer, 'response'):
        return answer.response
    elif isinstance(answer, dict) and 'response' in answer:
        return answer['response']
    else:
        return "Sorry, I couldn't find an answer."

# Streamlit UI
st.title("Your PDF Assistant 📄")
st.markdown("Get insights from your data – just chat!👇")

if 'messages' not in st.session_state:
    st.session_state.messages = [{'role': 'assistant', "content": 'I can answer your questions about a PDF. Just upload it!'}]

with st.sidebar:
    st.markdown("**Created by [Harish]**")
    st.title(':blue[Get Started]:')
    uploaded_file = st.file_uploader("Upload your PDF and Click Submit")
    if st.button("Submit"):
        with st.spinner("Processing..."):
            filepath = os.path.join(DATA_DIR, "saved_pdf.pdf")
            with open(filepath, "wb") as f:
                f.write(uploaded_file.getbuffer())
            # displayPDF(filepath)
            data_ingestion()
            st.success("Done")

user_prompt = st.chat_input("Ask me anything about the data inside the document:")
if user_prompt:
    st.session_state.messages.append({'role': 'user', "content": user_prompt})
    response = handle_query(user_prompt)
    st.session_state.messages.append({'role': 'assistant', "content": response})

for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.write(message['content'])
