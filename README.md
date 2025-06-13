# OpenFDA MCP Server - Device Classifications

A Model Context Protocol (MCP) server that provides access to FDA device classification data.

## Features

- Search FDA device classifications by name, class, or medical specialty
- Configurable result limits (1-1000 results)
- Comprehensive error handling
- Structured, readable output

## Installation

1. Clone this repository
2. Create virtual environment: `python -m venv venv`
3. Activate environment: `source venv/bin/activate` (Linux/Mac) or `venv\Scripts\activate` (Windows)
4. Install dependencies: `pip install -r requirements.txt`

## Usage

### Running the Server
```bash
python main.py
```

## Available Tools

### search_device_classifications
Search FDA device classifications.

**Parameters:**
- `search` (optional): Search query string
- `limit` (optional): Number of results to return (1-1000, default: 10)

**Examples:**
```json
{"search": "stethoscope", "limit": 5}
{"limit": 20}
{"search": "cardiac"}
```

## Testing

Run all tests:
```bash
python -m pytest test_*.py -v
```

## API Information

This server uses the OpenFDA Device Classification API:
- Endpoint: https://api.fda.gov/device/classification.json
- Documentation: https://open.fda.gov/apis/device/classification/

## Error Handling

The server handles various error conditions:
- Network connectivity issues
- API rate limiting
- Invalid parameters
- API server errors
- Malformed responses

## Logging

The server logs important events and errors. Set log level via environment:
```bash
export LOG_LEVEL=DEBUG
python main.py
```
