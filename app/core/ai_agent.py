from langchain_groq import ChatGroq
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.prebuilt import create_react_agent
from langchain_core.messages.ai import AIMessage
from app.common import logger

log = logger.get_logger(__name__)

def get_response_from_ai_agent(llm_id, query, allow_search, system_prompt):
    try:
        llm = ChatGroq(model=llm_id)
        tools = [TavilySearchResults(max_result=2)] if allow_search else []
        agent = create_react_agent(model=llm, tools=tools, prompt=system_prompt)

        state = {"messages": query}
        response = agent.invoke(state)
        messages = response.get("messages", [])

        ai_messages = [m for m in messages if isinstance(m, AIMessage)]
        if not ai_messages:
            log.error(f"No AI messages returned by agent. Full response: {response}")
            return "AI agent did not return a response."

        return ai_messages[-1].content if ai_messages else "No response generated."  # Return the actual message text

    except Exception as e:
        log.exception(f"AI agent invocation failed: {str(e)}")
        return f"AI agent error: {str(e)}"
