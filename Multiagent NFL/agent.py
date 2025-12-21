from __future__ import annotations

import json
import os
import re
import ssl
import operator
from html.parser import HTMLParser
from typing import Any, Annotated, TypedDict
from urllib.parse import parse_qs, unquote, urlencode, urlparse
from urllib.request import Request, urlopen

from langchain_experimental.utilities import PythonREPL
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.graph import END, StateGraph
from langgraph.prebuilt.tool_node import ToolNode

from dotenv import load_dotenv
load_dotenv()

USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
DEFAULT_SEARCH_RESULTS = 5
DEFAULT_SCRAPE_CHARS = 3500
WEB_VERIFY_SSL = os.getenv("WEB_VERIFY_SSL", "true").lower() in {"1", "true", "yes", "y"}

MCP_BASE_URL = os.getenv("MCP_BASE_URL", "http://localhost:8000").rstrip("/")
MCP_TIMEOUT_SECONDS = float(os.getenv("MCP_TIMEOUT_SECONDS", "15"))
MCP_VERIFY_SSL = os.getenv("MCP_VERIFY_SSL", "false").lower() in {"1", "true", "yes", "y"}

class NflAgentState(TypedDict, total=False):
    messages: Annotated[list, operator.add]
    final_answer: str

class _DuckDuckGoParser(HTMLParser):
    def __init__(self, max_results: int) -> None:
        super().__init__()
        self.max_results = max_results
        self.results: list[dict[str, str]] = []
        self._capture = False
        self._current_href: str | None = None
        self._text_parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag != "a":
            return
        attr_map = dict(attrs)
        class_value = attr_map.get("class", "")
        if "result__a" not in class_value:
            return
        self._capture = True
        self._current_href = attr_map.get("href")
        self._text_parts = []

    def handle_data(self, data: str) -> None:
        if self._capture:
            self._text_parts.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag != "a" or not self._capture:
            return
        title = "".join(self._text_parts).strip()
        href = self._current_href or ""
        if title and href and len(self.results) < self.max_results:
            self.results.append({"title": title, "url": _clean_ddg_url(href)})
        self._capture = False
        self._current_href = None
        self._text_parts = []

def _clean_ddg_url(raw_url: str) -> str:
    parsed = urlparse(raw_url)
    if parsed.netloc.endswith("duckduckgo.com") and parsed.path == "/l/":
        qs = parse_qs(parsed.query)
        if "uddg" in qs and qs["uddg"]:
            return unquote(qs["uddg"][0])
    return raw_url



def _fetch_url(url: str, timeout: float) -> str:
    request = Request(url, headers={"User-Agent": USER_AGENT})
    context = None
    if url.startswith("https") and not WEB_VERIFY_SSL:
        context = ssl._create_unverified_context()
    with urlopen(request, timeout=timeout, context=context) as response:
        return response.read().decode("utf-8", errors="ignore")


@tool("web_search")
def web_search(query: str, max_results: int = DEFAULT_SEARCH_RESULTS) -> str:
    """
    Perform a lightweight web search using DuckDuckGo and return parsed results.

    This tool sends the query to DuckDuckGo's HTML endpoint, parses the
    search results page, and returns a JSON string containing the original
    query and a list of search results.

    Args:
        query (str): The search query to look up on the web.
        max_result (int): Maximum number of search results to return.
            Defaults to DEFAULT_SEARCH_RESULTS.

    Returns:
        str: A JSON-encoded string with the following structure:
            {
                "query": "<original query>",
                "results": [
                    {
                        "title": "<result title>",
                        "url": "<result URL>",
                        "snippet": "<short description>"
                    },
                    ...
                ]
            }

    Notes:
        - Uses DuckDuckGo's public HTML interface (no API key required).
        - Results are best-effort and may change if the page structure changes.
        - Intended for general information lookup, not guaranteed real-time accuracy.
    """
    encoded = urlencode({"q": query})
    url = f"https://duckduckgo.com/html/?{encoded}"
    html = _fetch_url(url, timeout=15)
    parser = _DuckDuckGoParser(max_results=max_results)
    parser.feed(html)
    payload = {"query": query, "results": parser.results}
    print(payload)
    return json.dumps(payload, ensure_ascii=True)

def build_agent() -> any:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required to run the NFL multi-agent graph.")
    
    model = ChatOpenAI(
        api_key=api_key,
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        temperature=0.2,
    )

    tools = [
        web_search,
    ]

    model_with_tools = model.bind_tools(tools)

    system_prompt = (
        "You are an NFL news analyst. Decide which tools to use (if any) to answer the user. "
        "Use web search for fresh NFL news, scrape only when you need details from a specific source, "
        "use MCP tools if they are relevant or available, and use Python only for calculations or "
        "lightweight analysis. Do not call tools unnecessarily. Summarize key events, then provide "
        "a short takeaways section and a Sources line with URLs."
    )

    def agent_node(state: NflAgentState) -> NflAgentState:
        messages = [SystemMessage(content=system_prompt)] + state.get("messages", [])
        response = model_with_tools.invoke(messages)
        return {"messages": [response]}
    
    def finalize(state: NflAgentState) -> NflAgentState:
        messages = state.get("messages") or []
        if messages and isinstance(messages[-1], AIMessage):
            return {"final_answer": messages[-1].content.strip()}
        return {"final_answer": ""}
    
    def should_continue(state: NflAgentState) -> str:
        messages = state.get("messages") or []
        if not messages:
            return "finalize"
        last = messages[-1]
        if isinstance(last, AIMessage) and last.tool_calls:
            return "tools"
        return "finalize"

    graph = StateGraph(NflAgentState)

    graph.add_node("agent", agent_node)
    graph.add_node("tools", ToolNode(tools))
    graph.add_node("finalize", finalize)    

    graph.set_entry_point("agent")
    graph.add_conditional_edges("agent", should_continue, {"tools": "tools", "finalize": "finalize"})
    graph.add_edge("tools", "agent")
    graph.add_edge("finalize", END)

    return graph.compile()

def answer_question(question: str) -> str:
    graph = build_agent()
    result = graph.invoke({"messages": [HumanMessage(content=question)]})
    return result.get("final_answer", "").strip()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="NFL multi-agent tool runner.")
    parser.add_argument(
        "question",
        nargs="?",
        default="What matches are played by PHILADELPHIA EAGLES in NFL this year",
        help="Question for the multi-agent system.",
    )
    args = parser.parse_args()
    print(answer_question(args.question))


