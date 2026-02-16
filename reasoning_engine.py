from memory_system import store_preference, add_task, get_preference
from vector_memory import semantic_search

CONFIDENCE_THRESHOLD = 0.75

def reason(intent_data, user_input):

    if intent_data["confidence"] < CONFIDENCE_THRESHOLD:
        return {"action": "clarify"}

    intent = intent_data["intent"]

    if intent == "set_preference":
        return {
            "action": "store_preference",
            "key": "meeting_time",
            "value": user_input
        }

    if intent == "schedule_meeting":
        pref = get_preference("meeting_time")
        if pref:
            return {
                "action": "schedule_with_preference",
                "time": pref
            }
        else:
            return {"action": "schedule_default"}

    if intent == "set_reminder":
        return {
            "action": "store_task",
            "task": user_input,
            "time": intent_data["time"] if intent_data["time"] else "No time detected",
            "person": intent_data["person"] if intent_data["person"] else None
        }


    if intent == "retrieve_task":
        context = semantic_search(user_input)
        return {
            "action": "semantic_recall",
            "context": context
        }

    if intent == "create_task":
        return {
            "action": "store_task",
            "task": user_input,
            "time": intent_data["time"] if intent_data["time"] else "No time detected",
            "person": intent_data["person"] if intent_data["person"] else None
        }

    return {"action": "unknown"}
