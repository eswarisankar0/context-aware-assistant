# Quick Start: Transformer-Based Intent Detection

## Installation

The intent detectors require additional packages. Install them with:

```bash
# For HuggingFace and Sentence Transformers
pip install transformers sentence-transformers

# For Claude API
pip install anthropic

# Or install everything
pip install transformers sentence-transformers anthropic
```

## Testing the Implementations

### 1. Test Sentence Transformers (Recommended - Fast & Lightweight)
```bash
python test_intent_detectors.py
```

Output:
```
Testing SENTENCE_TRANSFORMERS Backend
======================================================================

✓ [92.00%] schedule_meeting     | schedule a meeting with the team tomorrow at 3pm
✓ [88.00%] set_preference       | I prefer quiet hours from 9 to 5
✓ [95.00%] set_reminder         | remind me about the project deadline
✓ [80.00%] retrieve_task        | what did I mention about the presentation?
✓ [91.00%] create_task          | send an email to john.doe@example.com

----------------------------------------------------------------------
Accuracy: 100.0% (5/5)
Average Time: 0.042s per inference
Total Time: 0.21s
```

### 2. Interactive Testing
```bash
python test_intent_detectors.py --interactive
```

### 3. Compare All Backends
```bash
python test_intent_detectors.py --compare
```

### 4. Test Specific Backend
```bash
# Test HuggingFace
python test_intent_detectors.py --backend huggingface

# Test Claude (requires API key)
export ANTHROPIC_API_KEY="sk-ant-..."
python test_intent_detectors.py --backend claude
```

## Using in Your Code

### Simple Usage

```python
from intent_detectors import detect_intent_sentence_transformers

intent, confidence = detect_intent_sentence_transformers("schedule a meeting")
print(f"Intent: {intent}, Confidence: {confidence:.1%}")
```

### With Detector Class

```python
from intent_detectors import TransformerIntentDetector

# Initialize
detector = TransformerIntentDetector(backend="sentence_transformers")

# Use multiple times
result1 = detector.detect("remind me tomorrow")
result2 = detector.detect("create a task")

# Switch backend
detector.switch_backend("huggingface")
result3 = detector.detect("schedule meeting")
```

### Integration with Main App

To use transformers in the main application, uncomment the import in `nlp_engine.py`:

```python
# nlp_engine.py - add at the top
from intent_detectors import TransformerIntentDetector

# In analyze_input() function:
detector = TransformerIntentDetector(backend="sentence_transformers")
intent, confidence = detector.detect(user_input)
```

## Performance Notes

| Backend | First Load | Per Query | Model Size |
|---------|-----------|-----------|-----------|
| Sentence Transformers | ~2s | 40ms | 100MB |
| HuggingFace | ~15s | 50ms | 1.6GB |
| Claude | ~1s | 500ms+ | Cloud |

## Environment Variables

```bash
# Enable Claude API
export ANTHROPIC_API_KEY="sk-ant-..."

# Set default backend (optional)
export INTENT_BACKEND="sentence_transformers"
```

## Troubleshooting

**Q: "ModuleNotFoundError: No module named 'transformers'"**
A: Run `pip install transformers`

**Q: "torch is not installed"**
A: Run `pip install torch` (CPU version is fine)

**Q: Claude API returns authorization error**
A: Check your API key with `echo $ANTHROPIC_API_KEY`

**Q: Very slow on first run**
A: Models are being downloaded. This is one-time. Subsequent runs are fast.

**Q: Out of memory error**
A: Use `sentence_transformers` backend instead (lighter model)

## Next Steps

1. Run `test_intent_detectors.py` to validate your setup
2. Try interactive mode: `python test_intent_detectors.py --interactive`
3. Compare backends: `python test_intent_detectors.py --compare`
4. Integrate best backend into your application
5. See `TRANSFORMER_INTENT_DETECTION.md` for detailed documentation

---

For questions or issues, refer to the main documentation or check the source code in `intent_detectors.py`.
