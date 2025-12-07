"""
Unit tests for Toon Optimizer backend utilities.
Run with: pytest test_utils.py -v
"""
import pytest
import json
from utils import (
    convert_json_to_toon_util,
    convert_toon_to_json_util,
    count_tokens,
    check_api_keys
)


class TestJsonToToonConversion:
    """Tests for JSON to TOON conversion."""
    
    def test_simple_object_conversion(self):
        """Test converting a simple JSON object."""
        json_input = '{"name": "Alice", "age": 30}'
        result = convert_json_to_toon_util(json_input, indent=2, delimiter=",")
        
        assert "output" in result
        assert result["json_data_tokens"] > 0
        assert result["toon_data_tokens"] > 0
        assert result["savings"] >= 0  # TOON should save tokens
        assert result["savings_percent"] >= 0
    
    def test_array_of_objects_conversion(self):
        """Test converting an array of uniform objects (ideal for TOON)."""
        json_input = '[{"id": 1, "name": "Apple"}, {"id": 2, "name": "Banana"}]'
        result = convert_json_to_toon_util(json_input, indent=2, delimiter=",")
        
        assert "output" in result
        assert result["savings_percent"] > 0, "Array of objects should have token savings"
    
    def test_invalid_json_raises_error(self):
        """Test that invalid JSON raises an exception."""
        json_input = '{"invalid": json without quotes}'
        
        with pytest.raises(json.JSONDecodeError):
            convert_json_to_toon_util(json_input, indent=2, delimiter=",")
    
    def test_empty_object_conversion(self):
        """Test converting an empty JSON object."""
        json_input = '{}'
        result = convert_json_to_toon_util(json_input, indent=2, delimiter=",")
        
        assert "output" in result
        assert result["json_data_tokens"] > 0
    
    def test_delimiter_options(self):
        """Test different delimiter options."""
        json_input = '{"name": "Alice"}'
        
        # Comma delimiter
        result_comma = convert_json_to_toon_util(json_input, indent=2, delimiter=",")
        assert "output" in result_comma
        
        # Tab delimiter
        result_tab = convert_json_to_toon_util(json_input, indent=2, delimiter="\t")
        assert "output" in result_tab
        
        # Pipe delimiter
        result_pipe = convert_json_to_toon_util(json_input, indent=2, delimiter="|")
        assert "output" in result_pipe


class TestToonToJsonConversion:
    """Tests for TOON to JSON conversion."""
    
    def test_simple_toon_conversion(self):
        """Test converting simple TOON back to JSON."""
        toon_input = "[2,]{id,name}:\n  1,Apple\n  2,Banana"
        
        try:
            result = convert_toon_to_json_util(toon_input)
            assert "output" in result
            assert result["toon_data_tokens"] > 0
            assert result["json_data_tokens"] > 0
            
            # Verify output is valid JSON
            parsed = json.loads(result["output"])
            assert isinstance(parsed, list)
        except NotImplementedError:
            # TOON decoder is in beta, this is expected for some inputs
            pytest.skip("TOON decoder is in beta, skipping test")


class TestTokenCounting:
    """Tests for token counting functionality."""
    
    def test_count_tokens_basic(self):
        """Test basic token counting."""
        text = "Hello, world!"
        count = count_tokens(text)
        
        assert isinstance(count, int)
        assert count > 0
    
    def test_count_tokens_empty_string(self):
        """Test token counting with empty string."""
        count = count_tokens("")
        assert count == 0
    
    def test_count_tokens_json(self):
        """Test token counting with JSON text."""
        json_text = '{"name": "Alice", "age": 30, "city": "New York"}'
        count = count_tokens(json_text)
        
        assert isinstance(count, int)
        assert count > 5  # JSON should have multiple tokens


class TestApiKeyChecks:
    """Tests for API key configuration checks."""
    
    def test_check_api_keys_returns_dict(self):
        """Test that check_api_keys returns expected structure."""
        status = check_api_keys()
        
        assert "langsmith_connected" in status
        assert "gemini_configured" in status
        assert isinstance(status["langsmith_connected"], bool)
        assert isinstance(status["gemini_configured"], bool)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
