# FastAPI LangGraph Starter 🚀

A production-ready, async AI agent boilerplate built with **FastAPI**, **LangGraph**, and **uv**. Features multi-provider LLM support (Anthropic Claude, Google Gemini, Ollama), stateful multi-turn conversations with SQLite persistence, dynamic tool execution, and real-time Server-Sent Events (SSE) streaming.

---

## 🌟 Features

- **⚡ FastAPI & Uvicorn**: High-performance asynchronous API framework with automatic OpenAPI (`/docs`) and ReDoc (`/redoc`) documentation.
- **🦜🕸️ LangGraph Agent Workflows**: Cyclic graph-driven agent architecture (`StateGraph`) with built-in tool binding, tool routing (`ToolNode`), and conditional edges (`tools_condition`).
- **💾 Session Persistence**: SQLite-backed checkpointer (`AsyncSqliteSaver`) supporting conversational memory indexed by `thread_id`.
- **🔄 Real-Time SSE Streaming**: Native Server-Sent Events (`/api/v1/chat/stream`) emitting live tokens and tool execution lifecycle events:
  - `token`: Incremental LLM text generation deltas
  - `tool_start`: Tool execution starting events (name, arguments)
  - `tool_end`: Tool execution results and payloads
  - `done`: Final completion event
  - `error`: Error capture and propagation
- **🧠 Multi-Provider LLM Factory**: Dynamic switching between LLM providers:
  - **Anthropic**: Claude 3.5 Sonnet, Claude 3 Opus, Claude 3 Haiku
  - **Google**: Gemini 1.5 Pro, Gemini 1.5 Flash, Gemini 2.0 Flash
  - **Ollama**: Local models (`llama3`, `mistral`, `deepseek-r1`, `qwen2.5`, etc.)
