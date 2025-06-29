import argparse
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.prompts import ChatPromptTemplate
import time
import traceback
from colorama import init, Fore, Back, Style

# Import logger if available
try:
    from logger_config import logger, log_request, log_response, log_error
except ImportError:
    import logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    def log_request(*args, **kwargs): pass
    def log_response(*args, **kwargs): pass
    def log_error(*args, **kwargs): pass

# Initialize colorama for cross-platform colored output
init(autoreset=True)

CHROMA_DB_PATH = "./chroma_db_openai"

PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
"""

def print_colored_response(response_text, sources):
    """Print the response with colored formatting"""
    print("\n" + "="*80)
    print(f"{Fore.CYAN}{Back.BLUE}{Style.BRIGHT}  AI RESPONSE {Style.RESET_ALL}")
    print("="*80)
    print(f"{Fore.GREEN}{Style.BRIGHT}{response_text}{Style.RESET_ALL}")
    print("\n" + "-"*80)
    print(f"{Fore.YELLOW}{Style.BRIGHT} Sources:{Style.RESET_ALL}")
    for i, source in enumerate(sources, 1):
        print(f"{Fore.WHITE}  {i}. {source}{Style.RESET_ALL}")
    print("="*80 + "\n")

def main():
    logger.info("=== Starting OpenAI RAG Query ===")
    
    #Create CLI
    parser = argparse.ArgumentParser()
    parser.add_argument("query_text", type=str, help="The query text.")
    args = parser.parse_args()
    query_text = args.query_text
    
    logger.info(f"Query received: {query_text}")
    log_request("QUERY", query_text)

    try:
        #prepare the DB
        logger.info("Initializing OpenAI embeddings")
        embedding_functions = OpenAIEmbeddings()
        db = Chroma(persist_directory=CHROMA_DB_PATH, embedding_function=embedding_functions)
        logger.info("Database loaded successfully")

        #Search the DB
        logger.info(f"Searching database for relevant documents")
        start_time = time.time()
        results = db.similarity_search_with_relevance_scores(query_text, k=3)
        search_time = time.time() - start_time
        
        log_response("SEARCH", "SUCCESS", response_time=search_time, 
                    response_data=f"Found {len(results)} results")
        
        if len(results) == 0:
            logger.warning("No matching results found")
            print(f"{Fore.RED}❌ Unable to find matching results{Style.RESET_ALL}")
            return
        
        # Check similarity threshold
        best_score = results[0][1]
        if best_score < 0.7:
            logger.warning(f"Best match has low similarity score: {best_score:.3f}")
            print(f"{Fore.YELLOW}⚠️  Warning: Best match has low similarity score: {best_score:.3f}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}   Proceeding anyway...{Style.RESET_ALL}")
        
        # Display search results
        print(f"\n{Fore.CYAN}🔍 Search Results:{Style.RESET_ALL}")
        for i, (doc, score) in enumerate(results, 1):
            print(f"{Fore.WHITE}  {i}. Score: {score:.3f} - {doc.page_content[:100]}...{Style.RESET_ALL}")
        
        # Prepare context and prompt
        logger.info("Preparing context and prompt")
        context_text = "\n\n --- \n\n".join([doc.page_content for doc, _score in results])
        prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
        prompt = prompt_template.format(context=context_text, question=query_text)
        
        # Log prompt for debugging (truncated)
        logger.debug(f"PAYLOAD | Generated prompt (truncated): {prompt[:500]}...")
        
        # Generate AI response
        logger.info("Generating AI response")
        model = ChatOpenAI()
        start_time = time.time()
        response_text = model.predict(prompt)
        response_time = time.time() - start_time
        
        log_response("AI_RESPONSE", "SUCCESS", response_time=response_time)
        logger.info(f"AI response generated in {response_time:.2f}s")

        # Extract sources
        sources = [doc.metadata.get("source", "Unknown") for doc, _score in results]
        
        # Print colored response
        print_colored_response(response_text, sources)
        
        # Log final summary
        logger.info("=== Query completed successfully ===")
        log_response("QUERY_COMPLETE", "SUCCESS", 
                    response_data=f"Query: {query_text[:100]}... | Sources: {len(sources)}")
        
    except Exception as e:
        error_msg = f"Query failed: {str(e)}"
        logger.error(error_msg)
        log_error("QUERY_FAILED", str(e), traceback.format_exc())
        print(f"{Fore.RED}❌ {error_msg}{Style.RESET_ALL}")
        raise

if __name__ == "__main__":
    main()