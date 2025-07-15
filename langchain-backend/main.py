from fastapi import FastAPI, Request
from pydantic import BaseModel
from langchain_community.chat_models import ChatOllama
from langchain.schema.messages import HumanMessage

app = FastAPI()

class Payload(BaseModel):
    userQuery: str
    triggerUser: str
    messages: list[str]

@app.post("/process")
async def process_chat(payload: Payload):
    history = "\n".join(payload.messages)

    prompt = f"""This is the chat log:\n{history}\n\n
    The user '{payload.triggerUser}' asked: "{payload.userQuery}".\n
    Provide a relevant summary, follow-up, or answer as appropriate.
    """

    llm = ChatOllama(model="llama3")
    response = llm.invoke([HumanMessage(content=prompt)])
    return {"summary": response.content}
