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

    query_id = save_query(
        username=username,
        channel=channel,
        query_text=query_text,
        timestamp=timestamp
    )

    intents = classify_intents(query_text)
    print("Detected intents:", intents)

    result = {}

    if "summary" in intents:
        docs = find_similar_messages(f"summary: {query_text}", k=30)
        context = "\n".join(doc.page_content for doc in docs)

        summary_result = summarize_chat(
            question=query_text,
            context=context
        )

        result["summary"] = summary_result.get("summary", "No summary found.")

    if "tasks" in intents:
        docs = find_similar_messages(f"tasks: {query_text}", k=10)
        context = "\n".join(doc.page_content for doc in docs)
        tasks_result = extract_tasks(
            question=query_text,
            context=context,
            username=username
        )
        result["tasks"] = tasks_result.get("tasks", "No tasks found.")

    if "questions" in intents:
        docs = find_similar_messages(f"questions: {query_text}", k=10)
        context = "\n".join(doc.page_content for doc in docs)
        questions_result = extract_questions(
            question=query_text,
            context=context,
            username=username
        )
        result["questions"] = questions_result.get("questions", "No questions found.")

    if "decisions" in intents:
        docs = find_similar_messages(f"decisions: {query_text}", k=10)
        context = "\n".join(doc.page_content for doc in docs)
        decisions_result = extract_decisions(
            question=query_text,
            context=context,
            username=username
        )
        result["decisions"] = decisions_result.get("decisions", "No decisions found.")

    if "deadlines" in intents:
        docs = find_similar_messages(f"deadlines: {query_text}", k=10)
        context = "\n".join(doc.page_content for doc in docs)
        deadlines_result = extract_deadlines(
            question=query_text,
            context=context,
            username=username
        )
        result["deadlines"] = deadlines_result.get("deadlines", "No deadlines found.")

    if "mentions" in intents:
        docs = find_similar_messages(f"mentions: {query_text}", k=10)
        context = "\n".join(doc.page_content for doc in docs)
        mentions_result = extract_mentions(
            question=query_text,
            context=context,
            username=username
        )
        result["mentions"] = mentions_result.get("mentions", "No mentions found.")

    # Save the response
    if result:
        full_text = "\n\n".join([f"{k.upper()}:\n{v}" for k, v in result.items()])
        save_response(query_id=query_id, response_text=full_text, timestamp=timestamp)
    else:
        result["message"] = "Sorry, I couldn't understand what you're asking for."

    return result
