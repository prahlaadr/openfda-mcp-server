"""Test error handling."""

import pytest
from openfda_mcp_server.main import call_tool

@pytest.mark.asyncio
async def test_invalid_limit_string():
    """Test handling of invalid limit values."""
    result = await call_tool("search_device_classifications", {"limit": "invalid"})
    assert "must be a valid integer" in result[0].text

@pytest.mark.asyncio
async def test_too_long_search_query():
    """Test handling of overly long search queries."""
    long_query = "x" * 501
    result = await call_tool("search_device_classifications", {"search": long_query})
    assert "too long" in result[0].text

@pytest.mark.asyncio
async def test_limit_boundaries():
    """Test limit boundary conditions."""
    # Test with limit 1 (minimum)
    result = await call_tool("search_device_classifications", {"limit": 1})
    assert "FDA Device Classifications" in result[0].text
    
    # Test with limit 1000 (maximum)
    result = await call_tool("search_device_classifications", {"limit": 1000})
    assert "FDA Device Classifications" in result[0].text

if __name__ == "__main__":
    pytest.main([__file__, "-v"])