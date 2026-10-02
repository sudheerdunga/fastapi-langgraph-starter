def test_health_check(client):
    """Verify health endpoint returns 200 OK."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_list_tools_endpoint(client):
    """Verify tool discovery endpoint exposes registered tools."""
    response = client.get("/api/v1/chat/tools")
    assert response.status_code == 200
    tools = response.json().get("tools", [])
    tool_names = [t["name"] for t in tools]
    assert "get_current_time" in tool_names
    assert "calculate" in tool_names


def test_chat_non_streaming(client, mock_llm):
    """Verify non-streaming chat POST endpoint."""
    payload = {
        "message": "Hello test!",
        "thread_id": "test-session-suite-1",
    }
    response = client.post("/api/v1/chat", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["thread_id"] == "test-session-suite-1"
    assert "Mock AI response for testing." in data["response"]


def test_chat_streaming(client, mock_llm):
    """Verify SSE streaming chat endpoint."""
    payload = {
        "message": "Stream this test",
        "thread_id": "test-session-suite-2",
    }
    response = client.post("/api/v1/chat/stream", json=payload)
    assert response.status_code == 200
    assert "event: token" in response.text
    assert "event: done" in response.text
