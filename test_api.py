"""Test API connectivity."""

import pytest
import httpx
from openfda_mcp_server.main import CLASSIFICATION_ENDPOINT

@pytest.mark.asyncio
async def test_api_connectivity():
    """Test that we can reach the FDA API."""
    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(CLASSIFICATION_ENDPOINT, params={"limit": 1})
        assert response.status_code == 200
        data = response.json()
        assert "results" in data
        assert "meta" in data

if __name__ == "__main__":
    pytest.main([__file__, "-v"])