#!/usr/bin/env python3
"""Test that the MCP server can be started."""

import subprocess
import sys
import time

def test_server_startup():
    """Test that the server starts without immediate errors."""
    print("Testing OpenFDA MCP server startup...")
    
    # Start the server process
    process = subprocess.Popen(
        [sys.executable, "-m", "openfda_mcp_server.main"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # Give it a moment to start
    time.sleep(1)
    
    # Check if process is still running
    if process.poll() is None:
        print("✅ Server started successfully!")
        print("The server is now running and waiting for MCP client connections.")
        print("\nTo connect with an MCP client, the server expects JSON-RPC messages via stdin.")
        print("Example initialization message:")
        print('{"jsonrpc": "2.0", "method": "initialize", "params": {"protocolVersion": "2024-11-05", "capabilities": {}, "clientInfo": {"name": "test", "version": "1.0"}}, "id": 1}')
        
        # Terminate the test process
        process.terminate()
        assert True  # Test passed
    else:
        print("❌ Server failed to start")
        stdout, stderr = process.communicate()
        if stderr:
            print(f"Error: {stderr}")
        assert False, "Server failed to start"

if __name__ == "__main__":
    success = test_server_startup()
    sys.exit(0 if success else 1)