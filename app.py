import streamlit as st
from dotenv import load_dotenv


def main():
    load_dotenv()

    st.set_page_config(page_title= "DocuTalk-AI", page_icon=":books:")
    st.header("Chat with Multiple PDFs :books: ")
    st.text_input("Ask a question about your documents here...")

    with st.sidebar:
        st.subheader("Your Documents")
        st.file_uploader("Upload your PDF files here", type=["pdf"], accept_multiple_files=True)
        st.button("Process Documents")


if __name__ == "__main__":
    main()