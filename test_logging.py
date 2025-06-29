from logger_config import logger, log_request, log_response, log_error, log_database_operation
import time
import json

def test_logging_functionality():
    """Test all logging functions"""
    
    logger.info("=== Testing Logging Functionality ===")
    
    # Test request logging
    sample_payload = {
        "query": "What is Alice in Wonderland about?",
        "user_id": "user123",
        "timestamp": "2024-01-15T10:30:00Z"
    }
    
    sample_headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer token123",
        "User-Agent": "RAG-Chatbot/1.0"
    }
    
    log_request("SEARCH", "/api/search", payload=sample_payload, headers=sample_headers)
    
    # Simulate processing time
    time.sleep(0.5)
    
    # Test response logging
    sample_response = {
        "results": [
            {
                "content": "Alice in Wonderland is a novel about a young girl who falls through a rabbit hole...",
                "score": 0.95,
                "source": "alice_in_wonderland.md"
            }
        ],
        "total_results": 1,
        "processing_time": 0.45
    }
    
    log_response("SEARCH", "200", response_data=sample_response, response_time=0.45)
    
    # Test database operation logging
    log_database_operation("QUERY", "chroma_db", 
                          data="SELECT * FROM documents WHERE content LIKE '%Alice%'",
                          result="Found 15 matching documents")
    
    # Test error logging
    try:
        # Simulate an error
        raise ValueError("Sample error for testing")
    except Exception as e:
        log_error("PROCESSING", str(e))
    
    logger.info("=== Logging Test Completed ===")

def test_chat_interaction():
    """Simulate a chat interaction with logging"""
    
    logger.info("=== Simulating Chat Interaction ===")
    
    # User sends a message
    user_message = "Tell me about the White Rabbit in Alice in Wonderland"
    log_request("CHAT", "/api/chat", payload={"message": user_message, "user_id": "user456"})
    
    # Process the message
    time.sleep(0.3)
    
    # System response
    system_response = {
        "response": "The White Rabbit is a key character in Alice in Wonderland. He is always in a hurry and carries a pocket watch...",
        "confidence": 0.92,
        "sources": ["alice_in_wonderland.md"],
        "tokens_used": 150
    }
    
    log_response("CHAT", "200", response_data=system_response, response_time=0.3)
    
    logger.info("=== Chat Interaction Completed ===")

if __name__ == "__main__":
    test_logging_functionality()
    test_chat_interaction() 