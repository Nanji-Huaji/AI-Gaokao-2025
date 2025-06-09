import openai
import backoff
import json
import prompt
from typing import Optional
import base64
from pathlib import Path
import os

with open("config.json", "r") as f:
    config = json.load(f)


@backoff.on_exception(
    backoff.expo, (openai.RateLimitError, openai.APIError, openai.APIConnectionError, AssertionError), max_tries=5
)
def create_chat_completion(
    system_prompt: str, user_prompt: str, model: str, img_file_path: Optional[str] = None
) -> str:
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
                {"type": "text", "text": user_prompt},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"}},
            ],
        }
    else:
        # 纯文本消息格式
        user_message = {"role": "user", "content": user_prompt}

    messages.append(user_message)

    client = openai.OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=config[model]["api_base"],
    )

    response = client.chat.completions.create(
        model=config[model]["model"],
        messages=messages,
        temperature=config[model]["temperature"],
        max_tokens=config[model].get("max_tokens", 3000),
    )

    assert response.choices[0].message.content is not None
    return response.choices[0].message.content


def encode_image(image_path: str) -> str:
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def get_image_mime_type(image_path: str) -> str:
    suffix = Path(image_path).suffix.lower()
    mime_types = {
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
        ".gif": "image/gif",
        ".webp": "image/webp",
    }
    return mime_types.get(suffix, "image/jpeg")


def answer_single_question(question: str, model) -> str:
    user_prompt = prompt.user_prompt.format(question=question)
    answer = create_chat_completion(
        system_prompt=prompt.system_prompt,
        user_prompt=user_prompt,
        model=model,
    )
    return answer.strip()


def answer_json_file(file: str, model: str) -> list:
    with open(file, "r") as f:
        data = json.load(f)
    answers = []
    for question_dict in data:
        idx = question_dict.get("index")
        question = question_dict.get("content")
        type = question_dict.get("type")
        full_score = question_dict.get("score", 0)
        answer = answer_single_question(question, model)
        answer = {"index": idx, "content": answer, "type": type, "full_score": full_score, "score_get": None}
        answers.append(answer)
    with open("results/result.json", "w") as f:
        json.dump(answers, f, ensure_ascii=False, indent=4)
    return answers
