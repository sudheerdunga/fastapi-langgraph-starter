from collections.abc import Sequence
from langchain_core.tools import BaseTool


class ToolRegistry:
    """Central registry to manage and discover agent tools."""

    def __init__(self) -> None:
        self._tools: dict[str, BaseTool] = {}

    def register(self, tool: BaseTool) -> BaseTool:
        """Register a LangChain tool."""
        self._tools[tool.name] = tool
        return tool

    def get(self, name: str) -> BaseTool | None:
        """Get a single tool by name."""
        return self._tools.get(name)

    def get_tools(self, names: Sequence[str] | None = None) -> list[BaseTool]:
        """Get a list of tools by name.
        
        If names is None, returns all registered tools.
        """
        if names is None:
            return list(self._tools.values())
        return [self._tools[name] for name in names if name in self._tools]

    def list_available(self) -> list[dict[str, str]]:
        """Returns metadata of all registered tools."""
        return [
            {"name": tool.name, "description": tool.description}
            for tool in self._tools.values()
        ]


# Singleton instance
tool_registry = ToolRegistry()