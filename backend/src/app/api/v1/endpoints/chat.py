import json
from collections.abc import AsyncGenerator
from fastapi import APIRouter, HTTPException, status
from langchain_core.messages import HumanMessage
from sse_starlette.sse import EventSourceResponse

from app.api.v1.schemas.chat import ChatRequest, ChatResponse
from app.providers.llm_factory import LLMFactory
from app.tools import tool_registry
from app.workflows.checkpointer import get_checkpointer
from app.workflows.graphs.chat_graph import create_chat_graph

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.get("/tools")
async def list_tools():
    """Returns a list of all registered tools and their descriptions."""
    return {"tools": tool_registry.list_available()}


@router.post("", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest) -> ChatResponse:
    """Non-streaming conversational endpoint with tool support."""
    try:
        model = LLMFactory.get_model(
            provider=request.provider,
            model_name=request.model,
            temperature=request.temperature,
            streaming=False,
        )
        selected_tools = tool_registry.get_tools(request.tools)

        async with get_checkpointer() as checkpointer:
            graph = create_chat_graph(
                model=model,
                tools=selected_tools,
                checkpointer=checkpointer,
            )
            config = {"configurable": {"thread_id": request.thread_id}}

            result = await graph.ainvoke(
                {"messages": [HumanMessage(content=request.message)]},
                config=config,
            )

            last_message = result["messages"][-1]
            return ChatResponse(
                response=str(last_message.content),
                thread_id=request.thread_id,
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        ) from e


@router.post("/stream")
async def chat_stream_endpoint(request: ChatRequest) -> EventSourceResponse:
    """Server-Sent Events (SSE) streaming endpoint with live tool execution feedback."""

    async def event_generator() -> AsyncGenerator[dict, None]:
        try:
            model = LLMFactory.get_model(
                provider=request.provider,
                model_name=request.model,
                temperature=request.temperature,
                streaming=True,
            )
            selected_tools = tool_registry.get_tools(request.tools)

            async with get_checkpointer() as checkpointer:
                graph = create_chat_graph(
                    model=model,
                    tools=selected_tools,
                    checkpointer=checkpointer,
                )
                config = {"configurable": {"thread_id": request.thread_id}}

                async for event in graph.astream_events(
                    {"messages": [HumanMessage(content=request.message)]},
                    config=config,
                    version="v2",
                ):
                    kind = event.get("event")

                    # Stream LLM text tokens
                    if kind == "on_chat_model_stream":
                        chunk = event["data"].get("chunk")
                        if chunk and chunk.content:
                            yield {
                                "event": "token",
                                "data": json.dumps({"delta": chunk.content}),
                            }

                    # Stream tool start events (e.g. calculator starting)
                    elif kind == "on_tool_start":
                        yield {
                            "event": "tool_start",
                            "data": json.dumps({
                                "tool": event.get("name"),
                                "input": event.get("data", {}).get("input"),
                            }),
                        }

                    # Stream tool finish events with results
                    elif kind == "on_tool_end":
                        yield {
                            "event": "tool_end",
                            "data": json.dumps({
                                "tool": event.get("name"),
                                "output": str(event.get("data", {}).get("output")),
                            }),
                        }

            yield {"event": "done", "data": json.dumps({"status": "completed"})}
        except Exception as e:
            yield {"event": "error", "data": json.dumps({"error": str(e)})}

    return EventSourceResponse(event_generator())
