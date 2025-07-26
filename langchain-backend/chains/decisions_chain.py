from langchain.chains import LLMChain
from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate

llm = ChatOllama(model="llama3")

# Prompt updated for RAG context
prompt_template = ChatPromptTemplate.from_messages([
    ("system", "You are an AI that extracts important decisions made during team discussions."),
    ("human", """
User **{username}** asked: {question}

Relevant discussion context:
{context}

Identify all clear decisions made during this discussion.
Return them as plain text bullet points, no markdown or explanation.
""")
])

chain = LLMChain(llm=llm, prompt=prompt_template)

# Output cleaner
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

# Main handler
def extract_decisions(question: str, context: str, username: str) -> dict:
    try:
        output = chain.invoke({
            "question": question,
            "context": context,
            "username": username
        })

        decisions = extract_decision_text(output)

        if not decisions or len(decisions.strip()) < 5:
            raise ValueError("LLM did not return valid decisions.")

        return { "decisions": decisions }

    except Exception as e:
        print("Decision extractor error:", e)
        return { "decisions": "Could not extract decisions." }
