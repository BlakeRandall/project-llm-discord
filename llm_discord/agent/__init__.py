import logging
from typing import Any
from langchain.agents.factory import create_agent
from langchain.agents.middleware.types import AgentState
from langchain.agents.middleware.summarization import SummarizationMiddleware
from langchain.agents.middleware.model_call_limit import ModelCallLimitMiddleware
from langchain.agents.middleware.tool_call_limit import ToolCallLimitMiddleware
from langchain.agents.middleware.tool_retry import ToolRetryMiddleware
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.cache.memory import InMemoryCache
from langgraph.store.memory import InMemoryStore
from langgraph.graph.state import CompiledStateGraph
from llm_discord.agent.dynamicprompt import dynamic_system_prompt
from llm_discord.config.app import AppConfig
from llm_discord.config.chatmodel import ChatModelConfig
from llm_discord.config.mcp import MCPConfig
from llm_discord.model.singleton import SingletonMeta

logger = logging.getLogger(__name__)

app_config = AppConfig()
chatmodel_config = ChatModelConfig()
mcp_config = MCPConfig()


class AgentFacade(object, metaclass=SingletonMeta):
    @classmethod
    async def agent(cls) -> CompiledStateGraph[Any, Any, Any, Any]:
        cls_instance = cls()
        return await cls_instance.__agent()

    __agent_instance: CompiledStateGraph[Any, Any, Any, Any] | None = None

    async def __agent(self) -> CompiledStateGraph[Any, Any, Any, Any]:
        if self.__agent_instance is None:
            self.__agent_instance = create_agent(
                model=chatmodel_config.chat_model,
                tools=await mcp_config.tools(),
                middleware=[
                    dynamic_system_prompt,
                    SummarizationMiddleware(
                        model=chatmodel_config.chat_model,
                        max_tokens_before_summary=2**11,
                        messages_to_keep=50,
                    ),
                    ModelCallLimitMiddleware(
                        run_limit=3,
                        exit_behavior="end",
                    ),  # type: ignore
                    ToolCallLimitMiddleware(run_limit=3, exit_behavior="end"),  # type: ignore
                    ToolRetryMiddleware(),
                ],
                checkpointer=InMemorySaver(),
                cache=InMemoryCache(),
                # store=InMemoryStore(),
                system_prompt="""You are a useful assistant.""",
                state_schema=AgentState,
                context_schema=dict,
                name="custom_agent",
            )
        return self.__agent_instance
