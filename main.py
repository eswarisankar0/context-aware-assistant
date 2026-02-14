from nlp_engine import analyze_input
from reasoning_engine import reason
from action_engine import execute

def run():
    print("NIXIN AI - Layer 1 Context Engine Running\n")

    while True:
        user_input = input("You: ")

        if user_input.lower() == "exit":
            break

        intent_data = analyze_input(user_input)

        # 🔥 PROFESSIONAL OUTPUT BLOCK
        print("\n===== CONTEXTUAL RESPONSE =====")
        print("Intent:", intent_data["intent"])
        print("Confidence:", intent_data["confidence"])
        print("Entities:", intent_data["entities"])
        print("================================\n")

        action_data = reason(intent_data, user_input)

        execute(action_data, user_input)

if __name__ == "__main__":
    run()

    print("\nNIXIN AI - Layer 1 Context Engine Stopped")