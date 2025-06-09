from chat import create_chat_completion
from prompt import eval_prompt
import json


def get_answer_score(student_answer: str, reference_answer: str, type: str, score: int) -> int:
    system_prompt = "你是一个2025年高考的改卷人。你正在评阅一名学生的高考数学试题答案。"
    user_prompt = eval_prompt.format(
        score=score, type=type, reference_answer=reference_answer, student_answer=student_answer
    )

    judge_score = create_chat_completion(system_prompt=system_prompt, user_prompt=user_prompt, model="o4-mini")
    assert judge_score is not None, "评分失败"
    judge_score = judge_score.strip()
    if judge_score.isdigit():
        judge_score = int(judge_score)
    else:
        raise ValueError(f"评分结果不合法: {judge_score}")
    return judge_score


def eval_json_file(file: str) -> None:
    with open(file, "w") as f:
        data = json.load(f)
    for answer_dict in data:
        student_answer = answer_dict["student_answer"]
        reference_answer = answer_dict["reference_answer"]
        type = answer_dict["type"]
        full_score = answer_dict["full_score"]
        judge_score = get_answer_score(student_answer, reference_answer, type, full_score)
        answer_dict["score"] = judge_score
    with open(file, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def show_result(file: str) -> None:
    with open(file, "r") as f:
        data = json.load(f)
    total_score = 0
    for answer_dict in data:
        total_score += answer_dict["score"]
    print(f"总分: {total_score}")
