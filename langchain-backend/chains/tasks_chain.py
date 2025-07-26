from langchain.chains import LLMChain
from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate

llm = ChatOllama(model="llama3")

# Prompt to extract tasks
prompt_template = ChatPromptTemplate.from_messages([
    ("system", "You are an assistant that identifies tasks assigned or discussed."),
    ("human", """
User **{username}** asked: {question}

Here is the related conversation context:
{context}

List all tasks, responsibilities, or action items mentioned in this discussion.
If none, return "No tasks found."

Output should be plain text bullet points or a comma-separated list.
Avoid markdown and extra formatting.
""")
])

chain = LLMChain(llm=llm, prompt=prompt_template)

# Handles different LLM outputs
def extract_tasks_from_output(output) -> str:
    if isinstance(output, str):
        return output.strip()

    if isinstance(output, dict):
        if "tasks" in output:
            return output["tasks"].strip()
        if "text" in output:
            if isinstance(output["text"], str):
                return output["text"].strip()
            if isinstance(output["text"], dict):
                return output["text"].get("tasks", "").strip()

    return "No tasks found."

# Entry point
def extract_tasks(question: str, context: str, username: str) -> dict:
    try:
        output = chain.invoke({
            "question": question,
            "context": context,
            "username": username
        })

        tasks = extract_tasks_from_output(output)

        if not tasks or len(tasks.strip()) < 5:
            raise ValueError("LLM did not return valid tasks.")

        return {"tasks": tasks}

    except Exception as e:
        print("Task extraction error:", e)
        return {"tasks": "Could not extract tasks."}
