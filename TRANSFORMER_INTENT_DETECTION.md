# Transformer-Based Intent Detection

This document explains how to use transformer-based intent detection in the NIXIN AI system.

## Overview

The system supports **three transformer-based intent detection methods**:

1. **HuggingFace Zero-Shot Classification** - Facebook BART-large-mnli
2. **Sentence Transformers** - Semantic similarity-based classification
3. **Claude API** - Anthropic's Claude model

All methods are available in `intent_detectors.py` and can be used alongside the default rule-based detector.

---

## 1. HuggingFace Zero-Shot Classification

### Features
- ✅ No fine-tuning needed
- ✅ Works with any set of intent labels
- ✅ Fast inference on CPU
- ⚠️ Large model downloads (~1.6GB for BART)

### Quick Start

```python
from intent_detectors import detect_intent_huggingface

# First call will download the model
intent, confidence = detect_intent_huggingface("schedule a meeting tomorrow")
print(f"Intent: {intent}, Confidence: {confidence}")
```

### Output Example
```
Intent: schedule_meeting, Confidence: 0.92
```

### Using the Classifier

```python
from intent_detectors import detect_intent_huggingface, init_huggingface_classifier

# Initialize once
classifier = init_huggingface_classifier()

# Use multiple times
intent1, conf1 = detect_intent_huggingface("What did I say earlier?", classifier)
intent2, conf2 = detect_intent_huggingface("Send an email", classifier)
```

---

## 2. Sentence Transformers (Semantic Similarity)

### Features
- ✅ Lightweight model (~100MB)
- ✅ Fast inference
- ✅ Semantic understanding
- ✅ Works on CPU efficiently

### Quick Start

```python
from intent_detectors import detect_intent_sentence_transformers

intent, confidence = detect_intent_sentence_transformers("remind me in 30 minutes")
print(f"Intent: {intent}, Confidence: {confidence}")
```

### Output Example
```
Intent: set_reminder, Confidence: 0.78
```

### Using the Model

```python
from intent_detectors import detect_intent_sentence_transformers, init_sentence_transformer

# Initialize once
model = init_sentence_transformer()

# Use multiple times
intent1, conf1 = detect_intent_sentence_transformers("submit the report", model)
intent2, conf2 = detect_intent_sentence_transformers("call headquarters", model)
```

---

## 3. Claude API (Anthropic)

### Features
- ✅ State-of-the-art language understanding
- ✅ Contextual awareness
- ✅ Flexible intent definitions
- ⚠️ Requires API key and credits

### Setup

1. **Install Anthropic SDK**
   ```bash
   pip install anthropic
   ```

2. **Set your API key**
   ```bash
   export ANTHROPIC_API_KEY="sk-ant-..."
   ```

### Quick Start

```python
from intent_detectors import detect_intent_claude

intent, confidence = detect_intent_claude("organize a team meeting")
print(f"Intent: {intent}, Confidence: {confidence}")
```

### Output Example
```
Intent: schedule_meeting, Confidence: 0.95
```

### Usage without environment variable

```python
from intent_detectors import detect_intent_claude

api_key = "sk-ant-..."
intent, confidence = detect_intent_claude("remind me tomorrow", api_key)
```

---

## 4. Unified Detector Interface

Use the `TransformerIntentDetector` class to switch between backends dynamically:

```python
from intent_detectors import TransformerIntentDetector

# Start with HuggingFace
detector = TransformerIntentDetector(backend="huggingface")
intent1, conf1 = detector.detect("schedule a meeting")

# Switch to Sentence Transformers
detector.switch_backend("sentence_transformers")
intent2, conf2 = detector.detect("set a reminder")

# Switch to Claude
detector.switch_backend("claude")
intent3, conf3 = detector.detect("create a task")
```

---

## Available Intents

Both rule-based and transformer methods recognize these intents:

| Intent | Example |
|--------|---------|
| `set_preference` | "I prefer coffee over tea", "Set timezone to EST" |
| `set_reminder` | "Remind me about the meeting", "Alert in 30 mins" |
| `schedule_meeting` | "Schedule meeting tomorrow", "Book appointment" |
| `retrieve_task` | "What did I say?", "Do you remember?" |
| `create_task` | "Submit the report", "Call the client" |
| `unknown` | (when intent cannot be determined) |

