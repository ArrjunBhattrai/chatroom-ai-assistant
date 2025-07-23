from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from langchain_community.chat_models import ChatOllama
from models.chat import ChatPayload

llm = ChatOllama(model="llama3")

# 🧠 Prompt to extract tasks from chat
prompt_template = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant that extracts tasks assigned in a conversation."),
    ("human", """
Here is the recent chat log:
{chat_log}

List all tasks or action items mentioned in this conversation.
If none, say "No tasks found."
Return them as a plain list of bullet points or a comma-separated string.
Avoid markdown formatting.
""")
])

chain = LLMChain(llm=llm, prompt=prompt_template)

def extract_tasks_from_output(output) -> str:
    if isinstance(output, str):
        return output.strip()

    if isinstance(output, dict):
        if "tasks" in output:
            return output["tasks"].strip()
        if "text" in output:
            if isinstance(output["text"], str):
                return output["text"].strip()
            if isinstance(output["text"], dict):
                return output["text"].get("tasks", "").strip()

    return "No tasks found."

def extract_tasks(payload: ChatPayload) -> dict:
    chat_log = "\n".join(f"{msg.username}: {msg.content}" for msg in payload.messages)

    try:
        llm_output = chain.invoke({ "chat_log": chat_log })
        tasks = extract_tasks_from_output(llm_output)

        if not tasks:
            raise ValueError("LLM did not return any tasks.")

        return { "tasks": tasks }

    except Exception as e:
        print("Task extraction error:", e)
        return { "tasks": "Could not extract tasks due to an error." }