- **🛠️ Extensible Tool Registry**: Centralized `ToolRegistry` with auto-discovery and per-request tool selection. Includes built-in tools for mathematical evaluation and timezone-aware datetime lookups.
- **🔭 Observability**: Built-in LangSmith tracing integration for debugging agent reasoning chains and monitoring token latency.
- **🚀 Modern Tooling**: Powered by [uv](https://docs.astral.sh/uv/) for fast dependency management, [ruff](https://docs.astral.sh/ruff/) for linting, and [pytest](https://pytest.org/) for async test suites.

---

## 📁 Project Structure

```text
backend/
├── src/
│   └── app/
│       ├── __init__.py           # Package entry point and CLI runner
│       ├── main.py               # FastAPI application factory & middleware
│       ├── api/
│       │   └── v1/
│       │       ├── endpoints/
│       │       │   └── chat.py   # Synchronous and SSE streaming chat routes
│       │       └── schemas/
│       │           └── chat.py   # Pydantic v2 validation models
│       ├── core/
│       │   └── config.py         # Type-safe settings via pydantic-settings
│       ├── providers/
│       │   └── llm_factory.py    # Multi-provider model instantiator
│       ├── tools/
│       │   ├── builtins.py       # Built-in tools (calculate, get_current_time)
│       │   └── registry.py       # Singleton tool registry
│       ├── workflows/
│       │   ├── checkpointer.py   # Async SQLite conversation checkpointer
│       │   ├── state.py          # LangGraph AgentState schema
│       │   └── graphs/
│       │       └── chat_graph.py # LangGraph workflow definition & compiler
│       └── tests/
│           ├── conftest.py       # Pytest fixtures and mock LLM test client
│           ├── test_api.py       # Integration tests for API endpoints
│           └── test_tools.py     # Unit tests for tool functionality
├── examples/
│   └── client/
│       └── stream.ts             # TypeScript SSE streaming consumption example
├── pyproject.toml                # Project metadata and dependencies
├── uv.lock                       # Deterministic dependency lockfile
└── .env.example                  # Environment configuration template
```

---

## 🛠️ Prerequisites

- **Python**: `>= 3.13`
- **uv**: Fast Python package manager ([Installation Guide](https://docs.astral.sh/uv/getting-started/installation/))
  ```bash
  # macOS / Linux
  curl -LsSf https://astral.sh/uv/install.sh | sh
  # Or via Homebrew
  brew install uv
  ```

---

## 🚀 Quick Start

### 1. Clone the repository
```bash
git clone <repo-url>
cd fastapi-langgraph-starter/backend
```

### 2. Configure Environment Variables
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
Edit `.env` and set your preferred provider keys:
```env
# Application Settings
APP_NAME="AI Application Boilerplate"
APP_ENV="development"
DEBUG=true
API_V1_PREFIX="/api/v1"
CORS_ORIGINS=["http://localhost:3000", "http://localhost:5173"]

# LLM Providers (anthropic | google | ollama)
DEFAULT_MODEL_PROVIDER="anthropic"
DEFAULT_MODEL_NAME="claude-3-5-sonnet-latest"
DEFAULT_TEMPERATURE=0.7

# Provider API Keys
ANTHROPIC_API_KEY="your-anthropic-api-key"
GOOGLE_API_KEY="your-google-api-key"
OLLAMA_BASE_URL="http://localhost:11434"

# Observability (Optional)
LANGSMITH_TRACING=false
LANGSMITH_API_KEY=""
LANGSMITH_PROJECT="fastapi-langgraph-boilerplate"

# Persistence
CHECKPOINT_DB_PATH="checkpoints.db"
```

### 3. Install Dependencies
Sync project dependencies using `uv`:
```bash
uv sync --all-groups
```

### 4. Run the Development Server
Start the server using either the pre-configured script command or Uvicorn directly:
```bash
# Using the project script
uv run app

# Or directly with uvicorn
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The application will be live at `http://localhost:8000`.

### 5. Access Interactive API Documentation
- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc UI**: [http://localhost:8000/redoc](http://localhost:8000/redoc)
- **Health Check**: [http://localhost:8000/health](http://localhost:8000/health)

---

## 📡 API Reference

### 1. Health Check
```http
GET /health
```
**Response:**
```json
{
  "status": "healthy",
  "app": "AI Application Boilerplate"
}
```

---

### 2. List Available Tools
Discover all tools registered in the agent's runtime.
```http
GET /api/v1/chat/tools
```
**Response:**
```json
{
  "tools": [
    {
      "name": "get_current_time",
      "description": "Returns the current date and time."
    },
    {
      "name": "calculate",
      "description": "Evaluates a mathematical expression safely."
    }
  ]
}
```

---

### 3. Synchronous Chat (`POST /api/v1/chat`)
Sends a message to the agent and waits for the full response.

**Request:**
```bash
curl -X POST "http://localhost:8000/api/v1/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What is 48 * 24 and what time is it in UTC?",
    "thread_id": "session-101"
  }'
```

**Payload Schema:**
| Field | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `message` | `string` | Yes | The user's input prompt. |
| `thread_id` | `string` | Yes | Unique session identifier for memory persistence. |
| `tools` | `string[]` | No | Optional tool filter (e.g. `["calculate"]`). If omitted, all registered tools are enabled. |
| `provider` | `string` | No | Override provider: `"anthropic"`, `"google"`, or `"ollama"`. |
| `model` | `string` | No | Override model name (e.g. `"claude-3-5-sonnet-latest"`). |
| `temperature` | `float` | No | Override sampling temperature (`0.0` - `2.0`). |

**Response:**
```json
{
  "response": "48 multiplied by 24 is 1,152. The current UTC time is 2026-10-02 06:15:00 UTC.",
  "thread_id": "session-101"
}
```

---

### 4. Streaming Chat with Server-Sent Events (`POST /api/v1/chat/stream`)
Streams incremental LLM tokens and live tool execution telemetry over an SSE connection.

**Request:**
```bash
curl -N -X POST "http://localhost:8000/api/v1/chat/stream" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Calculate sqrt(256) * 12",
    "thread_id": "session-102"
  }'
```

**SSE Event Types:**

1. **`tool_start`**: Fired when the agent invokes an external tool:
   ```text
   event: tool_start
   data: {"tool": "calculate", "input": {"expression": "sqrt(256) * 12"}}
   ```

2. **`tool_end`**: Fired when the tool execution yields an answer:
   ```text
   event: tool_end
   data: {"tool": "calculate", "output": "Result: 192.0"}
   ```

3. **`token`**: Fired for each incremental word or token emitted by the model:
   ```text
   event: token
   data: {"delta": "The"}

   event: token
   data: {"delta": " answer"}

   event: token
   data: {"delta": " is 192."}
   ```

4. **`done`**: Emitted once the full response and graph execution completes:
   ```text
   event: done
   data: {"status": "completed"}
   ```

---

## 💻 Frontend Client Integration

An example TypeScript client for consuming the SSE stream is provided in [`examples/client/stream.ts`](examples/client/stream.ts):

```typescript
async function streamChat({
  message,
  threadId,
  tools,
}: {
  message: string;
  threadId: string;
  tools?: string[];
}) {
  const response = await fetch("http://localhost:8000/api/v1/chat/stream", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message, thread_id: threadId, tools }),
  });

  const reader = response.body?.getReader();
  const decoder = new TextDecoder();

  while (true) {
    const { done, value } = await reader!.read();
    if (done) break;

    const chunk = decoder.decode(value);
    const lines = chunk.split("\n");

    let currentEvent = "";
    for (const line of lines) {
      if (line.startsWith("event: ")) {
        currentEvent = line.replace("event: ", "").trim();
      } else if (line.startsWith("data: ")) {
        const data = JSON.parse(line.replace("data: ", ""));

        if (currentEvent === "token") {
          process.stdout.write(data.delta); // Append token to UI
        } else if (currentEvent === "tool_start") {
          console.log(`\n⚙️ Executing tool: ${data.tool}...`);
        } else if (currentEvent === "tool_end") {
          console.log(`✅ Tool output: ${data.output}\n`);
        } else if (currentEvent === "done") {
          console.log("\n Stream complete.");
        }
      }
    }
  }
}
```

---

## 🧩 Adding Custom Tools

Tools are built using LangChain's `@tool` decorator and registered with `tool_registry`.

### Example: Define and Register a Tool
In `src/app/tools/builtins.py` (or your own tools module):

```python
from langchain_core.tools import tool
from app.tools.registry import tool_registry

@tool
def fetch_weather(city: str) -> str:
    """Returns the weather forecast for a specified city.
    
    Args:
        city: The name of the city (e.g. 'San Francisco', 'London').
    """
    # Integrate your weather API or logic here
    return f"The weather in {city} is 72°F (22°C) and sunny."

# Register tool to make it available to the agent
tool_registry.register(fetch_weather)
```

Once registered:
1. The tool will automatically appear in `GET /api/v1/chat/tools`.
2. The agent can invoke it autonomously when prompted.
3. Callers can enable or restrict it selectively via the `tools` array in requests.

---

## 🧪 Testing & Code Quality

### Running Tests
Execute the test suite with `pytest`:
```bash
uv run pytest
```

### Linting & Formatting
Check and format code using `ruff`:
```bash
# Lint checks
uv run ruff check .

# Automatic lint fix
uv run ruff check --fix .

# Code formatting
uv run ruff format .
```

---

## ⚙️ Configuration Reference

All settings can be configured via environment variables or a `.env` file (defined in `src/app/core/config.py`):

| Variable | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `APP_NAME` | `string` | `"AI Application Boilerplate"` | Application title displayed in docs |
| `APP_ENV` | `string` | `"development"` | Environment (`development`, `staging`, `production`) |
| `DEBUG` | `bool` | `true` | Enables FastAPI debug mode |
| `API_V1_PREFIX` | `string` | `"/api/v1"` | URL prefix for V1 endpoints |
| `CORS_ORIGINS` | `list[str]` | `["*"]` | Allowed CORS origins for frontend clients |
| `DEFAULT_MODEL_PROVIDER` | `string` | `"anthropic"` | Default LLM provider (`anthropic`, `google`, `ollama`) |
| `DEFAULT_MODEL_NAME` | `string` | `"claude-3-5-sonnet-latest"` | Default model name |
| `DEFAULT_TEMPERATURE` | `float` | `0.7` | Default model generation temperature |
| `ANTHROPIC_API_KEY` | `string` | `None` | Anthropic API key |
| `GOOGLE_API_KEY` | `string` | `None` | Google Generative AI API key |
| `OLLAMA_BASE_URL` | `string` | `"http://localhost:11434"` | Base URL for local Ollama instance |
| `CHECKPOINT_DB_PATH` | `string` | `"checkpoints.db"` | SQLite database path for session checkpoints |
| `LANGSMITH_TRACING` | `bool` | `false` | Enable LangSmith tracing |
| `LANGSMITH_API_KEY` | `string` | `None` | LangSmith API key |
| `LANGSMITH_PROJECT` | `string` | `"fastapi-langgraph-boilerplate"` | LangSmith project name |

---

## 📄 License

This project is licensed under the MIT License.
