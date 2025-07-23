from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from langchain_community.chat_models import ChatOllama
from models.chat import ChatPayload

llm = ChatOllama(model="llama3")

# 🧠 Prompt to extract questions asked to the user
prompt_template = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant that extracts questions asked to a specific user in a conversation."),
    ("human", """
Here is the recent chat log:
{chat_log}

The user you're assisting is: {trigger_user}

Identify all questions that were directly or indirectly asked to this user.
A question is valid if:
- It directly mentions the user with @tag
- It includes their username in the sentence
- Or it's clearly aimed at them in context

Only return the actual question texts (not usernames or metadata).
If there are no such questions, say "No questions found."
Avoid markdown or formatting.
""")
])

chain = LLMChain(llm=llm, prompt=prompt_template)

def extract_questions_from_output(output) -> str:
    if isinstance(output, str):
        return output.strip()

    if isinstance(output, dict):
        if "questions" in output:
            return output["questions"].strip()
        if "text" in output:
            if isinstance(output["text"], str):
                return output["text"].strip()
            if isinstance(output["text"], dict):
                return output["text"].get("questions", "").strip()

    return "No questions found."

def extract_questions(payload: ChatPayload) -> dict:
    chat_log = "\n".join(f"{msg.username}: {msg.content}" for msg in payload.messages)

    try:
        llm_output = chain.invoke({
            "chat_log": chat_log,
            "trigger_user": payload.triggerUser
        })

        questions = extract_questions_from_output(llm_output)

        if not questions:
            raise ValueError("LLM did not return any questions.")

        return { "questions": questions }

    except Exception as e:
        print("Question extraction error:", e)
        return { "questions": "Could not extract questions due to an error." }
