import streamlit as st
from streamlit_chat import message
import os
import shutil
from pathlib import Path
from typing import List
from langchain.document_loaders import (
    CSVLoader,
    EverNoteLoader,
    GitLoader,
    NotebookLoader,
    OnlinePDFLoader,
    PDFMinerLoader,
    PythonLoader,
    TextLoader,
    UnstructuredEPubLoader,
    UnstructuredFileLoader,
    UnstructuredHTMLLoader,
    UnstructuredMarkdownLoader,
    UnstructuredODTLoader,
    UnstructuredPowerPointLoader,
    UnstructuredWordDocumentLoader,
    WebBaseLoader,
)
from langchain.document_loaders.base import BaseLoader
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from tqdm import tqdm
from transformers import AutoTokenizer, AutoModelForQuestionAnswering

FILE_LOADER_MAPPING = {
    ".csv": (CSVLoader, {"encoding": "utf-8"}),
    ".doc": (UnstructuredWordDocumentLoader, {}),
    ".docx": (UnstructuredWordDocumentLoader, {}),
    ".enex": (EverNoteLoader, {}),
    ".epub": (UnstructuredEPubLoader, {}),
    ".html": (UnstructuredHTMLLoader, {}),
    ".md": (UnstructuredMarkdownLoader, {}),
    ".odt": (UnstructuredODTLoader, {}),
    ".pdf": (PDFMinerLoader, {}),
    ".ppt": (UnstructuredPowerPointLoader, {}),
    ".pptx": (UnstructuredPowerPointLoader, {}),
    ".txt": (TextLoader, {"encoding": "utf8"}),
    ".ipynb": (NotebookLoader, {}),
    ".py": (PythonLoader, {}),
    # Add more mappings for other file extensions and loaders as needed
}

def main():
    st.title("File Upload and Text Prompt")

    
    # Directory loading
    st.header("Upload Directory")
    uploaded_directory = st.text_input("Choose a directory")

    if uploaded_directory is not None:
        file_paths = get_file_paths_from_directory(uploaded_directory)
        documents = load_documents(file_paths)
        print(documents)


def save_file(uploaded_file):
    if uploaded_file is not None:
        file_contents = uploaded_file.read()
        file_path = os.path.join(os.getcwd(), "uploads", uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(file_contents)
            f.close()
    else:
        st.write("No file uploaded")

def get_file_paths_from_directory(uploaded_dir):
    file_paths = []
    for root, _, files in os.walk(uploaded_dir):
        for file in files:
            file_paths.append(os.path.join(root, file))
    return file_paths

def load_documents(file_paths):
    documents = []
    for file_path in file_paths:
        documents.append(load_document(file_path))
    return documents

def load_document(uploaded_filename):
    ext = "." + uploaded_filename.rsplit(".", 1)[-1]
    if ext in FILE_LOADER_MAPPING:
        loader_class, loader_args = FILE_LOADER_MAPPING[ext]
        loader = loader_class(uploaded_filename, **loader_args)
    else: return 
    return loader.load()

if __name__ == "__main__":
    main()

