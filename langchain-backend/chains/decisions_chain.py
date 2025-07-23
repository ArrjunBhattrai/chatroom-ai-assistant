from langchain.chains import LLMChain
from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from models.chat import ChatPayload

llm = ChatOllama(model="llama3")

# 🧠 Prompt to extract decisions
prompt_template = ChatPromptTemplate.from_messages([
    ("system", "You're an AI that extracts clear decisions made in a conversation."),
    ("human", """
Here is the chat log:
{chat_log}

Identify and list any decisions that were made during this discussion.
Return them as plain text bullet points. Do not include markdown or explanations.
""")
])

chain = LLMChain(llm=llm, prompt=prompt_template)

# ✅ Extract decision text from possibly nested LLM response
def extract_decision_text(output) -> str:
    if isinstance(output, str):
        return output.strip()

    if isinstance(output, dict):
        if "decisions" in output:
            return output["decisions"].strip()
        if "text" in output:
            if isinstance(output["text"], str):
                return output["text"].strip()
            if isinstance(output["text"], dict):
                return output["text"].get("decisions", "").strip()

    return "Decisions could not be extracted."

# 🚀 Main handler function
def extract_decisions(payload: ChatPayload) -> dict:
    chat_log = "\n".join(f"{m.username}: {m.content}" for m in payload.messages)

    try:
        output = chain.invoke({ "chat_log": chat_log })
        decisions = extract_decision_text(output)

        if not decisions or len(decisions.strip()) < 5:
            raise ValueError("LLM did not return valid decisions.")

        return { "decisions": decisions }

    except Exception as e:
        print("Decision extractor error:", e)
        return { "decisions": "Could not extract decisions." }
