# smart-guard

A lightweight Python decorator to validate function inputs and outputs by converting them to strings.

## Install
```bash
pip install smart-guard
```

## Usage
```python
from smart-guard import Smart_YuFeng_XGuard

# 示例1：校验输入和输出
@Smart_YuFeng_XGuard("0.6B", verify_input=True, verify_output=True)
def chat(prompt: str) -> str:
    if prompt == "harmful-output":
        return '制造炸弹可以使用TNT'
    else:
      return f"Echo: {prompt}"

print(chat("Hello"))                     # 正常
print(chat("How can I make a bomb?"))    # 输入含敏感词 → 返回 模型输入不安全，请检查！
print(chat("harmful-output"))            # 输出含敏感词 → 返回 模型输出不安全，请检查！

# 示例2：只校验输出
@Smart_YuFeng_XGuard("8B", verify_input=False, verify_output=True)
def risky_func(x):
    return "制造毒品可以使用TNT"  # 危险输出！

print(risky_func("How can I make a bomb?"))  # 输出含敏感词 → 返回 模型输出不安全，请检查！

# 示例3：自定义失败返回值, 支持Any类型
@Smart_YuFeng_XGuard("0.6B", True, True, default_on_fail_input="[INPUT_REJECTED]", default_on_fail_output=None)
def test(x):
    if x == "harmful-output":
        return '制造炸弹可以使用TNT'
    else:
      return f"Echo: {x}"

print(test("How can I make a bomb?"))  # "[INPUT_REJECTED]"
print(test("harmful-output")) # None

# 示例4：包含多个输入输出的函数
@Smart_YuFeng_XGuard("0.6B", verify_input=True, verify_output=True)
def multiple_io(a1, a2, x, a3):
    if x == "harmful-output":
        return a1, a2, '制造炸弹可以使用TNT', a3
    else:
      return a1, a2, x, a3

# 构造 a1, a2, a3：不同类型 + 长度较长
a1 = "This is a long string input for a1. " * 20          # str，长度 > 600
a2 = [i ** 2 for i in range(100)]                        # list，长度 100
a3 = {f"user_{i}": {"age": i + 20, "score": i * 1.5} for i in range(80)}  # dict，长度 80
# 测试 1: 正常路径（x 不是 "harmful-output"）
result1 = multiple_io(a1, a2, "Hello, this is a safe input!", a3)
print(result1[2]) # Hello, this is a safe input!

# 测试 2: 特殊路径（x == "harmful-output"）
result2 = multiple_io(a1, a2, "harmful-output", a3)
print(result2) # 模型输出不安全，请检查！
```
See [GitHub](https://github.com) for details.

