# FastAPI LangGraph Starter 🚀

A modern, production-grade template for building stateful AI agents using **FastAPI**, **LangGraph**, and **uv**.

## 🌟 Key Highlights

- **FastAPI Backend**: Async, high-performance web service with automated OpenAPI Swagger UI.
- **LangGraph Agent Workflow**: Dynamic cyclic graph workflows with conditional tool routing and SQLite session checkpointer persistence (`thread_id`).
- **Multi-LLM Provider Support**: Out-of-the-box support for Anthropic Claude, Google Gemini, and local Ollama models.
- **Real-Time Streaming**: Server-Sent Events (SSE) emitting token streams and tool lifecycle events (`tool_start`, `tool_end`).
- **Tool Registry**: Dynamic tool discovery, registration, and per-request tool filtering.
- **Modern Python Tooling**: Fast dependency resolution with `uv`, code linting with `ruff`, and testing with `pytest`.

## 📂 Quick Links

- [Backend Documentation & Setup Guide](file:///Users/sudheerdunga/Desktop/Development/Training/python-ai/fastapi-langgraph-starter/backend/README.md)
- [Client Integration Example (TypeScript)](file:///Users/sudheerdunga/Desktop/Development/Training/python-ai/fastapi-langgraph-starter/backend/examples/client/stream.ts)

## 🚀 Getting Started

Navigate to the `backend` folder and get started:

```bash
cd backend
cp .env.example .env
uv sync --all-groups
uv run app
```

Visit the interactive Swagger API documentation at: [http://localhost:8000/docs](http://localhost:8000/docs).
