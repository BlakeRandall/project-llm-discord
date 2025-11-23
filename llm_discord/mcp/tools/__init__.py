import logging
import inspect
from mcp.server.fastmcp import FastMCP

logger = logging.getLogger(__name__)


class AbstractTool:
    __tool_identifier_prefix__: str = "tool_"

    def __init__(self, mcp: FastMCP):
        for tool in [
            member
            for name, member in inspect.getmembers(
                self,
                lambda member: inspect.isroutine(member)
                and not inspect.isbuiltin(member),
            )
            if name.startswith(self.__tool_identifier_prefix__)
        ]:
            logger.info(f"Registering tool: {tool.__name__}")
            mcp.tool()(tool)
