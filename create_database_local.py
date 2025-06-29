from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain_community.vectorstores import Chroma
from langchain.embeddings.base import Embeddings
from sentence_transformers import SentenceTransformer
import time
import traceback

from dotenv import load_dotenv
from logger_config import logger, log_request, log_response, log_error, log_database_operation
import shutil
import os

load_dotenv()

DATA_PATH = "./sample_data/books"
CHROMA_DB_PATH = "./chroma_db"

class SentenceTransformerEmbeddings(Embeddings):
    def __init__(self, model_name="sentence-transformers/all-MiniLM-L6-v2"):
        logger.info(f"Initializing SentenceTransformer with model: {model_name}")
        try:
            self.model = SentenceTransformer(model_name)
            logger.info("SentenceTransformer model loaded successfully")
        except Exception as e:
            log_error("MODEL_INIT", str(e), traceback.format_exc())
            raise
    
    def embed_documents(self, texts):
        logger.debug(f"PAYLOAD | Embedding {len(texts)} documents")
        try:
            start_time = time.time()
            embeddings = self.model.encode(texts).tolist()
            response_time = time.time() - start_time
            log_response("EMBEDDING", "SUCCESS", response_time=response_time)
            logger.debug(f"PAYLOAD | Generated {len(embeddings)} embeddings")
            return embeddings
        except Exception as e:
            log_error("EMBEDDING", str(e), traceback.format_exc())
            raise
    
    def embed_query(self, text):
        logger.debug(f"PAYLOAD | Embedding query: {text[:100]}...")
        try:
            start_time = time.time()
            embedding = self.model.encode([text]).tolist()[0]
            response_time = time.time() - start_time
            log_response("QUERY_EMBEDDING", "SUCCESS", response_time=response_time)
            return embedding
        except Exception as e:
            log_error("QUERY_EMBEDDING", str(e), traceback.format_exc())
            raise

def load_documents(dir : str):
    logger.info(f"Loading documents from directory: {dir}")
    log_request("DOCUMENT_LOAD", dir)
    
    try:
        loader = DirectoryLoader(dir, glob="*.md")
        documents = loader.load()
        log_response("DOCUMENT_LOAD", "SUCCESS", response_data=f"Loaded {len(documents)} documents")
        logger.info(f"Successfully loaded {len(documents)} documents")
        return documents
    except Exception as e:
        log_error("DOCUMENT_LOAD", str(e), traceback.format_exc())
        raise

def chunk_documents(documents : list[Document]):
    logger.info("Starting document chunking process")
    log_request("CHUNKING", f"Processing {len(documents)} documents")
    
    try:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, 
            chunk_overlap=500, 
            length_function=len, 
            add_start_index=True
        )
        
        start_time = time.time()
        chunks = text_splitter.split_documents(documents)
        response_time = time.time() - start_time
        
        log_response("CHUNKING", "SUCCESS", response_data=f"Created {len(chunks)} chunks", response_time=response_time)
        logger.info(f"Loaded {len(documents)} documents and split into {len(chunks)} chunks")

        # Log sample chunk for debugging
        if chunks:
            document = chunks[10] if len(chunks) > 10 else chunks[0]
            logger.debug(f"PAYLOAD | Sample chunk content: {document.page_content[:200]}...")
            logger.debug(f"PAYLOAD | Sample chunk metadata: {document.metadata}")
        
        return chunks
    except Exception as e:
        log_error("CHUNKING", str(e), traceback.format_exc())
        raise

def generate_datastore():
    logger.info("Starting datastore generation process")
    try:
        documents = load_documents(DATA_PATH)
        chunks = chunk_documents(documents)
        save_to_chroma(chunks)
        logger.info("Datastore generation completed successfully")
    except Exception as e:
        log_error("DATASTORE_GENERATION", str(e), traceback.format_exc())
        raise

def save_to_chroma(chunks : list[Document]):
    logger.info("Starting Chroma database creation")
    log_request("CHROMA_CREATE", f"Creating database with {len(chunks)} chunks")
    
    try:
        # remove the database if it exists
        if os.path.exists(CHROMA_DB_PATH):
            logger.info(f"Removing existing database at {CHROMA_DB_PATH}")
            shutil.rmtree(CHROMA_DB_PATH)
            log_database_operation("DELETE", "chroma_db", result="Database removed")
        
        # Use our custom embeddings class
        logger.info("Initializing embeddings model")
        embeddings = SentenceTransformerEmbeddings()
        
        # Create database
        start_time = time.time()
        database = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            persist_directory=CHROMA_DB_PATH
        )
        response_time = time.time() - start_time
        
        log_response("CHROMA_CREATE", "SUCCESS", response_time=response_time)
        log_database_operation("CREATE", "chroma_db", data=f"{len(chunks)} chunks", result="Database created successfully")
        
        # Chroma now auto-persists, so no need to call persist()
        logger.info(f"Saved {len(chunks)} chunks to {CHROMA_DB_PATH}.")
        
    except Exception as e:
        log_error("CHROMA_CREATE", str(e), traceback.format_exc())
        raise

def main():
    logger.info("=== Starting RAG Chatbot Database Creation ===")
    try:
        generate_datastore()
        logger.info("=== Database Creation Completed Successfully ===")
    except Exception as e:
        logger.error(f"=== Database Creation Failed: {str(e)} ===")
        raise

if __name__ == "__main__":
    main() 