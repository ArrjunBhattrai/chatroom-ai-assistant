# 🧠 Discord AI Assistant

An intelligent assistant for Discord that listens to conversations, summarizes discussions, extracts tasks/questions, and identifies follow-ups — helping teams stay aligned and productive in real-time.

---

## 🚀 Features

- 🔍 **Summarization**: Understands and summarizes recent conversations in a channel.
- ✅ **Task Extraction**: Identifies action items from messages.
- ❓ **Question Detection**: Captures unanswered or important questions.
- 📌 **Follow-Up Tracking**: Flags pending items or points that need attention.
- 🧠 **Intent Classifier**: Automatically determines user query type (e.g., "summarize", "follow-ups", etc.)
- 💬 **Multi-user & Multi-channel Support**: Handles multiple servers, users, and channels concurrently.
- 🧾 **Message Logging**: Stores all messages and assistant interactions in PostgreSQL.
- 🔎 **Semantic Memory Search**: Integrates ChromaDB to retrieve relevant past queries and responses using embeddings.

---

## 🛠️ Tech Stack

| Layer         | Tools Used                                               |
|---------------|----------------------------------------------------------|
| **Bot**       | Discord.js (or Discord.py if Python version)            |
| **Workflow**  | [n8n](https://n8n.io) (event-driven orchestration)       |
| **LLM**       | LangChain (running locally on FastAPI) + Ollama/Gemini  |
| **Database**  | PostgreSQL + ChromaDB (for vector search)               |
| **Embeddings**| `text-embedding-ada-002` (or local model)               |
| **Frontend**  | None (CLI / Discord interface only)                     |

---