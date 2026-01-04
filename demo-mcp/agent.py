#!/usr/bin/env python3
"""
Example agent using the MCP SQLite Employee Database Server with LangChain
"""

import asyncio
import os
from pathlib import Path
from dotenv import load_dotenv
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_core.tools import Tool
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

load_dotenv()


async def create_mcp_tools(server_script_path: str):
    """Create LangChain tools from an MCP server"""

    server_params = StdioServerParameters(
        command="python3",
        args=[server_script_path]
    )

    tools = []

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # List available tools
            result = await session.list_tools()

            print(f"Loaded {len(result.tools)} tools from MCP server:")
            for mcp_tool in result.tools:
                print(f"  - {mcp_tool.name}: {mcp_tool.description}")
            print()

            for mcp_tool in result.tools:
                def create_tool_func(tool_name):
                    async def tool_func(**kwargs):
                        async with stdio_client(server_params) as (r, w):
                            async with ClientSession(r, w) as s:
                                await s.initialize()
                                result = await s.call_tool(tool_name, arguments=kwargs)
                                return result.content[0].text if result.content else ""
                    return tool_func

                langchain_tool = Tool(
                    name=mcp_tool.name,
                    description=mcp_tool.description or "",
                    func=lambda **kwargs: asyncio.run(create_tool_func(mcp_tool.name)(**kwargs)),
                    coroutine=create_tool_func(mcp_tool.name)
                )
                tools.append(langchain_tool)

    return tools


async def main():
    tools = await create_mcp_tools("/Users/trainer/demo-mcp/server_sqllite.py")

    llm = ChatOpenAI(model="gpt-4")
    agent = create_react_agent(llm, tools)

    queries = [
        "How many employees are in the Engineering department?"
    ]

    for query in queries:
        print(f"\nQuery: {query}")
        response = await agent.ainvoke({
            "messages": [("user", query)]
        })
        print(f"Response: {response['messages'][-1].content}")


if __name__ == "__main__":
    asyncio.run(main())
