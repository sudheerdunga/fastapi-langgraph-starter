from collections.abc import Sequence
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.tools import BaseTool
from langgraph.checkpoint.base import BaseCheckpointSaver
from langgraph.graph import END, START, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition

from app.providers.llm_factory import LLMFactory
from app.workflows.state import AgentState


def create_chat_graph(
    model: BaseChatModel | None = None,
    tools: Sequence[BaseTool] | None = None,
    checkpointer: BaseCheckpointSaver | None = None,
):
    """Creates a compiled LangGraph workflow.
    
    Args:
        model: Optional pre-configured chat model. If None, uses default LLMFactory model.
        tools: Optional list of tools to bind to the model.
        checkpointer: Optional checkpointer for persisting multi-turn conversations.
    """
    llm = model or LLMFactory.get_model()
    tools_list = list(tools or [])

    if tools_list:
        llm_with_tools = llm.bind_tools(tools_list)
    else:
        llm_with_tools = llm

    # 1. Define nodes
    async def call_model(state: AgentState) -> dict:
        response = await llm_with_tools.ainvoke(state["messages"])
        return {"messages": [response]}

    # 2. Build graph structure
    workflow = StateGraph(AgentState)
    workflow.add_node("agent", call_model)
    workflow.add_edge(START, "agent")

    if tools_list:
        workflow.add_node("tools", ToolNode(tools_list))
        # Conditional edge: route to tools if tool_calls requested, otherwise END
        workflow.add_conditional_edges("agent", tools_condition)
        workflow.add_edge("tools", "agent")
    else:
        workflow.add_edge("agent", END)

    # 3. Compile graph with checkpointer
    return workflow.compile(checkpointer=checkpointer)