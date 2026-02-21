from typing import Dict, Any, Callable, List
from dataclasses import dataclass

@dataclass
class Tool:
    name: str
    description: str
    func: Callable
    schema: Dict[str, Any]

class MCPServer:
    """
    Acts as the Model Context Protocol (MCP) Server.
    It registers tools and executes them based on names.
    """
    def __init__(self):
        self.tools: Dict[str, Tool] = {}

    def register_tool(self, tool: Tool):
        self.tools[tool.name] = tool
        print(f"[MCP] Registered tool: {tool.name}")

    def list_tools(self) -> List[Dict[str, Any]]:
        return [
            {
                "name": t.name,
                "description": t.description,
                "schema": t.schema
            }
            for t in self.tools.values()
        ]

    def call_tool(self, name: str, arguments: Dict[str, Any]) -> Any:
        if name not in self.tools:
            raise ValueError(f"Tool '{name}' not found.")
        
        print(f"[MCP] Executing tool '{name}' with args: {arguments}")
        try:
            return self.tools[name].func(**arguments)
        except Exception as e:
            print(f"[MCP] Error executing '{name}': {e}")
            raise e
