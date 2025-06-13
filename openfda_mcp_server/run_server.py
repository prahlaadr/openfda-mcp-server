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
    logging.basicConfig(
        level=getattr(logging, Config.LOG_LEVEL.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('openfda_mcp.log')
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