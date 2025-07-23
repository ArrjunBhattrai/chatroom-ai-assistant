from langchain.chains import LLMChain
from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from models.chat import ChatPayload

llm = ChatOllama(model="llama3")

# 🧠 Prompt to extract user mentions
prompt_template = ChatPromptTemplate.from_messages([
    ("system", "You're an AI that identifies when a specific user is mentioned in a conversation."),
    ("human", """
Here is the chat log:
{chat_log}

Was the user '{trigger_user}' mentioned explicitly or indirectly in this discussion?
Return any mentions or references with short context, as plain text bullet points.
Do not include explanations or markdown.
""")
])

chain = LLMChain(llm=llm, prompt=prompt_template)

# ✅ Output extractor for mentions
def extract_mentions_text(output) -> str:
    if isinstance(output, str):
        return output.strip()

    if isinstance(output, dict):
        if "mentions" in output:
            return output["mentions"].strip()
        if "text" in output:
            if isinstance(output["text"], str):
                return output["text"].strip()
            if isinstance(output["text"], dict):
                return output["text"].get("mentions", "").strip()

    return "Mentions could not be extracted."

# 🚀 Main function to invoke the mentions chain
def extract_mentions(payload: ChatPayload) -> dict:
    chat_log = "\n".join(f"{m.username}: {m.content}" for m in payload.messages)

    try:
        output = chain.invoke({
            "chat_log": chat_log,
            "trigger_user": payload.triggerUser
        })

        mentions = extract_mentions_text(output)

        if not mentions or len(mentions.strip()) < 5:
            raise ValueError("LLM did not return valid mentions.")

        return {"mentions": mentions}

    except Exception as e:
        print("Mentions extractor error:", e)
        return {"mentions": "Could not extract mentions."}
