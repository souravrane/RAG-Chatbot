from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

from dotenv import load_dotenv
import shutil
import os

load_dotenv()

DATA_PATH = "./sample_data/books"
CHROMA_DB_PATH = "./chroma_db_openai"

def load_documents(dir : str):
    loader = DirectoryLoader(dir, glob="*.md")
    documents = loader.load()
    return documents

def chunk_documents(documents : list[Document]):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=500, length_function=len, add_start_index=True)
    chunks = text_splitter.split_documents(documents)
    print(f"Loaded {len(documents)} documents and split into {len(chunks)} chunks")

    document = chunks[10]
    print(document.page_content)
    print(document.metadata)
    return chunks

def generate_datastore():
    documents = load_documents(DATA_PATH)
    chunks = chunk_documents(documents)
    save_to_chroma(chunks)

def save_to_chroma(chunks : list[Document]):
    # remove the database if it exists
    if os.path.exists(CHROMA_DB_PATH):
        shutil.rmtree(CHROMA_DB_PATH)
    
    database = Chroma.from_documents(
        documents=chunks,
        embedding=OpenAIEmbeddings(),
        persist_directory=CHROMA_DB_PATH
    )
    database.persist()
    print(f"Saved {len(chunks)} chunks to {CHROMA_DB_PATH}.")
        

def main():
    generate_datastore()

if __name__ == "__main__":
    main()