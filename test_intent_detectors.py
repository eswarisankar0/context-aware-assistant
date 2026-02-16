#!/usr/bin/env python3
"""
Example script demonstrating all three transformer-based intent detection methods.
Run this to test and compare the different backends.

Usage:
    python test_intent_detectors.py
    python test_intent_detectors.py --backend huggingface
    python test_intent_detectors.py --backend sentence_transformers
    python test_intent_detectors.py --backend claude
"""

import sys
import argparse
import time
from typing import List, Tuple

from intent_detectors import (
    TransformerIntentDetector,
    INTENT_CONFIG,
    detect_intent_huggingface,
    detect_intent_sentence_transformers,
    detect_intent_claude,
)

# Test inputs with expected intents
TEST_DATA = [
    ("schedule a meeting with the team tomorrow at 3pm", "schedule_meeting"),
    ("I prefer quiet hours from 9 to 5", "set_preference"),
    ("remind me about the project deadline", "set_reminder"),
    ("what did I mention about the presentation?", "retrieve_task"),
    ("send an email to john.doe@example.com", "create_task"),
    ("set timezone to UTC", "set_preference"),
    ("alert me 30 minutes before the call", "set_reminder"),
    ("when is my next meeting?", "retrieve_task"),
    ("buy coffee beans", "create_task"),
    ("hello there", "unknown"),
]

def test_single_backend(backend: str) -> None:
    """Test a single backend detector"""
    print(f"\n{'=' * 70}")
    print(f"Testing {backend.upper()} Backend")
    print(f"{'=' * 70}\n")
    
    detector = TransformerIntentDetector(backend=backend)
    
    results = []
    total_time = 0
    
    for text, expected_intent in TEST_DATA:
        try:
            start_time = time.time()
            intent, confidence = detector.detect(text)
            elapsed = time.time() - start_time
            total_time += elapsed
            
            is_correct = intent == expected_intent
            status = "✓" if is_correct else "✗"
            
            results.append((text, intent, confidence, expected_intent, elapsed))
            
            print(f"{status} [{confidence:.2%}] {intent:<18} | {text[:50]}")
            if not is_correct:
                print(f"  Expected: {expected_intent}")
                
        except Exception as e:
            print(f"✗ [ERROR] {text[:50]}")
            print(f"  Error: {str(e)[:60]}")
    
    # Summary
    correct = sum(1 for _, intent, _, expected, _ in results if intent == expected)
    accuracy = correct / len(results) if results else 0
    avg_time = total_time / len(results) if results else 0
    
    print(f"\n{'-' * 70}")
    print(f"Accuracy: {accuracy:.1%} ({correct}/{len(results)})")
    print(f"Average Time: {avg_time:.3f}s per inference")
    print(f"Total Time: {total_time:.2f}s")

def test_all_backends() -> None:
    """Test all available backends and compare"""
    print(f"\n{'=' * 70}")
    print("Comparison of All Backends")
    print(f"{'=' * 70}\n")
    
    backends = ["sentence_transformers", "huggingface", "claude"]
    comparison = {}
    
    for backend in backends:
        try:
            print(f"\nInitializing {backend.upper()}...")
            detector = TransformerIntentDetector(backend=backend)
            
            correct = 0
            total_time = 0
            
            for text, expected_intent in TEST_DATA:
                try:
                    start_time = time.time()
                    intent, confidence = detector.detect(text)
                    elapsed = time.time() - start_time
                    total_time += elapsed
                    
                    if intent == expected_intent:
                        correct += 1
                except Exception:
                    pass
            
            accuracy = correct / len(TEST_DATA)
            avg_time = total_time / len(TEST_DATA) if TEST_DATA else 0
            
            comparison[backend] = {
                "accuracy": accuracy,
                "avg_time": avg_time,
                "total_time": total_time
            }
            
        except Exception as e:
            print(f"Failed to test {backend}: {e}")
    
    # Print comparison table
    print(f"\n{'Backend':<25} {'Accuracy':<15} {'Avg Time':<15} {'Total Time':<15}")
    print(f"{'-' * 70}")
    
    for backend, metrics in comparison.items():
        print(
            f"{backend:<25} "
            f"{metrics['accuracy']:.1%}{'':8} "
            f"{metrics['avg_time']:.3f}s{'':8} "
            f"{metrics['total_time']:.2f}s"
        )

def interactive_mode(backend: str = "sentence_transformers") -> None:
    """Interactive mode - test custom inputs"""
    print(f"\n{'=' * 70}")
    print(f"Interactive Mode - {backend.upper()} Backend")
    print(f"{'=' * 70}")
    print("\nEnter text to analyze intent. Type 'quit' to exit.\n")
    
    detector = TransformerIntentDetector(backend=backend)
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if user_input.lower() == "quit":
                print("Exiting...")
                break
            
            if not user_input:
                continue
            
            start_time = time.time()
            intent, confidence = detector.detect(user_input)
            elapsed = time.time() - start_time
            
            description = INTENT_CONFIG[intent]["template"]
            
            print(f"\nIntent: {intent}")
            print(f"Confidence: {confidence:.1%}")
            print(f"Description: {description}")
            print(f"Time: {elapsed:.3f}s\n")
            
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"Error: {e}\n")

def main():
    parser = argparse.ArgumentParser(
        description="Test transformer-based intent detection"
    )
    parser.add_argument(
        "--backend",
        choices=["huggingface", "sentence_transformers", "claude"],
        help="Specific backend to test"
    )
    parser.add_argument(
        "--compare",
        action="store_true",
        help="Compare all backends"
    )
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Interactive mode for custom inputs"
    )
    
    args = parser.parse_args()
    
    if args.compare:
        test_all_backends()
    elif args.interactive:
        backend = args.backend or "sentence_transformers"
        interactive_mode(backend)
    elif args.backend:
        test_single_backend(args.backend)
    else:
        # Default: test sentence_transformers (fastest)
        print("Testing Sentence Transformers backend (default - fastest)")
        test_single_backend("sentence_transformers")
        
        print("\n\nTo compare all backends, run:")
        print("  python test_intent_detectors.py --compare")
        print("\nTo test specific backend:")
        print("  python test_intent_detectors.py --backend huggingface")
        print("  python test_intent_detectors.py --backend sentence_transformers")
        print("  python test_intent_detectors.py --backend claude")
        print("\nFor interactive mode:")
        print("  python test_intent_detectors.py --interactive --backend sentence_transformers")

if __name__ == "__main__":
    main()
