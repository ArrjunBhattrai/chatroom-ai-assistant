from models.chat import ChatPayload
from services.message_service import save_query, save_response
from services.semantic_search import find_similar_messages
from chains.intent_classifier import classify_intents
from chains.summarizer_chain import summarize_chat
from chains.tasks_chain import extract_tasks
from chains.questions_chain import extract_questions
from chains.decisions_chain import extract_decisions
from chains.deadlines_chain import extract_deadlines
from chains.mentions_chain import extract_mentions
from datetime import datetime


def process_chat_intelligently(payload: ChatPayload) -> dict:
    print("Processing query:", payload.userQuery)

    query_text = payload.userQuery
    username = payload.triggerUser
    channel = payload.channel
    timestamp = str(datetime.utcnow())

    query_id = save_query(username=username, channel=channel, query_text=query_text, timestamp=timestamp)
    similar_docs = find_similar_messages(query_text, k=5)
    context = "\n".join([doc.page_content for doc in similar_docs])


    intents = classify_intents(payload.userQuery)
    print("Detected intents:", intents)

    result = {}

    input_data = {
    "question": query_text,
    "context": context,
    "username": username,        
    }
    if "summary" in intents:
        summary_result = summarize_chat(input_data)
        result["summary"] = summary_result.get("summary", "No summary found.")

    if "tasks" in intents:
        tasks_result = extract_tasks(input_data)
        result["tasks"] = tasks_result.get("tasks", "No tasks found.")

    if "questions" in intents:
        questions_result = extract_questions(input_data)
        result["questions"] = questions_result.get("questions", "No questions found.")

    if "decisions" in intents:
        decisions_result = extract_decisions(input_data)
        result["decisions"] = decisions_result.get("decisions", "No decisions found.")

    if "deadlines" in intents:
        deadlines_result = extract_deadlines(input_data)
        result["deadlines"] = deadlines_result.get("deadlines", "No deadlines found.")

    if "mentions" in intents:
        mentions_result = extract_mentions(input_data)
        result["mentions"] = mentions_result.get("mentions", "No mentions found.")

    if not result:
        result["message"] = "Sorry, I couldn't understand what you're asking for."

    return result
