from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.chains.question_answering import load_qa_chain
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.vectorstores import FAISS
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
from PyPDF2 import PdfReader
import streamlit as st
from geminiAPI import*
import shutil
import io
import os

# Load environment variables
load_dotenv()

# Configure Google API Key
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    st.error("Google API Key is not set. Please add it to your .env file.")
else:
    genai.configure(api_key=api_key)

# Utility Functions
def dltfaiss():
    """Delete the existing FAISS index directory."""
    try:
        shutil.rmtree("faiss_index")
    except FileNotFoundError:
        pass

def get_pdf_text(pdf_docs):
    """Extract text from uploaded PDF files."""
    text = ""
    for pdf in pdf_docs:
        try:
            pdf_reader = PdfReader(io.BytesIO(pdf.read()))
            for page in pdf_reader.pages:
                text += page.extract_text()
        except Exception as e:
            st.error(f"Error reading PDF: {e}")
    return text

def get_vector_store(text_chunks):
    """Generate and save a FAISS index from text chunks."""
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    vector_store.save_local("faiss_index")

def get_text_chunks(text):
    """Split text into manageable chunks."""
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    return text_splitter.split_text(text)

def get_conversational_chain():
    """Create a conversational QA chain."""
    prompt_template = """
    Answer the question as detailed as possible in simple language based on the provided context. If the answer is not in the context, say,
    "Answer is not available in the context." Do not provide incorrect answers.

    Context:
    {context}

    Question:
    {question}

    Answer:
    """
    model = ChatGoogleGenerativeAI(model="gemini-1.5-pro-latest", temperature=0.3)
    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    return load_qa_chain(model, chain_type="stuff", prompt=prompt)

def user_input(user_question):
    """Process user queries using the FAISS index."""
    if os.path.exists("faiss_index"):
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        try:
            new_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
            docs = new_db.similarity_search(user_question)
            chain = get_conversational_chain()
            response = chain({"input_documents": docs, "question": user_question}, return_only_outputs=True)
            return response.get("output_text", "No response generated.")
        except Exception as e:
            return f"Error processing your question: {e}"
    else:
        return "You did not provide any PDF. First, upload the PDF."

# Streamlit App
st.title("Fusion Chat 🤖")
st.page_link("pages/1_Text_Fusion.py", label="Text Fusion", icon="1️⃣")
st.page_link("pages/2_Image_Fusion.py", label="Image Fusion", icon="2️⃣")

st.subheader("Text Fusion")

# Sidebar for PDF upload
with st.sidebar:
    st.title("Menu:")
    pdf_docs = st.file_uploader("Upload your readable PDF Files", accept_multiple_files=True)
    if pdf_docs and len(pdf_docs) > 0:
        if st.button("Submit & Process"):
            with st.spinner("Processing..."):
                raw_text = get_pdf_text(pdf_docs)
                if raw_text.strip():
                    text_chunks = get_text_chunks(raw_text)
                    get_vector_store(text_chunks)
                    st.success("Processing complete. You can now ask questions!")
                else:
                    st.error("No text extracted from the uploaded PDFs.")
    else:
        st.write("No files uploaded.")

# User interaction for questions
if pdf_docs:
    user_question = st.chat_input("Ask a question from the uploaded PDF files:")
    if user_question:
        st.write(f"**👤 User:** {user_question}")
        response = user_input(user_question)
        st.write(f"**🤖:** {response}")
