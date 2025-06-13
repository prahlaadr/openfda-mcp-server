#!/usr/bin/env python3
"""
Entry point for the OpenFDA MCP Server.
"""

import sys
import logging
from pathlib import Path

from .main import main as server_main
from .config import Config

def setup_logging():
    """Set up logging configuration."""
    # Use a writable directory for log files
    import os
    log_dir = os.path.expanduser('~/Library/Logs')
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, 'openfda_mcp.log')
    
    logging.basicConfig(
        level=getattr(logging, Config.LOG_LEVEL.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stderr),  # Use stderr for MCP compatibility
            logging.FileHandler(log_file)
        ]
    )

def main():
    """Main entry point for the OpenFDA MCP Server."""
    setup_logging()
    logger = logging.getLogger("openfda-mcp")
    logger.info("Starting OpenFDA MCP Server")
    
    try:
        server_main()
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Server crashed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()