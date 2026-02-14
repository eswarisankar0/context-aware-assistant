from memory_system import store_preference, add_task, add_conversation

def execute(action_data, user_input):

    add_conversation(user_input)

    action = action_data["action"]

    if action == "store_preference":
        store_preference(action_data["key"], action_data["value"])
        print("Assistant: Preference saved.")

    elif action == "schedule_with_preference":
        print(f"Assistant: Meeting scheduled based on your preference: {action_data['time']}")

    elif action == "schedule_default":
        print("Assistant: Meeting scheduled at default time.")

    elif action == "store_task":
       add_task(action_data["task"], action_data["time"])
       print(f"Assistant: Task saved for {action_data['time']}")


    elif action == "semantic_recall":
        context = action_data["context"]
        if context:
            print(f"Assistant: I remember you said: {context['match']}")
            print(f"Relevance Score: {context['score']:.2f}")
        else:
            print("Assistant: No relevant memory found.")

    elif action == "clarify":
        print("Assistant: Could you clarify your request?")

    else:
        print("Assistant: I didn’t understand that.")
