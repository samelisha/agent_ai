from typing import Any, Dict
from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from google.adk.runners import InMemoryRunner
from google.adk.tools import google_search
from google.genai import types

import asyncio
import warnings
warnings.filterwarnings('ignore')

# Agent configuration
agent_name = "eli_assistant"  # Agent name for printing replies
agent_description = "A simple agent that can answer general questions"
agent_model = "gemini-2.5-flash-lite"
agent_instruction = "You are a helpful assistant. Use Google Search for current info or if unsure."
agent_tools = [google_search]

# Create the agent and runner
root_agent = Agent(
    name=agent_name,
    model=Gemini(model=agent_model),
    description=agent_description,
    instruction=agent_instruction,
    tools=agent_tools
)
runner = InMemoryRunner(agent=root_agent, app_name="search_agent_app")
session_service = runner.session_service
USER_ID = "default_user"

async def chat():
    # Create a new session for the conversation
    session_id = "chat_session"
    await session_service.create_session(
        app_name=runner.app_name, user_id=USER_ID, session_id=session_id
    )
    
    # Chat loop
    while True:
        query = input("User > ")
        if query.lower() in ['exit', 'quit']:
            print("Exiting chat.")
            break

        # Format the user message for ADK
        content = types.Content(role="user", parts=[types.Part(text=query)])

        # Send the message to the agent and await response events
        async for event in runner.run_async(
            user_id=USER_ID, 
            session_id=session_id, 
            new_message=content
        ):
            # When final response is received, print and break
            if event.is_final_response() and event.content:
                text = event.content.parts[0].text.strip()
                print(f"{agent_name.capitalize()} > {text}")
                break

if __name__ == "__main__":
    asyncio.run(chat())

