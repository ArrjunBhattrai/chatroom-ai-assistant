from langchain.chains import LLMChain
from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from models.chat import ChatPayload

llm = ChatOllama(model="llama3")

# 🧠 Prompt for follow-up suggestions
prompt_template = ChatPromptTemplate.from_messages([
    ("system", "You're an AI that suggests follow-up actions based on team discussions."),
    ("human", """
Here is the chat log:
{chat_log}

Based on this discussion, suggest next steps or follow-up actions.

Return the follow-ups as plain text bullet points. Do not include explanations or markdown formatting.
""")
])

chain = LLMChain(llm=llm, prompt=prompt_template)

# 🧪 Output extractor (handles different output types)
def extract_followup_text(output) -> str:
    if isinstance(output, str):
        return output.strip()

    if isinstance(output, dict):
        if "followups" in output:
            return output["followups"].strip()
        if "text" in output:
            if isinstance(output["text"], str):
                return output["text"].strip()
            if isinstance(output["text"], dict):
                return output["text"].get("followups", "").strip()

    return "Could not extract follow-up actions."

# 🚀 Main entry point for chain
def extract_followups(payload: ChatPayload) -> dict:
    chat_log = "\n".join(f"{m.username}: {m.content}" for m in payload.messages)

    try:
        output = chain.invoke({"chat_log": chat_log})
        followups = extract_followup_text(output)

        if not followups or len(followups.strip()) < 5:
            raise ValueError("LLM returned empty or invalid follow-up content.")

        return {"followups": followups}

    except Exception as e:
        print("Follow-up extractor error:", e)
        return {"followups": "Could not extract follow-ups."}
