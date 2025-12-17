from typing import Any, Dict
from google.adk.agents import Agent, LlmAgent, SequentialAgent, ParallelAgent
from google.adk.models.google_llm import Gemini
from google.adk.runners import InMemoryRunner, Runner
from google.adk.tools import google_search, AgentTool, FunctionTool
from google.genai import types
from google.adk.apps.app import App, EventsCompactionConfig
from google.adk.sessions import DatabaseSessionService, InMemorySessionService
from google.adk.tools.tool_context import ToolContext

import pandas as pd
import json
import matplotlib.pyplot as plt

import warnings
warnings.filterwarnings('ignore')

print("✅ ADK components imported successfully.")



retry_config=types.HttpRetryOptions(
    attempts=2,  # Maximum retry attempts
    exp_base=10,  # Delay multiplier
    initial_delay=10, # Initial delay before first retry (in seconds)
    http_status_codes=[500, 503, 504] # Retry on these HTTP errors
)

async def run_session(
    runner_instance: Runner,
    user_queries: list[str] | str = None,
    session_name: str = "default",
):
    print(f"\n ### Session: {session_name}")

    # Get app name from the Runner
    app_name = runner_instance.app_name

    # Attempt to create a new session or retrieve an existing one
    try:
        session = await session_service.create_session(
            app_name=app_name, user_id=USER_ID, session_id=session_name
        )
    except:
        session = await session_service.get_session(
            app_name=app_name, user_id=USER_ID, session_id=session_name
        )

    # Process queries if provided
    if user_queries:
        # Convert single query to list for uniform processing
        if type(user_queries) == str:
            user_queries = [user_queries]

        # Process each query in the list sequentially
        for query in user_queries:
            print(f"\nUser > {query}")

            # Convert the query string to the ADK Content format
            query = types.Content(role="user", parts=[types.Part(text=query)])

            # Stream the agent's response asynchronously
            async for event in runner_instance.run_async(
                user_id=USER_ID, session_id=session.id, new_message=query
            ):
                # Check if the event contains valid content
                if event.content and event.content.parts:
                    # Filter out empty or "None" responses before printing
                    if (
                        event.content.parts[0].text != "None"
                        and event.content.parts[0].text
                    ):
                        print(f"{MODEL_NAME} > ", event.content.parts[0].text)
    else:
        print("No queries!")


print("✅ Helper functions defined.")

agent_name = "my_search_assistant"
agent_description = "A simple agent that can answer my simple questions"
agent_model = "gemini-2.5-flash-lite"
agent_instruction = "You are a helpful assistant that answers my question within one line. Use Google Search for current info or if unsure."
agent_tools = [google_search]

print("✅ Main properties defined.")


root_agent = Agent(
    name=agent_name,
    model=Gemini(
        model=agent_model,
        retry_options=retry_config
    ),
    description=agent_description,
    instruction=agent_instruction,
    tools=agent_tools,
)
print("✅ Root Agent defined.")

runner = InMemoryRunner(agent=root_agent)
print("✅ Runner created.")
