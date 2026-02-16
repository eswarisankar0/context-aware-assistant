"""
Comprehensive test suite for context-aware assistant
Tests across all intent types, entity combinations, and edge cases
"""

from nlp_engine import analyze_input
from reasoning_engine import reason
import json

test_cases = [
    # ==================== SET_REMINDER TESTS ====================
    {
        "input": "remind me to submit undertaking form to kavita mam on 17 feb 2026",
        "category": "set_reminder",
        "expected_intent": "set_reminder",
        "expected_action": "store_task",
        "has_person": True,
        "has_time": True,
    },
    {
        "input": "remind me about the meeting tomorrow",
        "category": "set_reminder",
        "expected_intent": "set_reminder",
        "expected_action": "store_task",
        "has_person": False,
        "has_time": True,
    },
    {
        "input": "remind me to call alice",
        "category": "set_reminder",
        "expected_intent": "set_reminder",
        "expected_action": "store_task",
        "has_person": True,
        "has_time": False,
    },
    {
        "input": "alert me at 3 pm",
        "category": "set_reminder",
        "expected_intent": "set_reminder",
        "expected_action": "store_task",
        "has_person": False,
        "has_time": True,
    },
    
    # ==================== SCHEDULE_MEETING TESTS ====================
    {
        "input": "schedule meeting tomorrow",
        "category": "schedule_meeting",
        "expected_intent": "schedule_meeting",
        "expected_action": "schedule_with_preference",  # or schedule_default
        "has_person": False,
        "has_time": True,
    },
    {
        "input": "schedule meeting tomorrow with alice",
        "category": "schedule_meeting",
        "expected_intent": "schedule_meeting",
        "expected_action": "schedule_with_preference",  # or schedule_default
        "has_person": True,
        "has_time": True,
    },
    {
        "input": "book an appointment with dr. smith on monday",
        "category": "schedule_meeting",
        "expected_intent": "schedule_meeting",
        "expected_action": "schedule_with_preference",  # or schedule_default
        "has_person": True,
        "has_time": True,
    },
    
    # ==================== SET_PREFERENCE TESTS ====================
    {
        "input": "set preference for morning time",
        "category": "set_preference",
        "expected_intent": "set_preference",
        "expected_action": "store_preference",
        "has_person": False,
        "has_time": False,
    },
    {
        "input": "I prefer coffee over tea",
        "category": "set_preference",
        "expected_intent": "set_preference",
        "expected_action": "store_preference",
        "has_person": False,
        "has_time": False,
    },
    {
        "input": "prefer meetings in the afternoon",
        "category": "set_preference",
        "expected_intent": "set_preference",
        "expected_action": "store_preference",
        "has_person": False,
        "has_time": False,
    },
    
    # ==================== CREATE_TASK TESTS ====================
    {
        "input": "send an email to john sir by 5 pm",
        "category": "create_task",
        "expected_intent": "create_task",
        "expected_action": "store_task",
        "has_person": True,
        "has_time": True,
    },
    {
        "input": "submit the report by friday",
        "category": "create_task",
        "expected_intent": "create_task",
        "expected_action": "store_task",
        "has_person": False,
        "has_time": True,
    },
    {
        "input": "call the client today",
        "category": "create_task",
        "expected_intent": "create_task",
        "expected_action": "store_task",
        "has_person": False,
        "has_time": True,
    },
    {
        "input": "prepare presentation for alice",
        "category": "create_task",
        "expected_intent": "create_task",
        "expected_action": "store_task",
        "has_person": True,
        "has_time": False,
    },
    {
        "input": "finish the project",
        "category": "create_task",
        "expected_intent": "create_task",
        "expected_action": "store_task",
        "has_person": False,
        "has_time": False,
    },
    {
        "input": "pay the bill on 20 feb",
        "category": "create_task",
        "expected_intent": "create_task",
        "expected_action": "store_task",
        "has_person": False,
        "has_time": True,
    },
    
    # ==================== RETRIEVE_TASK / MEMORY RECALL TESTS ====================
    {
        "input": "what have I told you about the project",
        "category": "retrieve_task",
        "expected_intent": "retrieve_task",
        "expected_action": "semantic_recall",
        "has_person": False,
        "has_time": False,
    },
    {
        "input": "did I mention anything about the meeting",
        "category": "retrieve_task",
        "expected_intent": "retrieve_task",
        "expected_action": "semantic_recall",
        "has_person": False,
        "has_time": False,
    },
    {
        "input": "what did I tell you earlier",
        "category": "retrieve_task",
        "expected_intent": "retrieve_task",
        "expected_action": "semantic_recall",
        "has_person": False,
        "has_time": False,
    },
    {
        "input": "do you remember my preferences",
        "category": "retrieve_task",
        "expected_intent": "retrieve_task",
        "expected_action": "semantic_recall",
        "has_person": False,
        "has_time": False,
    },
    
    # ==================== EDGE CASES ====================
    {
        "input": "remind alice to send report to kavita mam on 18 feb",
        "category": "edge_case_multiple_people",
        "expected_intent": "set_reminder",
        "expected_action": "store_task",
        "has_person": True,
        "has_time": True,
    },
    {
        "input": "schedule meeting with john sir tomorrow at 2 pm",
        "category": "edge_case_time_and_person",
        "expected_intent": "schedule_meeting",
        "has_person": True,
        "has_time": True,
    },
    {
        "input": "xyz qwerty asdf",
        "category": "unknown",
        "expected_intent": "unknown",
        "expected_action": "clarify",
        "has_person": False,
        "has_time": False,
    },
]

