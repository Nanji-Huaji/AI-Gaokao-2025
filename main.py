import chat
import eval


def main(data_file: str = "dataset/2025_math_1.json", model: str = "o4-mini", eval_model: str = "o4-mini"):
    chat.answer_json_file(data_file, model=model)
    eval.eval_json_file("results/result.json", model=eval_model)


if __name__ == "__main__":
    main()
    eval.summarize_result("results/result.json")
