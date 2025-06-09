import openai
import backoff
import json
import prompt
from typing import Optional
import base64
from pathlib import Path
import os
import re

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


def answer_single_question(question: str, model: str, type: str, img_file: Optional[str] = None) -> str:
    user_prompt = prompt.user_prompt.format(question=question, type=type)
    if img_file is not None:
        answer = create_chat_completion(
            system_prompt=prompt.system_prompt,
            user_prompt=user_prompt,
            model=model,
            img_file_path=img_file,
        )
    else:
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
        img_file = question_dict.get("img_file", None)
        answer = answer_single_question(question, model, type, img_file)
        reference_answer = question_dict.get("answer", "")
        if type == "选择题" or type == "多选题" or type == "填空题":
            answer = extract_answer(answer)
        answer_dict = {
            "index": idx,
            "student_answer": answer,
            "reference_answer": reference_answer,
            "type": type,
            "full_score": full_score,
            "score_get": None,
        }
        answers.append(answer_dict)
        sorted_answers = sorted(answers, key=lambda x: x["index"])
    with open("results/result.json", "w") as f:
        json.dump(sorted_answers, f, ensure_ascii=False, indent=4)
    return answers


def extract_answer(text: str) -> str:
    """
    从文本中提取"答案：<答案>"格式的内容

    Args:
        text: 包含答案的文本

    Returns:
        提取出的答案，如果没有找到匹配则返回空字符串
    """
    # 使用正则表达式匹配"答案："后面的内容
    pattern = r"答案：([\s\S]*?)(?:\n\n|$)"
    match = re.search(pattern, text)

    if match:
        return match.group(1).strip()
    else:
        # 尝试匹配其他可能的格式
        pattern2 = r"答案[：:]([\s\S]*?)(?:\n\n|$)"
        match2 = re.search(pattern2, text)
        if match2:
            return match2.group(1).strip()

    return ""
