import json

MEMORY_FILE = "memory.json"

def load_memory():
    with open(MEMORY_FILE, "r") as f:
        return json.load(f)

def save_memory(memory):
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=4)

def store_preference(key, value):
    memory = load_memory()
    memory["preferences"][key] = value
    save_memory(memory)

def add_task(task, time):
    memory = load_memory()

    # Prevent duplicates
    for t in memory["tasks"]:
        if t["task"] == task:
            return

    memory["tasks"].append({
        "task": task,
        "time": time
    })

    save_memory(memory)


def add_conversation(text):
    memory = load_memory()
    memory["conversation_history"].append(text)
    save_memory(memory)

def get_preference(key):
    memory = load_memory()
    return memory["preferences"].get(key)

def get_tasks():
    memory = load_memory()
    return memory["tasks"]

def get_conversation_history():
    memory = load_memory()
    return memory["conversation_history"]   