---

## Performance Comparison

| Method | Speed | Accuracy | Model Size | Requirements |
|--------|-------|----------|-----------|--------------|
| **Rule-Based** | ⚡ Fast | ⭐⭐⭐ Good | None | None |
| **HuggingFace** | ⚡⚡ Medium | ⭐⭐⭐⭐ Excellent | 1.6GB | transformers |
| **Sentence Transformers** | ⚡ Fast | ⭐⭐⭐⭐ Excellent | 100MB | sentence-transformers |
| **Claude API** | ⚡⚡ Medium | ⭐⭐⭐⭐⭐ State-of-art | Cloud | Internet, API Key |

---

## Integration in Main Application

### To use transformer detection in `nlp_engine.py`:

```python
from intent_detectors import TransformerIntentDetector

# In nlp_engine.py
detector = TransformerIntentDetector(backend="huggingface")

def analyze_input(user_input):
    # ... existing code ...
    
    # Use transformer-based detection
    intent, confidence = detector.detect(user_input)
    
    return {
        "intent": intent,
        "entities": entities,  
        "confidence": confidence,
        "timestamp": datetime.now()
    }
```

### To enable specific backend via environment variable:

```bash
# Use HuggingFace
export INTENT_BACKEND="huggingface"

# Use Sentence Transformers
export INTENT_BACKEND="sentence_transformers"

# Use Claude
export INTENT_BACKEND="claude"

python main.py
```

---

## Example: Complete Workflow

```python
from intent_detectors import TransformerIntentDetector, INTENT_CONFIG

# Initialize detector
detector = TransformerIntentDetector(backend="sentence_transformers")

# Sample inputs
test_inputs = [
    "Schedule a meeting with the team tomorrow",
    "I prefer quiet hours from 9 to 5",
    "Remind me about the project deadline",
    "What did I mention about the presentation?",
    "Send an email to John"
]

print("=" * 60)
print("Intent Detection Results")
print("=" * 60)

for text in test_inputs:
    intent, confidence = detector.detect(text)
    description = INTENT_CONFIG[intent]["template"]
    
    print(f"\nInput: {text}")
    print(f"Intent: {intent} ({confidence:.2%} confidence)")
    print(f"Description: {description}")
```

**Output:**
```
============================================================
Intent Detection Results
============================================================

Input: Schedule a meeting with the team tomorrow
Intent: schedule_meeting (92.00% confidence)
Description: scheduling a meeting or appointment

Input: I prefer quiet hours from 9 to 5
Intent: set_preference (88.00% confidence)
Description: setting user preference or configuration

Input: Remind me about the project deadline
Intent: set_reminder (95.00% confidence)
Description: setting a reminder or alert

Input: What did I mention about the presentation?
Intent: retrieve_task (80.00% confidence)
Description: retrieving or recalling information from memory

Input: Send an email to John
Intent: create_task (91.00% confidence)
Description: creating a new task or to-do
```

---

## Troubleshooting

### Issue: Large model download is slow
**Solution:** Use Sentence Transformers backend instead (100MB vs 1.6GB)

### Issue: Claude API returns errors
**Solution:** Check that `ANTHROPIC_API_KEY` is set and valid

### Issue: Out of memory errors
**Solution:** Use rule-based detection or smaller models

### Issue: Model not found
**Solution:** First call downloads models automatically. Ensure internet connection.

---

## Advanced Configuration

### Custom Intent Labels

```python
from intent_detectors import detect_intent_huggingface, init_huggingface_classifier

classifier = init_huggingface_classifier()

# Custom labels
custom_labels = [
    "customer inquiry",
    "technical support",
    "billing question",
    "general question"
]

# Use with custom text
result = classifier("My bill is incorrect", 
                     custom_labels, 
                     multi_class=False)
```

---

## Cost Considerations

- **Rule-Based**: Free ✅
- **HuggingFace**: Free (one-time download) ✅
- **Sentence Transformers**: Free (one-time download) ✅
- **Claude API**: ~$0.003 per 1K input tokens 💰

---

## Next Steps

1. **Test different backends** with your data
2. **Measure performance** on your specific use cases
3. **Fine-tune** if needed for domain-specific intents
4. **Monitor confidence scores** to detect uncertain cases

For more information, see `intent_detectors.py` source code.
