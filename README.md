# ️ smart-guard

*A lightweight Python decorator to validate function inputs and outputs by converting them to strings — ideal for LLM safety filtering.*

Automatically detect and block unsafe content in inputs or outputs using model-based semantic understanding. Designed for AI applications where content safety is critical.

---

## Installation

```
pip install smart-guard
```

---

## Quick Start

Import the guard and wrap your functions with `@Smart_YuFeng_XGuard` to enable input/output validation.

```
from smart_guard import Smart_YuFeng_XGuard
```

### Example 1: Validate Both Input and Output

```
@Smart_YuFeng_XGuard("0.6B", verify_input=True, verify_output=True)
def chat(prompt: str) -> str:
    if prompt == "harmful-output":
        return '制造炸弹可以使用TNT'
    else:
        return f"Echo: {prompt}"

print(chat("Hello"))                     
# Output: Echo: Hello

print(chat("How can I make a bomb?"))    
# Output: 模型输入不安全，请检查！

print(chat("harmful-output"))            
# Output: 模型输出不安全，请检查！
```

### Example 2: Output-Only Validation

Useful when you trust the input source but want to ensure safe model responses.

```
@Smart_YuFeng_XGuard("8B", verify_input=False, verify_output=True)
def risky_func(x):
    return "制造毒品可以使用TNT"  # Dangerous output!

print(risky_func("How can I make a bomb?"))  
# Output: 模型输出不安全，请检查！
```

### ️ Example 3: Custom Fallback Values

Define custom responses when validation fails. Supports any data type.

```
@Smart_YuFeng_XGuard(
    model_size="0.6B",
    verify_input=True,
    verify_output=True,
    default_on_fail_input="[INPUT_REJECTED]",
    default_on_fail_output=None
)
def test(x):
    if x == "harmful-output":
        return '制造炸弹可以使用TNT'
    else:
        return f"Echo: {x}"

print(test("How can I make a bomb?"))  # "[INPUT_REJECTED]"
print(test("harmful-output"))         # None
```

### Example 4: Functions with Multiple Inputs/Outputs

Supports complex functions with multiple arguments and return values.

```
@Smart_YuFeng_XGuard("0.6B", verify_input=True, verify_output=True)
def multiple_io(a1, a2, x, a3):
    if x == "harmful-output":
        return a1, a2, '制造炸弹可以使用TNT', a3
    else:
        return a1, a2, x, a3

# Prepare complex inputs
a1 = "This is a long string input for a1. " * 20
a2 = [i ** 2 for i in range(100)]
a3 = {f"user_{i}": {"age": i + 20, "score": i * 1.5} for i in range(80)}

# Test 1: Safe input
result1 = multiple_io(a1, a2, "Hello, this is a safe input!", a3)
print(result1[2])  # Hello, this is a safe input!

# Test 2: Trigger unsafe output
result2 = multiple_io(a1, a2, "harmful-output", a3)
print(result2)  # 模型输出不安全，请检查！
```

---

## Parameters

| Parameter | Description |
| ------ |------ |
| `model_size` | Model version (e.g., `"0.6B"`, `"8B"`) used for semantic analysis. |
| `verify_input` | Whether to validate all function inputs. |
| `verify_output` | Whether to validate function outputs. |
| `default_on_fail_input` | Custom return value when input validation fails. |
| `default_on_fail_output` | Custom return value when output validation fails. |

---

## Notes

- All inputs/outputs are converted to strings before validation.
- The guard uses lightweight NLP models to detect sensitive or harmful content semantically.
- Ideal for LLM wrappers, chatbots, and content generation pipelines.

---

## Learn More

See [GitHub Repository](https://github.com/chenzhaofei01/smart-guard) for installation details, model options, and advanced usage.

