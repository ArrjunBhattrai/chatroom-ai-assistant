from langchain.chains import LLMChain
from langchain_community.chat_models import ChatOllama
from langchain.prompts import PromptTemplate

llm = ChatOllama(model="llama3")

intent_prompt = PromptTemplate.from_template("""
The user asked: "{query}"

Identify what types of information they are requesting.
Valid options: summary, tasks, questions, decisions, deadlines, mentions.

Respond with a comma-separated list using only the above options.
Do not explain.
""")

intent_chain = LLMChain(llm=llm, prompt=intent_prompt)

def classify_intents(query: str) -> list[str]:
    try:
        raw = intent_chain.run({ "query": query })
        print("Intent Chain Output:", raw)
        return [intent.strip().lower() for intent in raw.split(",") if intent.strip()]
    except Exception as e:
        print("Intent classification failed:", e)
        return []
