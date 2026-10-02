from datetime import datetime, timezone
import math
from langchain_core.tools import tool
from app.tools.registry import tool_registry


@tool
def get_current_time(time_zone: str = "UTC") -> str:
    """Returns the current date and time.
    
    Use this tool whenever the user asks for the current time, today's date,
    or current day of the week.
    """
    now = datetime.now(timezone.utc)
    return f"Current date and time ({time_zone}): {now.strftime('%Y-%m-%d %H:%M:%S %Z')}"


@tool
def calculate(expression: str) -> str:
    """Evaluates a mathematical expression safely.
    
    Examples of valid input: '25 * 4', 'sqrt(144) + 10', '2 ** 8'.
    Use this tool whenever exact mathematical calculations are required.
    """
    # Safe namespace containing standard math functions
    allowed_names = {
        k: v for k, v in math.__dict__.items() if not k.startswith("__")
    }
    allowed_names.update({"abs": abs, "round": round})

    try:
        # Evaluate within restricted globals and no locals
        result = eval(expression, {"__builtins__": {}}, allowed_names)
        return f"Result: {result}"
    except Exception as e:
        return f"Error evaluating expression '{expression}': {e}"


# Auto-register built-in tools
tool_registry.register(get_current_time)
tool_registry.register(calculate)
