from langchain.chains import LLMChain
from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate

llm = ChatOllama(model="llama3")

# Prompt to detect user mentions
prompt_template = ChatPromptTemplate.from_messages([
    ("system", "You're an AI that identifies if a specific user was mentioned in a conversation."),
    ("human", """
User **{username}** asked: {question}

Here is the relevant chat context:
{context}

Was **{username}** explicitly or implicitly mentioned in this discussion?
Return all relevant references as plain text bullet points. Avoid markdown and explanations.
""")
])

chain = LLMChain(llm=llm, prompt=prompt_template)

# Extract mention text cleanly
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

# Main function
def extract_mentions(question: str, context: str, username: str) -> dict:
    try:
        output = chain.invoke({
            "question": question,
            "context": context,
            "username": username
        })

        mentions = extract_mentions_text(output)

        if not mentions or len(mentions.strip()) < 5:
            raise ValueError("LLM did not return valid mentions.")

        return {"mentions": mentions}

    except Exception as e:
        print("Mentions extractor error:", e)
        return {"mentions": "Could not extract mentions."}
