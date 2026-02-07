from functools import wraps
from typing import Any, Callable
from .inference import is_safe

def Smart_YuFeng_XGuard(
    model_size: str,
    verify_input: bool = True,
    verify_output: bool = True,
    default_on_fail_input: Any = '模型输入不安全，请检查！',
    default_on_fail_output: Any = '模型输出不安全，请检查！'
):
    """
    极简智能护栏装饰器。
    
    用户只需指定：
      - model_size: "0.6B" 或 "8B"
      - verify_input: 是否校验输入
      - verify_output: 是否校验输出
    
    其余逻辑全部封装。
    """
    # === 内部预定义规则 ===
    INPUT_RULES = {
        "0.6B": lambda *args, **kwargs: _check_input_0_6B(*args, **kwargs),
        "8B": lambda *args, **kwargs: _check_input_8B(*args, **kwargs),
    }

    OUTPUT_RULES = {
        "0.6B": lambda result: _check_output_0_6B(result),
        "8B": lambda result: _check_output_8B(result),
    }

    # 获取对应规则
    input_checker = INPUT_RULES.get(model_size)
    output_checker = OUTPUT_RULES.get(model_size)

    if input_checker is None or output_checker is None:
        raise ValueError(f"不支持的 model_size: {model_size}，仅支持 '0.6B' 或 '8B'")

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # --- 输入拦截 ---
            if verify_input:
                try:
                    if not input_checker(*args, **kwargs):
                        return default_on_fail_input
                except Exception:
                    return default_on_fail_input

            # --- 执行原函数 ---
            try:
                result = func(*args, **kwargs)
            except Exception:
                # 原函数异常不捕获，由调用者处理
                raise

            # --- 输出拦截 ---
            if verify_output:
                try:
                    if not output_checker(result):
                        return default_on_fail_output
                except Exception:
                    return default_on_fail_output

            return result
        return wrapper
    return decorator


# ========================
# 内部校验逻辑（用户不可见）
# ========================

def _check_input_0_6B(*args, **kwargs) -> bool:
    """0.6B 模型：接受任意非 None 输入"""
    if len(args) == 0 and len(kwargs) == 0:
        return False
    main_input = _serialize_input(*args, **kwargs)
    return is_safe(main_input, model_size="0.6B")


def _check_input_8B(*args, **kwargs) -> bool:
    """8B 模型：接受任意非 None 输入"""
    # 至少有一个参数且不全为 None
    if len(args) == 0 and len(kwargs) == 0:
        return False
    main_input = _serialize_input(*args, **kwargs)
    return is_safe(main_input, model_size="8B")


def _check_output_0_6B(result) -> bool:
    """0.6B 模型：输出不能是 None"""
    return is_safe(str(result), model_size="0.6B")


def _check_output_8B(result) -> bool:
    """8B 模型：输出不能是 None"""
    return is_safe(str(result), model_size="8B")

def _serialize_input(*args, **kwargs) -> str:
    """将所有输入参数序列化为字符串"""
    parts = []
    for arg in args:
        parts.append(str(arg))
    for k, v in kwargs.items():
        parts.append(f"{k}={v}")
    return " | ".join(parts)