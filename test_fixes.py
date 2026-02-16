from nlp_engine import analyze_input
from reasoning_engine import reason

test_cases = [
    ('schedule meeting tomorrow with alice', 'Person without title', 'alice'),
    ('send an email to john sir by 5 pm', 'create_task action', 'store_task'),
    ('what have I told you about the project', 'Memory recall intent', 'retrieve_task'),
]

print("\n" + "="*80)
print("TESTING FIXES")
print("="*80)

for user_input, description, expected in test_cases:
    intent_data = analyze_input(user_input)
    action_data = reason(intent_data, user_input)
    
    if "intent" in expected.lower():
        actual = intent_data['intent']
    elif "task" in expected.lower():
        actual = action_data['action']
    else:
        actual = intent_data['person']
    
    status = "✓ PASS" if actual == expected else "✗ FAIL"
    
    print(f"\n{status} | {description}")
    print(f"  Input: {user_input}")
    if "intent" in description.lower():
        print(f"  Expected: {expected}, Got: {actual}")
    elif "task" in description.lower():
        print(f"  Intent: {intent_data['intent']}")
        print(f"  Expected Action: {expected}, Got: {actual}")
    else:
        print(f"  Expected: {expected}, Got: {actual}")

print("\n" + "="*80)
