import json
import os
from difflib import SequenceMatcher

# Get the directory where this script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MEMORY_FILE = os.path.join(SCRIPT_DIR, "memory.json")

def simple_similarity(a, b):
    """Calculate basic string similarity score"""
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

def semantic_search(query):
    try:
        with open(MEMORY_FILE, "r") as f:
            memory = json.load(f)
    except FileNotFoundError:
        return None

    history = memory.get("conversation_history", [])

    if not history:
        return None

    # Compute similarity scores using simple string matching
    scores = [simple_similarity(query, h) for h in history]

    best_index = max(range(len(scores)), key=lambda i: scores[i])
    best_score = scores[best_index]

    return {
        "match": history[best_index],
        "score": best_score
    }

    # Save memory
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=4)