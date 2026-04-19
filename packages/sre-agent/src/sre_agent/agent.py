"""
ReAct SRE Agent.

Implements a ReAct (Reasoning and Acting) agent that autonomously diagnoses
Kubernetes incidents by combining runbook knowledge (via the search_runbooks
tool) with its own domain expertise.

The agent reasons step-by-step: it decides when to consult the runbooks,
interprets the retrieved context, and produces a structured Markdown
diagnostic report.

Usage:
    python -m sre_agent.agent "high cpu usage in production pods"
"""

import sys

from langchain.agents import create_agent
from langchain_core.messages import ToolMessage
from langchain_openai import ChatOpenAI

from sre_agent.config import (
    NO_CONTEXT_SENTINEL,
    OPENAI_CHAT_MODEL,
    load_project_env,
)
from sre_agent.query import search_runbooks

SYSTEM_PROMPT = """\
You are an expert Kubernetes Site Reliability Engineer (SRE) agent.

Your mission is to diagnose incidents and produce a detailed analysis report.

## Tools
You have access to a `search_runbooks` tool that queries the organization's SRE
runbook knowledge base. You SHOULD use it to look for documented procedures
relevant to the reported problem. You may call it multiple times with different
queries if the first search does not return useful results.

## Response Format
- Format your entire response in **Markdown**.
- Structure your analysis with these sections: **Overview**, **Diagnosis**,
  **Resolution Steps**, and **Prevention**.
- When information comes from a runbook, **cite the source** explicitly
  (file path and heading/section).

## Guidelines
- Be concise and actionable.
- Prioritize information from the runbooks over your own knowledge.
"""

_WARNING_BLOCK = (
    "> [!WARNING]\n"
    "> No internal runbook covers this issue. "
    "The following analysis is based entirely on general SRE and domain knowledge.\n\n"
)


def create_sre_agent():
    """Create and return the SRE ReAct agent."""
    load_project_env()
    llm = ChatOpenAI(model=OPENAI_CHAT_MODEL, temperature=0)

    return create_agent(
        model=llm,
        tools=[search_runbooks],
        system_prompt=SYSTEM_PROMPT,
    )


def _runbooks_were_found(messages: list) -> bool:
    """
    Inspect the agent's message history to determine whether any
    search_runbooks tool call returned actual runbook content.

    Returns True if at least one ToolMessage contains content other
    than the sentinel string, False if all searches came up empty.
    """
    tool_results = [
        msg.content
        for msg in messages
        if isinstance(msg, ToolMessage)
    ]
    if not tool_results:
        return False
    return any(result != NO_CONTEXT_SENTINEL for result in tool_results)


def diagnose(query: str) -> str:
    """
    Run the SRE agent to diagnose an incident.

    Args:
        query: A natural-language description of the problem, error log line,
               or alert message.

    Returns:
        A Markdown-formatted diagnostic report, with a warning block prepended
        if no relevant runbook content was found during the agent's tool calls.
    """
    agent = create_sre_agent()
    response = agent.invoke(
        {"messages": [{"role": "user", "content": query}]}
    )

    messages = response["messages"]
    report = messages[-1].content

    if not _runbooks_were_found(messages):
        report = _WARNING_BLOCK + report

    return report


def main() -> None:
    """Run the CLI diagnosis entrypoint."""
    if len(sys.argv) <= 1:
        print(
            'Error: No query provided. Usage: python -m sre_agent.agent "your query"'
        )
        sys.exit(1)

    query = " ".join(sys.argv[1:])
    print(f"Query: {query}\n")
    print(diagnose(query))


if __name__ == "__main__":
    main()
