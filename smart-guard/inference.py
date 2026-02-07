import torch
from modelscope import AutoModelForCausalLM, AutoTokenizer

# 全局变量用于缓存已加载的模型和 tokenizer
_LOADED_MODELS = {}

def _load_model(model_size: str):
    """内部函数：根据 model_size 加载模型和 tokenizer"""
    if model_size not in _LOADED_MODELS:
        if model_size == "0.6B":
            model_name = "Alibaba-AAIG/YuFeng-XGuard-Reason-0.6B"
        elif model_size == "8B":
            model_name = "Alibaba-AAIG/YuFeng-XGuard-Reason-8B"
        else:
            raise ValueError("model_size 必须是 '0.6B' 或 '8B'")
        
        print(f"正在加载 {model_size} 模型...")
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype="auto",
            device_map="auto"
        ).eval()
        _LOADED_MODELS[model_size] = (model, tokenizer)
        print(f"{model_size} 模型加载完成。")
    return _LOADED_MODELS[model_size]

def is_safe(text, model_size="0.6B"):
    """
    判断输入是否安全。
    
    参数:
        messages (list): 聊天消息列表，格式如 [{"role": "user", "content": "..."}]
        model_size (str): 使用的模型大小，可选 "0.6B" 或 "8B"
    
    返回:
        bool: True 表示安全（输出为 "sec"），False 表示不安全
    """
    model, tokenizer = _load_model(model_size)

    messages=[
        {'role': 'user', 'content': text},
    ]
    rendered_query = tokenizer.apply_chat_template(
        messages, policy=None, reason_first=False, tokenize=False
    )

    model_inputs = tokenizer([rendered_query], return_tensors="pt").to(model.device)
    
    with torch.no_grad():
        outputs = model.generate(
            **model_inputs,
            max_new_tokens=1,
            do_sample=False,
            output_scores=True,
            return_dict_in_generate=True
        )

    batch_idx = 0
    input_length = model_inputs['input_ids'].shape[1]
    output_ids = outputs["sequences"].tolist()[batch_idx][input_length:]
    response = tokenizer.decode(output_ids, skip_special_tokens=True)
    
    return response == "sec"
