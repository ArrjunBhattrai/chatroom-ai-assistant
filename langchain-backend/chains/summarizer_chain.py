from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from langchain_community.chat_models import ChatOllama
from models.chat import ChatPayload

llm = ChatOllama(model="llama3")

# 🧠 Prompt to get plain text summary
prompt_template = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant that summarizes conversations."),
    ("human", """
Here is the recent chat log:
{chat_log}

Summarize the conversation in 3-5 sentences.
Avoid markdown, bullet points, or formatting.
Return ONLY the plain summary text.
""")
])

chain = LLMChain(llm=llm, prompt=prompt_template)

def extract_summary(output) -> str:
    if isinstance(output, str):
        return output.strip()

    if isinstance(output, dict):
        if "summary" in output:
            return output["summary"].strip()
        if "text" in output:
            if isinstance(output["text"], str):
                return output["text"].strip()
            if isinstance(output["text"], dict):
                return output["text"].get("summary", "").strip()

    return "Summary could not be generated."

def summarize_chat(payload: ChatPayload) -> dict:
    chat_log = "\n".join(f"{msg.username}: {msg.content}" for msg in payload.messages)

    try:
        llm_output = chain.invoke({ "chat_log": chat_log })
        summary = extract_summary(llm_output)

        if not summary or len(summary) < 5:
            raise ValueError("LLM did not return a valid summary.")

        return { "summary": summary }

    except Exception as e:
        print("Summarizer error:", e)
        return { "summary": "Could not generate summary due to an error." }
