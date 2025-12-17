# agent_ai
Gemini Chat Agent (FastAPI + HTML UI)
A simple chat application built using FastAPI, Google ADK (Gemini), and a lightweight HTML frontend.
It exposes a REST API for chat and a browser-based chat UI.

✨ Features
Chat-style conversation with Gemini
Session-based memory
REST API (/chat)
Simple HTML frontend (no build tools)
CORS-enabled for browser usage
Easy local setup

🧱 Architecture
Browser (HTML UI)
        |
        v
 FastAPI Backend
        |
        v
 Google ADK Runner
        |
        v
 Gemini LLM
 
📦 Prerequisites
Python 3.10+
Google Gemini API Key
Internet connection

🔑 Environment Setup
1️⃣ Set Google API Key
macOS / Linux
export GOOGLE_API_KEY="your_api_key_here"
Windows (PowerShell)
setx GOOGLE_API_KEY "your_api_key_here"
Restart your terminal after setting the key.

📥 Install Dependencies
pip install fastapi uvicorn google-adk google-genai

🚀 Run the Backend (FastAPI)
uvicorn app:app --reload
Server will start at:
http://127.0.0.1:8000
📘 API Documentation (Swagger)
Open in browser:
http://127.0.0.1:8000/docs
🧠 Chat API Usage
Endpoint
POST /chat
Request Body
{
  "session_id": "my-session-1",
  "message": "Hello!"
}
Response
{
  "response": "Hello! How can I help you today?"
}

Notes
Reuse the same session_id to maintain chat memory
New session_id → new conversation
Sessions are stored in memory (restart clears them)

🌐 Frontend (HTML Chat UI)
1️⃣ Open the HTML File
Simply open index.html in your browser:
open index.html
(or double-click the file)
2️⃣ What It Does
Sends messages to /chat
Displays responses in chat format
Uses a fixed session ID by default
You can modify this line in index.html:
const sessionId = "web-session-1";

❌ Missing API Key Error
ValueError: Missing key inputs argument
Fix: Ensure GOOGLE_API_KEY is set correctly.
