import spacy

nlp = spacy.load("en_core_web_sm")

def analyze_input(user_input):

    doc = nlp(user_input)

    entities = []
    time_entity = None

    for ent in doc.ents:
        entities.append((ent.text, ent.label_))
        if ent.label_ in ["TIME", "DATE"]:
            time_entity = ent.text

    intent = detect_intent(user_input)

    return {
        "intent": intent,
        "entities": entities,
        "time": time_entity,
        "confidence": 0.90
    }

def detect_intent(text):
    text = text.lower()

    if "prefer" in text:
        return "set_preference"
    if "remind" in text:
        return "set_reminder"
    if "schedule" in text:
        return "schedule_meeting"
    if "when" in text:
        return "retrieve_task"
    return "unknown"
