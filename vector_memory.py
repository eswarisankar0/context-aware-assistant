from sentence_transformers import SentenceTransformer, util
import json
import torch

MEMORY_FILE = "memory.json"

# Load transformer model once
model = SentenceTransformer("all-MiniLM-L6-v2")

def semantic_search(query):
    with open(MEMORY_FILE, "r") as f:
        memory = json.load(f)

    history = memory["conversation_history"]

    if not history:
        return None

    # Encode query and history
    query_embedding = model.encode(query, convert_to_tensor=True)
    history_embeddings = model.encode(history, convert_to_tensor=True)

    # Compute cosine similarity
    scores = util.cos_sim(query_embedding, history_embeddings)

    best_index = torch.argmax(scores)
    best_score = scores[0][best_index].item()

    return {
        "match": history[best_index],
        "score": best_score
    }

    # Save memory
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=4)