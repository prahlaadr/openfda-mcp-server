"""Test result formatting."""

import pytest
from openfda_mcp_server.main import format_classification_results

def test_format_empty_results():
    """Test formatting with no results."""
    data = {"results": [], "meta": {"results": {"total": 0}}}
    result = format_classification_results(data, "test", 10)
    assert "No classifications found" in result

def test_format_with_results():
    """Test formatting with sample results."""
    data = {
        "results": [
            {
                "device_name": "Test Device",
                "device_class": "Class II",
                "medical_specialty_description": "Cardiology",
                "regulation_number": "21 CFR 123.456",
                "product_code": "ABC"
            }
        ],
        "meta": {"results": {"total": 1}}
    }
    result = format_classification_results(data, "test", 10)
    assert "Test Device" in result
    assert "Class II" in result
    assert "Cardiology" in result

if __name__ == "__main__":
    pytest.main([__file__, "-v"])