from typing import Literal
from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(..., description="The user's input prompt or message")
    thread_id: str = Field(
        ...,
        description="Unique session/thread ID for conversation state persistence",
        examples=["session-abc-123"],
    )
    tools: list[str] | None = Field(
        default=None,
        description="Optional list of tool names to enable (e.g. ['calculate', 'get_current_time']). If omitted, all tools are enabled.",
    )
    provider: Literal["anthropic", "google", "ollama"] | None = Field(
        default=None,
        description="Override default LLM provider",
    )
    model: str | None = Field(
        default=None,
        description="Override default model name",
    )
    temperature: float | None = Field(
        default=None,
        ge=0.0,
        le=2.0,
        description="Override default temperature",
    )


class ChatResponse(BaseModel):
    response: str
    thread_id: str
