# OpenFDA MCP Server

[![Test](https://github.com/prahlaadr/openfda-mcp-server/actions/workflows/test.yml/badge.svg)](https://github.com/prahlaadr/openfda-mcp-server/actions/workflows/test.yml)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) server that provides access to FDA device classification data through the [OpenFDA API](https://open.fda.gov/).

## Features

- 🔍 Search FDA device classifications by name, class, or medical specialty
- ⚡ Fast, async API calls with proper error handling
- 📊 Configurable result limits (1-1000 results)
- 🛡️ Comprehensive input validation and sanitization
- 📝 Structured, readable output format
- 🔄 Automatic retry logic for network issues
- 📋 Extensive logging and monitoring

## Quick Start

### Installation

**Option 1: Direct Installation with pipx (Recommended)**
```bash
pipx install git+https://github.com/prahlaadr/openfda-mcp-server.git
```

**Option 2: Development Installation**
```bash
# Clone the repository
git clone https://github.com/prahlaadr/openfda-mcp-server.git
cd openfda-mcp-server

# Install in development mode
pip install -e .
```

### Running the Server

```bash
# Using the installed command
openfda-mcp-server

# Or directly with Python
python -m openfda_mcp_server.run_server
```

## Claude Desktop Configuration

To use with Claude Desktop, add this to your MCP configuration file:

**Location**: `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS)

```json
{
  "mcpServers": {
    "openfda": {
      "command": "/Users/yourusername/.local/pipx/venvs/openfda-mcp-server/bin/python",
      "args": ["-m", "openfda_mcp_server.run_server"],
      "env": {
        "LOG_LEVEL": "INFO"
      }
    }
  }
}
```

**Note**: Replace `/Users/yourusername/` with your actual home directory path.

### Alternative Configuration (Direct Command)
```json
{
  "mcpServers": {
    "openfda": {
      "command": "openfda-mcp-server",
      "env": {
        "LOG_LEVEL": "INFO"
      }
    }
  }
}
```

After configuration, restart Claude Desktop and you can ask questions like:
- "Search for cardiac medical devices"
- "Find Class II surgical instruments"
- "What are the FDA classifications for stethoscopes?"

## Available Tools

### search_device_classifications

Search FDA device classifications with flexible query options.

**Parameters:**
- `search` (optional): Search query string for device names, classifications, or medical specialties
- `limit` (optional): Number of results to return (1-1000, default: 10)

**Examples:**

```json
// Search for stethoscopes
{"search": "stethoscope", "limit": 5}

// Get latest 20 classifications
{"limit": 20}

// Search for cardiac devices
{"search": "cardiac"}
```

**Response Format:**

The tool returns formatted markdown with:
- Device name and classification
- Medical specialty
- Regulation number
- Product code
- Total results count

## Development

### Running Tests

```bash
# Run all tests
python -m pytest test_*.py -v

# Run specific test file
python -m pytest test_integration.py -v

# Run with coverage
python -m pytest test_*.py --cov=openfda_mcp_server
```

### Project Structure

```
openfda-mcp-server/
├── .github/workflows/       # CI/CD pipeline
├── openfda_mcp_server/      # Main package
│   ├── __init__.py
│   ├── config.py           # Configuration management
│   ├── main.py            # MCP server implementation
│   └── run_server.py      # Entry point
├── test_basic.py          # Core functionality tests
├── test_errors.py         # Error handling tests
├── test_integration.py    # API integration tests
├── requirements.txt       # Dependencies
├── setup.py              # Package setup
└── README.md             # This file
```

## API Information

This server uses the OpenFDA Device Classification API:
- **Endpoint**: https://api.fda.gov/device/classification.json
- **Documentation**: https://open.fda.gov/apis/device/classification/
- **Rate Limits**: 240 requests per minute (per IP)
- **Total Records**: 6,978+ device classifications available

## Error Handling

The server includes comprehensive error handling for:
- ❌ Network connectivity issues
- ⏱️ API rate limiting (with helpful retry messages)
- 🔍 Invalid search parameters
- 🚫 API server errors (500+ status codes)
- 📝 Malformed API responses
- 🔄 Automatic retry logic for transient failures

## Configuration

### Environment Variables

- `LOG_LEVEL`: Set logging verbosity (DEBUG, INFO, WARNING, ERROR)
  ```bash
  export LOG_LEVEL=DEBUG
  openfda-mcp-server
  ```

### Logs

The server creates logs in:
- **macOS**: `~/Library/Logs/openfda_mcp.log`
- **Console**: Real-time output via stderr

## Troubleshooting

### Claude Desktop Connection Issues

1. **Verify Installation**:
   ```bash
   which openfda-mcp-server
   openfda-mcp-server  # Should start without errors
   ```

2. **Check Configuration**:
   ```bash
   python3 -m json.tool "~/Library/Application Support/Claude/claude_desktop_config.json"
   ```

3. **View Logs**:
   ```bash
   tail -f ~/Library/Logs/openfda_mcp.log
   ```

4. **Restart Claude Desktop** after configuration changes

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup

```bash
# Install development dependencies
pip install -r requirements.txt

# Run tests before committing
python -m pytest test_*.py -v
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built for the [Model Context Protocol](https://modelcontextprotocol.io/)
- Powered by [OpenFDA API](https://open.fda.gov/)
- Inspired by the need for accessible FDA device data

## Support

- 🐛 [Report bugs](https://github.com/prahlaadr/openfda-mcp-server/issues)
- 💡 [Request features](https://github.com/prahlaadr/openfda-mcp-server/issues)
- 📖 [OpenFDA API Documentation](https://open.fda.gov/apis/)

---

Made with ❤️ for the MCP community