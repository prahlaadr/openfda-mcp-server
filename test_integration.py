"""Integration tests for the complete MCP server."""

import pytest
from openfda_mcp_server.main import call_tool

@pytest.mark.asyncio
async def test_search_without_query():
    """Test searching without a search query."""
    result = await call_tool("search_device_classifications", {"limit": 5})
    assert len(result) == 1
    assert "FDA Device Classifications" in result[0].text

@pytest.mark.asyncio
async def test_search_with_query():
    """Test searching with a specific query."""
    result = await call_tool("search_device_classifications", {
        "search": "stethoscope",
        "limit": 3
    })
    assert len(result) == 1
    content = result[0].text
    assert "FDA Device Classifications" in content
    assert "stethoscope" in content.lower() or "Search Query: stethoscope" in content

@pytest.mark.asyncio
async def test_limit_validation():
    """Test that limits are properly validated."""
    # Test upper limit
    result = await call_tool("search_device_classifications", {"limit": 2000})
    assert len(result) == 1
    # Should not error, limit should be capped
    
    # Test lower limit
    result = await call_tool("search_device_classifications", {"limit": 0})
    assert len(result) == 1
    # Should not error, limit should be set to 1

if __name__ == "__main__":
    pytest.main([__file__, "-v"])