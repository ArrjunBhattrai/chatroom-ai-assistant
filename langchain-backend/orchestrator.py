from models.chat import ChatPayload
from chains.intent_classifier import classify_intents
from chains.summarizer_chain import summarize_chat
from chains.tasks_chain import extract_tasks
from chains.questions_chain import extract_questions
from chains.decisions_chain import extract_decisions
from chains.deadlines_chain import extract_deadlines
from chains.mentions_chain import extract_mentions

def process_chat_intelligently(payload: ChatPayload) -> dict:
    print("🔍 Processing query:", payload.userQuery)

    intents = classify_intents(payload.userQuery)
    print("Detected intents:", intents)

    result = {}

    if "summary" in intents:
        summary_result = summarize_chat(payload)
        result["summary"] = summary_result.get("summary", "No summary found.")

    if "tasks" in intents:
        tasks_result = extract_tasks(payload)
        result["tasks"] = tasks_result.get("tasks", "No tasks found.")

    if "questions" in intents:
        questions_result = extract_questions(payload)
        result["questions"] = questions_result.get("questions", "No questions found.")

    if "decisions" in intents:
        decisions_result = extract_decisions(payload)
        result["decisions"] = decisions_result.get("decisions", "No decisions found.")

    if "deadlines" in intents:
        deadlines_result = extract_deadlines(payload)
        result["deadlines"] = deadlines_result.get("deadlines", "No deadlines found.")

    if "mentions" in intents:
        mentions_result = extract_mentions(payload)
        result["mentions"] = mentions_result.get("mentions", "No mentions found.")

    if not result:
        result["message"] = "Sorry, I couldn't understand what you're asking for."

    return result
