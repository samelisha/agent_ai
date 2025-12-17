import os
import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google.adk.errors.already_exists_error import AlreadyExistsError
from google.adk.agents import Agent
from google.adk.runners import InMemoryRunner
from google.adk.models.google_llm import Gemini
from google.genai import types

# ---------- FastAPI ----------
app = FastAPI(title="Elisha's Chat Agent")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for dev only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- Agent Setup ----------
agent = Agent(
    name="assistant",
    model=Gemini(
        model="gemini-2.5-flash-lite",
        api_key=os.environ.get("GOOGLE_API_KEY"),
    ),
    instruction="You are a helpful assistant."
)

runner = InMemoryRunner(agent=agent, app_name="chat_app")
session_service = runner.session_service

USER_ID = "web_user"

# ---------- Request / Response Models ----------
class ChatRequest(BaseModel):
    session_id: str
    message: str


class ChatResponse(BaseModel):
    response: str


# ---------- Startup ----------
@app.on_event("startup")
async def startup():
    print("FastAPI chat server started")


# ---------- Chat Endpoint ----------
@app.post("/chat")
async def chat(req: ChatRequest):

    try:
        await session_service.create_session(
            app_name=runner.app_name,
            user_id=USER_ID,
            session_id=req.session_id,
        )
    except AlreadyExistsError:
        pass

    content = types.Content(
        role="user",
        parts=[types.Part(text=req.message)]
    )

    async for event in runner.run_async(
        user_id=USER_ID,
        session_id=req.session_id,
        new_message=content
    ):
        if event.is_final_response():
            return {"response": event.content.parts[0].text}

