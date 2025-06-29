from loguru import logger
import sys
import os
from datetime import datetime

def setup_logger():
    """Setup loguru logger with different log files for different purposes"""
    
    # Remove default logger
    logger.remove()
    
    # Create logs directory if it doesn't exist
    os.makedirs("logs", exist_ok=True)
    
    # Console logger with colors
    logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level="INFO",
        colorize=True
    )
    
    # General application logs
    logger.add(
        "logs/app.log",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        level="DEBUG",
        rotation="10 MB",
        retention="30 days",
        compression="zip"
    )
    
    # Request logs
    logger.add(
        "logs/requests.log",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {message}",
        level="INFO",
        filter=lambda record: "REQUEST" in record["message"],
        rotation="10 MB",
        retention="30 days",
        compression="zip"
    )
    
    # Response logs
    logger.add(
        "logs/responses.log",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {message}",
        level="INFO",
        filter=lambda record: "RESPONSE" in record["message"],
        rotation="10 MB",
        retention="30 days",
        compression="zip"
    )
    
    # Payload logs
    logger.add(
        "logs/payloads.log",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {message}",
        level="DEBUG",
        filter=lambda record: "PAYLOAD" in record["message"],
        rotation="10 MB",
        retention="30 days",
        compression="zip"
    )
    
    # Error logs
    logger.add(
        "logs/errors.log",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        level="ERROR",
        rotation="10 MB",
        retention="30 days",
        compression="zip"
    )
    
    return logger

def log_request(request_type, endpoint, payload=None, headers=None):
    """Log request details"""
    logger.info(f"REQUEST | Type: {request_type} | Endpoint: {endpoint}")
    if payload:
        logger.debug(f"PAYLOAD | Request Payload: {payload}")
    if headers:
        logger.debug(f"PAYLOAD | Request Headers: {headers}")

def log_response(response_type, status_code, response_data=None, response_time=None):
    """Log response details"""
    logger.info(f"RESPONSE | Type: {response_type} | Status: {status_code}")
    if response_time:
        logger.info(f"RESPONSE | Response Time: {response_time:.2f}s")
    if response_data:
        logger.debug(f"PAYLOAD | Response Data: {response_data}")

def log_error(error_type, error_message, stack_trace=None):
    """Log error details"""
    logger.error(f"ERROR | Type: {error_type} | Message: {error_message}")
    if stack_trace:
        logger.error(f"ERROR | Stack Trace: {stack_trace}")

def log_database_operation(operation, table_name, data=None, result=None):
    """Log database operations"""
    logger.info(f"DB_OPERATION | Operation: {operation} | Table: {table_name}")
    if data:
        logger.debug(f"PAYLOAD | DB Data: {data}")
    if result:
        logger.debug(f"PAYLOAD | DB Result: {result}")

# Initialize logger
setup_logger() 