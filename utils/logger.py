"""Logging utilities for AI Organization OS"""

import logging
import sys
from datetime import datetime
from pathlib import Path

# Create logs directory
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

# Configure logger
logger = logging.getLogger("ai_os")

# Check if logger has handlers to avoid adding duplicates
if not logger.handlers:
    logger.setLevel(logging.DEBUG)
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(console_format)
    logger.addHandler(console_handler)
    
    # File handler
    log_file = LOG_DIR / f"ai_os_{datetime.now().strftime('%Y%m%d')}.log"
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    file_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s'
    )
    file_handler.setFormatter(file_format)
    logger.addHandler(file_handler)

def get_logger(name):
    """Get a logger instance"""
    return logging.getLogger(f"ai_os.{name}")

def log_agent_start(agent_name, input_data):
    """Log agent execution start"""
    logger.info(f"Agent '{agent_name}' starting execution")
    logger.debug(f"Input: {str(input_data)[:200]}...")

def log_agent_complete(agent_name, output_length):
    """Log agent execution completion"""
    logger.info(f"Agent '{agent_name}' completed (output: {output_length} chars)")

def log_agent_error(agent_name, error):
    """Log agent execution error"""
    logger.error(f"Agent '{agent_name}' failed: {str(error)}")

def log_memory_operation(operation, memory_id):
    """Log memory operation"""
    logger.debug(f"Memory operation '{operation}': {memory_id}")

def log_rag_retrieval(query, results_count):
    """Log RAG retrieval"""
    logger.debug(f"RAG retrieval: query='{query[:50]}...', results={results_count}")
