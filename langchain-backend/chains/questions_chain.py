from langchain.chains import LLMChain
from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate

llm = ChatOllama(model="llama3")

# Prompt to extract questions aimed at a user
prompt_template = ChatPromptTemplate.from_messages([
    ("system", "You're an assistant that extracts questions directed at a specific user."),
    ("human", """
User **{username}** asked: {question}

Here is the relevant discussion context:
{context}

Identify all questions that were directly or indirectly asked to **{username}**.
A question is valid if:
- It uses @username or mentions them
- It's clearly aimed at them based on context

Return only the exact question texts. Avoid metadata, markdown, or formatting.
If none found, return "No questions found."
""")
])

chain = LLMChain(llm=llm, prompt=prompt_template)

# Extractor for questions
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

# Entry point
def extract_questions(question: str, context: str, username: str) -> dict:
    try:
        output = chain.invoke({
            "question": question,
            "context": context,
            "username": username
        })

        questions = extract_questions_from_output(output)

        if not questions or len(questions.strip()) < 5:
            raise ValueError("LLM did not return valid questions.")

        return {"questions": questions}

    except Exception as e:
        print("Question extraction error:", e)
        return {"questions": "Could not extract questions."}
