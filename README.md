# DocuTalk-AI: Intelligent Multi-PDF Conversational Agent

<div align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit"/>
  <img src="https://img.shields.io/badge/LangChain-121212?style=for-the-badge&logo=langchain&logoColor=white" alt="LangChain"/>
  <img src="https://img.shields.io/badge/OpenRouter-000000?style=for-the-badge&logo=openai&logoColor=white" alt="OpenRouter"/>
</div>

## 📌 Overview
**DocuTalk-AI** is a powerful Retrieval-Augmented Generation (RAG) application that allows users to have intelligent conversations with multiple PDF documents simultaneously. By leveraging open-source LLMs through OpenRouter and vector embeddings via HuggingFace, it transforms static documents into an interactive knowledge base.

Whether you're analyzing complex legal contracts (like rent agreements), lengthy research papers, or financial reports, DocuTalk-AI extracts precise answers with source references.

## ✨ Key Features
- **Multi-Document Processing**: Seamlessly upload and process multiple PDF files in a single session.
- **Conversational Memory**: The AI remembers the context of the conversation, allowing for natural, follow-up questions.
- **Intelligent RAG Architecture**: Uses LangChain and FAISS for highly efficient and accurate document retrieval.
- **Source Verification**: Every answer comes with an expandable "Source References" section, showing exactly where in the document the information was found.


## 🛠️ Tech Stack
- **Frontend/Backend**: [Streamlit](https://streamlit.io/)
- **Orchestration**: [LangChain](https://www.langchain.com/)
- **Text Extraction**: `PyPDF2`
- **Embeddings**: `HuggingFaceEmbeddings` (`sentence-transformers/all-MiniLM-L6-v2`)
- **Vector Database**: `FAISS`
- **LLM Integration**: `ChatOpenAI` wrapper configured for OpenRouter

## 🚀 Real-World Use Case: Legal Document Analysis
In the demonstration, DocuTalk-AI was used to analyze a standard **Rent Agreement**. 

**Example Interactions:**
> **User**: "What is the security deposit amount?"  
> **DocuTalk-AI**: "The security deposit amount is Rs. 50,000."

> **User**: "What happens if the tenant pays rent after the 7th of the month?"  
> **DocuTalk-AI**: "The documents state that the tenant must pay the rent on or before the 7th day of each month without fail. They do not specify any consequence or process for paying after that date..."

*This demonstrates the model's ability to not only extract exact figures but also logically infer when information is missing from the legal text, preventing hallucinations.*

## 🧠 How It Works Under the Hood
1. **Document Loading**: PyPDF2 extracts raw text from the uploaded PDFs.
2. **Text Splitting**: LangChain's `CharacterTextSplitter` breaks the text into manageable chunks (1000 characters with 200 character overlap) to preserve context.
3. **Embedding Generation**: Text chunks are converted into dense vector representations using HuggingFace's MiniLM model.
4. **Vector Storage**: The embeddings are indexed in a local FAISS database for lightning-fast similarity search.
5. **Retrieval & Generation**: When a user asks a question, the system queries the FAISS index for the most relevant chunks, injects them into a prompt alongside the conversation history, and sends it to the selected LLM to generate a coherent answer.



## 💡 Step-by-Step Usage Guide
1. **Launch the Basic GUI**: Start the Streamlit application and select your preferred open-source model from the sidebar dropdown.

<img width="1917" height="1021" alt="image" src="https://github.com/user-attachments/assets/e246cbf4-a529-4304-b05d-a870918dd2f8" />


2. **Upload Documents**: Drag and drop your PDF files (e.g., `Rent Agreement.pdf`) into the designated upload area in the sidebar.



<img width="1917" height="1021" alt="Screenshot 2026-05-11 004306 - Copy" src="https://github.com/user-attachments/assets/cac093b8-af14-47f7-8db5-e74d9f9362a4" />

3. **Process and Create Vectors**: Click the "Process Documents" button. The application will extract the text, split it into chunks, generate embeddings using Hugging Face, and store them in a FAISS vector database.


<img width="1912" height="1013" alt="image" src="https://github.com/user-attachments/assets/d4440a2c-f6e5-4d14-8c9a-7275aeb9b3b5" />


4. **Ask Questions**: Once processing is complete, use the main chat interface to ask specific questions about your uploaded documents and receive context-aware answers.


<img width="1915" height="1015" alt="image" src="https://github.com/user-attachments/assets/0c998d0c-2a28-466a-b786-d44135a0d93c" />

