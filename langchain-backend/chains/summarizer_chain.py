from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from langchain_community.chat_models import ChatOllama
from models.chat import ChatPayload

llm = ChatOllama(model="llama3")

# Structured response fields
response_schemas = [
    ResponseSchema(name="summary", description="Short summary of the chat"),
    ResponseSchema(name="tasks", description="Action items or follow-ups"),
    ResponseSchema(name="questions", description="Any questions asked")
]

parser = StructuredOutputParser.from_response_schemas(response_schemas)

# Prompt
prompt_template = ChatPromptTemplate.from_messages([
    ("system", "You're an AI assistant helping summarize and track team conversations."),
    ("human", """
Here is the recent chat log:
{chat_log}

The user '{trigger_user}' asked: "{user_query}"

Please return:
1. A clear summary
2. A list of action items
3. Any questions asked

{format_instructions}
""")
])

# Final prompt with format instructions
prompt = prompt_template.partial(format_instructions=parser.get_format_instructions())

# Chain definition
chain = LLMChain(
    llm=llm,
    prompt=prompt,
    output_parser=parser
)

def summarize_chat(payload: ChatPayload) -> dict:
    chat_log = "\n".join(payload.messages)
    print("🧠 Building prompt for:", payload.triggerUser)

    response = chain.invoke({
        "chat_log": chat_log,
        "trigger_user": payload.triggerUser,
        "user_query": payload.userQuery
    })

    print("✅ Parsed Response:", response)
    return response
