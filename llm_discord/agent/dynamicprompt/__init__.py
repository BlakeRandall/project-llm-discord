from typing import Any, cast
from langchain.agents.middleware import dynamic_prompt, ModelRequest
from langgraph.runtime import Runtime
from discord import User


@dynamic_prompt
def dynamic_system_prompt(request: ModelRequest) -> str:
    runtime: Runtime = cast(Runtime, request.runtime)
    state: dict[str, Any] | None = cast(dict[str, Any] | None, request.state)
    context: dict[str, Any] | None = cast(dict[str, Any] | None, runtime.context)

    prompt = request.system_prompt or ""

    if not context:
        return prompt

    author: User | None = context.get("author", None)
    if not author:
        return prompt

    prompt += f"""
    User information:
        UID: {author.id}
        Display name: {author.display_name}
        Global name: {author.global_name}
        Nick name: {author.name}
        CreatedAt: {author.created_at}
    When responding to the user reference the user information, to keep it simple use Display name, unless the user asks about the other types of names."""
    return prompt
