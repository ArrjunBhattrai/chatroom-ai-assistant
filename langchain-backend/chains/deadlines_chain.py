from langchain.chains import LLMChain
from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate

llm = ChatOllama(model="llama3")

# Prompt to extract deadlines
prompt_template = ChatPromptTemplate.from_messages([
    ("system", "You're an AI that extracts deadlines from chat-based team discussions."),
    ("human", """
User **{username}** asked: {question}

Relevant discussion context:
{context}

Extract all dates, deadlines, and timeline commitments.
Respond as plain text, no markdown or formatting.
""")
])

chain = LLMChain(llm=llm, prompt=prompt_template)

# Output cleaner — handles variations
def extract_deadline_text(output) -> str:
    if isinstance(output, str):
        return output.strip()

    if isinstance(output, dict):
        if "deadlines" in output:
            return output["deadlines"].strip()
        if "text" in output:
            if isinstance(output["text"], str):
                return output["text"].strip()
            if isinstance(output["text"], dict):
                return output["text"].get("deadlines", "").strip()

    return "Deadlines could not be extracted."

#  Main callable
def extract_deadlines(question: str, context: str, username: str) -> dict:
    try:
        output = chain.invoke({
            "question": question,
            "context": context,
            "username": username
        })

        deadlines = extract_deadline_text(output)

        if not deadlines or len(deadlines) < 5:
            raise ValueError("LLM did not return valid deadlines.")

        return { "deadlines": deadlines }

    except Exception as e:
        print("Deadline extractor error:", e)
        return { "deadlines": "Could not extract deadlines." }