from typing import Annotated
from typing_extensions import TypedDict
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages


class AgentState(TypedDict):
    """Core state for the conversation graph.
    
    Attributes:
        messages: List of conversation messages. Using add_messages allows
                  automatic appending and updating by ID.
    """
    messages: Annotated[list[BaseMessage], add_messages]
