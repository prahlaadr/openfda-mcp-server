"""Basic tests for the MCP server structure."""

import pytest
from openfda_mcp_server.main import list_tools, call_tool

@pytest.mark.asyncio
async def test_list_tools():
    """Test that tools are listed correctly."""
    tools = await list_tools()
    assert len(tools) == 1
    assert tools[0].name == "search_device_classifications"
    assert "search" in tools[0].inputSchema["properties"]
    assert "limit" in tools[0].inputSchema["properties"]

@pytest.mark.asyncio
async def test_call_unknown_tool():
    """Test that unknown tools raise ValueError."""
    with pytest.raises(ValueError, match="Unknown tool"):
        await call_tool("unknown_tool", {})

if __name__ == "__main__":
    pytest.main([__file__, "-v"])