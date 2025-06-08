import openai
import backoff
import json
import prompt
from typing import Optional
import base64
from pathlib import Path


with open("config.json", "r") as f:
    config = json.load(f)


@backoff.on_exception(
    backoff.expo,
    (openai.RateLimitError, 
    openai.APIError, 
    openai.APIConnectionError,
    AssertionError),
    max_tries=5
)
def create_chat_completion(system_prompt: str, user_prompt: str, model: str, img_file_path: Optional[str] = None) -> str:
    messages = []
    messages.append({"role": "system", "content": system_prompt})
    
    # 构建用户消息
    if img_file_path is not None:
        # 读取并编码图片
        image_base64 = encode_image(img_file_path)
        
        # 包含图片的消息格式
        user_message = {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": user_prompt
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{image_base64}"
                    }
                }
            ]
        }
    else:
        # 纯文本消息格式
        user_message = {
            "role": "user",
            "content": user_prompt
        }
    
    messages.append(user_message)
    
    client = openai.OpenAI(
        api_key=config[model]["openai_api_key"],
        base_url=config[model]["openai_base"],
    )
    
    response = client.chat.completions.create(
        model=config[model]["model"],
        messages=messages,
        temperature=config[model]["temperature"],
        max_tokens=config[model].get("max_tokens", 3000)  
    )
    
    assert response.choices[0].message.content is not None
    return response.choices[0].message.content

def encode_image(image_path: str) -> str:
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def get_image_mime_type(image_path: str) -> str:
    suffix = Path(image_path).suffix.lower()
    mime_types = {
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.png': 'image/png',
        '.gif': 'image/gif',
        '.webp': 'image/webp'
    }
    return mime_types.get(suffix, 'image/jpeg')

def answer_single_question(index: int) -> str:
    pass

def eval_answer(index: int) -> str:
    pass
