"""Configuration settings for the OpenFDA MCP Server."""

import os
from typing import Optional

class Config:
    """Application configuration."""
    
    # API Configuration
    FDA_BASE_URL = "https://api.fda.gov"
    REQUEST_TIMEOUT = 30.0
    MAX_RETRIES = 3
    
    # Rate Limiting
    MAX_REQUESTS_PER_MINUTE = 240  # FDA API limit
    
    # Server Configuration
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    # Validation
    MAX_SEARCH_LENGTH = 500
    MAX_LIMIT = 1000
    MIN_LIMIT = 1
    DEFAULT_LIMIT = 10

    @classmethod
    def validate(cls) -> bool:
        """Validate configuration."""
        return all([
            cls.FDA_BASE_URL,
            cls.REQUEST_TIMEOUT > 0,
            cls.MAX_RETRIES > 0
        ])