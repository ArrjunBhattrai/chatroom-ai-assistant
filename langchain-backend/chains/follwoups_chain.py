from langchain.chains import LLMChain
from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate

llm = ChatOllama(model="llama3")

# RAG-based prompt for follow-up suggestions
prompt_template = ChatPromptTemplate.from_messages([
    ("system", "You're an AI that suggests follow-up actions based on team discussions."),
    ("human", """
User **{username}** asked: {question}

Relevant discussion context:
{context}

Based on this, suggest actionable next steps or follow-up actions.
Return them as plain text bullet points only (no markdown, no explanations).
""")
])

chain = LLMChain(llm=llm, prompt=prompt_template)

# Output parser
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

# Main callable
def extract_followups(question: str, context: str, username: str) -> dict:
    try:
        output = chain.invoke({
            "question": question,
            "context": context,
            "username": username
        })

        followups = extract_followup_text(output)

        if not followups or len(followups.strip()) < 5:
            raise ValueError("LLM returned empty or invalid follow-up content.")

        return {"followups": followups}

    except Exception as e:
        print("Follow-up extractor error:", e)
        return {"followups": "Could not extract follow-ups."}
