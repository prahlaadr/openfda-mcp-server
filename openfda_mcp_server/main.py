"""
OpenFDA MCP Server - Device Classification Endpoint
A Model Context Protocol server for querying FDA device classifications.
"""

import asyncio
import logging
from typing import Any, Sequence

import httpx
from mcp.server import Server, InitializationOptions
from mcp.types import (
    Resource,
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
    LoggingLevel
)
from .config import Config

# Validate configuration on startup
if not Config.validate():
    raise RuntimeError("Invalid configuration")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("openfda-mcp")

# Create the MCP server instance
app = Server("openfda-classification")

# Use configuration
FDA_BASE_URL = Config.FDA_BASE_URL
CLASSIFICATION_ENDPOINT = f"{FDA_BASE_URL}/device/classification.json"

@app.list_tools()
async def list_tools() -> list[Tool]:
    """Return the list of tools available in this server."""
    return [
        Tool(
            name="search_device_classifications",
            description="Search FDA device classifications by device name, class, or medical specialty",
            inputSchema={
                "type": "object",
                "properties": {
                    "search": {
                        "type": "string",
                        "description": "Search query (device name, class, specialty, etc.)"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Number of results to return (max 1000)",
                        "minimum": 1,
                        "maximum": 1000,
                        "default": 10
                    }
                },
                "required": []
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool calls."""
    if name == "search_device_classifications":
        return await search_device_classifications(arguments)
    else:
        raise ValueError(f"Unknown tool: {name}")

async def search_device_classifications(arguments: dict) -> list[TextContent]:
    """Search device classifications using the OpenFDA API."""
    try:
        # Extract and validate arguments
        search_query = arguments.get("search", "").strip()
        limit = arguments.get("limit", Config.DEFAULT_LIMIT)
        
        # Validate and sanitize inputs
        if isinstance(limit, str):
            try:
                limit = int(limit)
            except ValueError:
                return [TextContent(
                    type="text",
                    text="Error: 'limit' must be a valid integer"
                )]
        
        if limit > Config.MAX_LIMIT:
            limit = Config.MAX_LIMIT
        elif limit < Config.MIN_LIMIT:
            limit = Config.MIN_LIMIT
        
        # Build query parameters
        params = {"limit": limit}
        if search_query:
            # Basic input sanitization
            if len(search_query) > Config.MAX_SEARCH_LENGTH:
                return [TextContent(
                    type="text",
                    text=f"Error: Search query too long (max {Config.MAX_SEARCH_LENGTH} characters)"
                )]
            params["search"] = search_query
        
        logger.info(f"Searching classifications with params: {params}")
        
        # Make API request with retry logic
        max_retries = Config.MAX_RETRIES
        for attempt in range(max_retries):
            try:
                async with httpx.AsyncClient(timeout=Config.REQUEST_TIMEOUT) as client:
                    response = await client.get(CLASSIFICATION_ENDPOINT, params=params)
                    response.raise_for_status()
                    break
            except httpx.TimeoutException:
                if attempt == max_retries - 1:
                    raise
                await asyncio.sleep(1)  # Brief delay before retry
                
        data = response.json()
        
        # Validate response structure
        if not isinstance(data, dict) or "results" not in data:
            return [TextContent(
                type="text",
                text="Error: Unexpected response format from FDA API"
            )]
        
        # Format and return results
        return [TextContent(
            type="text",
            text=format_classification_results(data, search_query, limit)
        )]
        
    except httpx.HTTPStatusError as e:
        error_msg = f"FDA API returned an error (HTTP {e.response.status_code})"
        if e.response.status_code == 404:
            error_msg += ": Endpoint not found"
        elif e.response.status_code == 429:
            error_msg += ": Rate limit exceeded. Please try again later."
        elif e.response.status_code >= 500:
            error_msg += ": FDA API server error. Please try again later."
        
        logger.error(f"HTTP error: {e}")
        return [TextContent(type="text", text=error_msg)]
        
    except httpx.TimeoutException:
        logger.error("Request timeout")
        return [TextContent(
            type="text",
            text="Request timeout: FDA API is taking too long to respond. Please try again."
        )]
        
    except httpx.RequestError as e:
        logger.error(f"Request error: {e}")
        return [TextContent(
            type="text",
            text="Network error: Unable to connect to FDA API. Please check your internet connection."
        )]
        
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return [TextContent(
            type="text",
            text=f"An unexpected error occurred. Please try again. If the problem persists, contact support."
        )]

def format_classification_results(data: dict, search_query: str, limit: int) -> str:
    """Format the API response into readable text."""
    results = data.get("results", [])
    meta = data.get("meta", {})
    
    # Build header
    header_parts = ["# FDA Device Classifications"]
    
    if search_query:
        header_parts.append(f"**Search Query:** {search_query}")
    
    total_results = meta.get("results", {}).get("total", len(results))
    header_parts.append(f"**Results:** Showing {len(results)} of {total_results} total")
    
    header = "\n".join(header_parts) + "\n\n"
    
    # Handle empty results
    if not results:
        return header + "No classifications found matching your search criteria."
    
    # Format each result
    formatted_results = []
    for i, result in enumerate(results, 1):
        device_name = result.get("device_name", "N/A")
        device_class = result.get("device_class", "N/A")
        medical_specialty = result.get("medical_specialty_description", "N/A")
        regulation_number = result.get("regulation_number", "N/A")
        product_code = result.get("product_code", "N/A")
        
        formatted_result = f"""## {i}. {device_name}
- **Device Class:** {device_class}
- **Medical Specialty:** {medical_specialty}
- **Regulation Number:** {regulation_number}
- **Product Code:** {product_code}"""
        
        formatted_results.append(formatted_result)
    
    return header + "\n\n".join(formatted_results)

async def run():
    """Run the MCP server."""
    import mcp.server.stdio
    
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="openfda-classification",
                server_version="0.1.0",
                capabilities={}
            )
        )

def main():
    """Entry point for the MCP server."""
    import asyncio
    asyncio.run(run())

if __name__ == "__main__":
    main()