# Run tests
print("\n" + "="*100)
print("COMPREHENSIVE TEST SUITE - Context Aware Assistant")
print("="*100 + "\n")

passed = 0
failed = 0
warnings = 0

for idx, test in enumerate(test_cases, 1):
    user_input = test["input"]
    intent_data = analyze_input(user_input)
    action_data = reason(intent_data, user_input)
    
    # Check intent
    intent_match = intent_data["intent"] == test["expected_intent"]
    action_match = action_data["action"] == test.get("expected_action", action_data["action"])  # Default to actual if not specified
    
    # Check entities
    person_check = (intent_data["person"] is not None) == test["has_person"]
    time_check = (intent_data["time"] is not None) == test["has_time"]
    
    # Overall result
    all_pass = intent_match and action_match and person_check and time_check
    
    if all_pass:
        status = "✓ PASS"
        passed += 1
    else:
        status = "✗ FAIL"
        failed += 1
    
    print(f"{idx:2d}. {status} | {test['category'].upper()}")
    print(f"    Input: {user_input}")
    print(f"    Intent: {intent_data['intent']} (expected: {test['expected_intent']}) {'✓' if intent_match else '✗'}")
    if "expected_action" in test:
        print(f"    Action: {action_data['action']} (expected: {test['expected_action']}) {'✓' if action_match else '✗'}")
    else:
        print(f"    Action: {action_data['action']}")
    print(f"    Person: {intent_data['person']} (expected: {'present' if test['has_person'] else 'absent'}) {'✓' if person_check else '✗'}")
    print(f"    Time: {intent_data['time']} (expected: {'present' if test['has_time'] else 'absent'}) {'✓' if time_check else '✗'}")
    print(f"    Confidence: {intent_data['confidence']}")
    
    if not all_pass:
        print(f"    Full entities: {intent_data['entities']}")
    
    print()

# Summary
print("="*100)
print(f"TEST SUMMARY: {passed} PASSED, {failed} FAILED out of {len(test_cases)} tests")
print(f"Success Rate: {(passed/len(test_cases)*100):.1f}%")
print("="*100)

# Detailed failure report
if failed > 0:
    print("\n⚠️  FAILURES DETECTED - Review above for details")
else:
    print("\n✓ ALL TESTS PASSED!")
