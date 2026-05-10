import streamlit as st
from dotenv import load_dotenv
import os
from PyPDF2 import PdfReader
from langchain_text_splitters import CharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage

def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text


def get_text_chunks(raw_text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200, 
        length_function=len
    )
    chunks = text_splitter.split_text(raw_text)
    return chunks


def get_vectorstore(text_chunks):
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore


def get_llm(model_name):
    return ChatOpenAI(
        model=model_name,
        openai_api_key=os.getenv("OPENROUTER_API_KEY"),
        openai_api_base="https://openrouter.ai/api/v1",
        temperature=0.7,
        max_tokens=2000
    )


def handle_user_input(user_question):
    if 'vectorstore' not in st.session_state:
        st.warning("Please upload and process documents first!")
        return
    
    try:
        # Retrieve relevant documents using invoke()
        retriever = st.session_state.vectorstore.as_retriever(search_kwargs={"k": 3})
        docs = retriever.invoke(user_question)  # Changed from get_relevant_documents
        
        # Build context from retrieved documents
        context = "\n\n".join([doc.page_content for doc in docs])
        
        # Build chat history for context
        history_text = ""
        for msg in st.session_state.chat_history[-6:]:  # Last 3 exchanges only
            if isinstance(msg, HumanMessage):
                history_text += f"\nUser: {msg.content}"
            elif isinstance(msg, AIMessage):
                history_text += f"\nAssistant: {msg.content}"
        
        # Create prompt with context and history
        prompt = f"""Based on the following context from the documents, answer the question.
        
Previous conversation:
{history_text}

Context from documents:
{context}

Question: {user_question}

Answer the question based on the context provided. If the answer is not in the context, say so."""

        # Get response from LLM
        llm = st.session_state.llm
        response = llm.invoke(prompt)
        
        # Update chat history
        st.session_state.chat_history.append(HumanMessage(content=user_question))
        st.session_state.chat_history.append(AIMessage(content=response.content))
        
        # Display chat history
        for message in st.session_state.chat_history:
            if isinstance(message, HumanMessage):
                with st.chat_message("user"):
                    st.write(message.content)
            elif isinstance(message, AIMessage):
                with st.chat_message("assistant"):
                    st.write(message.content)
        
        # Show source documents
        with st.expander("📄 Source References"):
            for idx, doc in enumerate(docs):
                st.write(f"**Source {idx+1}:**")
                st.write(doc.page_content[:300] + "...")
                st.divider()
    
    except Exception as e:
        st.error(f"Error: {str(e)}")
        import traceback
        st.error(traceback.format_exc())


def main():
    load_dotenv()

    st.set_page_config(page_title="DocuTalk-AI", page_icon="📚")
    
    # Check for API key
    if not os.getenv("OPENROUTER_API_KEY"):
        st.error("⚠️ OPENROUTER_API_KEY not found in .env file!")
        st.stop()
    
    st.header("Chat with Multiple PDFs 📚")
    st.caption("Powered by OpenRouter Free Models")
    
    # Initialize session state
    if 'vectorstore' not in st.session_state:
        st.session_state.vectorstore = None
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'llm' not in st.session_state:
        st.session_state.llm = None
    
    user_question = st.text_input("Ask a question about your documents:")
    if user_question:
        handle_user_input(user_question)

    with st.sidebar:
        st.subheader("Your Documents")
        pdf_docs = st.file_uploader(
            "Upload your PDF files here", 
            type=["pdf"], 
            accept_multiple_files=True
        )
        
        # Model selector
        model_options = {
            "OpenRouter Auto (Best Free)": "openrouter/free",
            "Llama 3.3 70B": "meta-llama/llama-3.3-70b-instruct:free",
            "Qwen 3 Next 80B": "qwen/qwen3-next-80b-a3b-instruct:free",
            "Gemma 4 26B": "google/gemma-4-26b-a4b-it:free"
        }
        
        selected_model = st.selectbox(
            "Select Model",
            options=list(model_options.keys())
        )
        
        if st.button("Process Documents"):
            if pdf_docs:
                with st.spinner("Processing..."):
                    # Get PDF text
                    raw_text = get_pdf_text(pdf_docs)

                    # Get the text chunks
                    text_chunks = get_text_chunks(raw_text)

                    # Create the vector store
                    vectorstore = get_vectorstore(text_chunks)
                    
                    # Initialize LLM
                    llm = get_llm(model_options[selected_model])
                    
                    # Store in session state
                    st.session_state.vectorstore = vectorstore
                    st.session_state.llm = llm
                    st.session_state.chat_history = []  # Reset chat history
                    
                    st.success("✅ Documents processed! Ask your questions.")
            else:
                st.warning("Please upload at least one PDF file.")
        
        # Clear chat button
        if st.button("Clear Chat History"):
            st.session_state.chat_history = []
            st.rerun()

if __name__ == "__main__":
    main()