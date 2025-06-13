"""Full system integration test."""

import pytest
import asyncio
from openfda_mcp_server.main import list_tools, call_tool

@pytest.mark.asyncio
async def test_complete_workflow():
    """Test the complete workflow from tool listing to execution."""
    # Test tool listing
    tools = await list_tools()
    assert len(tools) == 1
    tool = tools[0]
    assert tool.name == "search_device_classifications"
    
    # Test tool execution with various parameters
    test_cases = [
        {},  # No parameters
        {"limit": 5},  # Just limit
        {"search": "cardiac"},  # Just search
        {"search": "stethoscope", "limit": 3},  # Both parameters
    ]
    
    for test_case in test_cases:
        result = await call_tool("search_device_classifications", test_case)
        assert len(result) == 1
        assert result[0].type == "text"
        assert "FDA Device Classifications" in result[0].text
        
        # Ensure no obvious errors in the output
        assert "Error:" not in result[0].text or "No classifications found" in result[0].text

if __name__ == "__main__":
    pytest.main([__file__, "-v"])