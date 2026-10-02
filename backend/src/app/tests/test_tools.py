from app.tools import calculate, get_current_time, tool_registry


def test_tool_registry():
    """Verify tools are registered in singleton."""
    tools = tool_registry.list_available()
    names = [t["name"] for t in tools]
    assert "get_current_time" in names
    assert "calculate" in names


def test_calculate_tool():
    """Verify calculator tool handles mathematical expressions safely."""
    result = calculate.invoke({"expression": "25 * 4"})
    assert result == "Result: 100"

    # Test error handling
    invalid_result = calculate.invoke({"expression": "1 / 0"})
    assert "Error" in invalid_result


def test_get_current_time_tool():
    """Verify time tool returns a formatted date-time string."""
    result = get_current_time.invoke({"time_zone": "UTC"})
    assert "Current date and time" in result
    assert "UTC" in result
