"""
PRACTICAL TEST CASES - Context Aware Assistant
Real-world scenarios to validate the system end-to-end
Run: python3 practical_test_cases.py
"""

from nlp_engine import analyze_input
from reasoning_engine import reason
from action_engine import execute
import json

# Color codes for output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

test_scenarios = [
    # ==================== REMINDERS ====================
    {
        "category": "REMINDER",
        "inputs": [
            "remind me to pay the electric bill on 20 feb 2026",
            "alert me about the doctor's appointment at 2 pm",
            "remind alice to call kavita mam tomorrow",
            "set a reminder for the team meeting at 10 am monday",
            "remind me to buy groceries after work",
        ]
    },
    
    # ==================== SCHEDULING ====================
    {
        "category": "SCHEDULING",
        "inputs": [
            "schedule meeting tomorrow with alice",
            "book an appointment with dr. smith on friday at 3 pm",
            "schedule a call with john sir next monday",
            "arrange a meeting for 17 feb 2026 with kavita",
            "set up a conference call tomorrow",
        ]
    },
    
    # ==================== PREFERENCES ====================
    {
        "category": "PREFERENCE",
        "inputs": [
            "set preference for morning time",
            "I prefer meetings in the afternoon",
            "prefer to work from home on fridays",
            "set my timezone to IST",
            "i like quiet hours from 9 to 5",
        ]
    },
    
    # ==================== TASKS ====================
    {
        "category": "TASK",
        "inputs": [
            "send an email to alice with the project report",
            "submit the assignment by friday",
            "call the client before 5 pm today",
            "prepare the presentation for john sir",
            "finish the project and send to kavita mam by 17 feb",
        ]
    },
    
    # ==================== MEMORY RECALL ====================
    {
        "category": "MEMORY_RECALL",
        "inputs": [
            "what have I told you about the project",
            "did I mention anything about the meeting",
            "what did I say about alice earlier",
            "do you remember my preferences",
            "recall our discussion from yesterday",
        ]
    },
    
    # ==================== COMPLEX SCENARIOS ====================
    {
        "category": "COMPLEX",
        "inputs": [
            "remind me to submit undertaking form to kavita mam on 17 feb 2026 at 9 am",
            "schedule a meeting with alice tomorrow and send her an email with the agenda",
            "after you schedule the meeting, remind me to prepare the slides for dr. smith",
            "set preference for morning meetings and remind me about the meeting with john sir tomorrow",
            "send email to alice and call john sir by 5 pm today",
        ]
    },
    
    # ==================== EDGE CASES ====================
    {
        "category": "EDGE_CASES",
        "inputs": [
            "xyz qwerty asdf",  # Unknown
            "remind me",  # Incomplete
            "schedule",  # Too vague
            "alice",  # Just a name
            "tomorrow at 3 pm",  # Just time
            "what",  # Too vague
            "",  # Empty
        ]
    },
]

def run_test(user_input):
    """Run a single test case"""
    if not user_input.strip():
        return None, None
    
    intent_data = analyze_input(user_input)
    action_data = reason(intent_data, user_input)
    
    return intent_data, action_data

def print_result(category, user_input, intent_data, action_data):
    """Print formatted test result"""
    if intent_data is None:
        print(f"  {RED}⊘ SKIP{RESET}: '{user_input}' (empty input)")
        return
    
    intent = intent_data["intent"]
    confidence = intent_data["confidence"]
    person = intent_data["person"]
    time_val = intent_data["time"]
    action = action_data["action"]
    
    # Color code based on confidence
    if confidence >= 0.85:
        conf_color = GREEN
    elif confidence >= 0.75:
        conf_color = YELLOW
    else:
        conf_color = RED
    
    print(f"  {BLUE}■{RESET} Input: '{user_input}'")
    print(f"    └─ Intent: {conf_color}{intent}{RESET} (conf: {confidence})")
    print(f"       • Action: {action}")
    print(f"       • Person: {person if person else 'None'}")
    print(f"       • Time: {time_val if time_val else 'None'}")
    print()

# Run all tests
print("\n" + "="*100)
print(f"{BLUE}PRACTICAL TEST CASES - Context Aware Assistant{RESET}")
print("="*100 + "\n")

total_tests = 0
undefined_tests = 0

for scenario in test_scenarios:
    category = scenario["category"]
    print(f"{YELLOW}═ {category}{RESET}")
    print()
    
    for user_input in scenario["inputs"]:
        total_tests += 1
        intent_data, action_data = run_test(user_input)
        
        if intent_data is None:
            undefined_tests += 1
        else:
            print_result(category, user_input, intent_data, action_data)

print("="*100)
print(f"{GREEN}✓ Tests Completed: {total_tests - undefined_tests} valid, {undefined_tests} skipped out of {total_tests}{RESET}")
print("="*100 + "\n")

# ==================== INTERACTIVE MODE ====================
print(f"\n{BLUE}═ INTERACTIVE TEST MODE{RESET}")
print("Enter your test input (type 'exit' to quit):\n")

while True:
    try:
        user_input = input(f"{BLUE}Test Input → {RESET}").strip()
        
        if user_input.lower() == "exit":
            print(f"{GREEN}✓ Exiting test mode{RESET}\n")
            break
        
        if not user_input:
            print(f"{YELLOW}⊘ Empty input, try again{RESET}\n")
            continue
        
        intent_data, action_data = run_test(user_input)
        
        if intent_data:
            print()
            print_result("CUSTOM", user_input, intent_data, action_data)
        else:
            print(f"{RED}✗ Error processing input{RESET}\n")
            
    except (KeyboardInterrupt, EOFError):
        print(f"\n{GREEN}✓ Test mode ended{RESET}\n")
        break
