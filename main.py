import chat
import eval
import argparse


def parse_args():
    parser = argparse.ArgumentParser(description="Process some integers.")
    parser.add_argument(
        "--data_file",
        type=str,
        default="dataset/2025_math_1.json",
        help="Path to the input JSON file",
    )
    parser.add_argument(
        "--model",
        type=str,
        default="gemini-2.5-pro",
        help="Model to use for answering questions",
    )
    parser.add_argument(
        "--eval_model",
        type=str,
        default="o4-mini",
        help="Model to use for evaluation",
    )
    return parser.parse_args()


args = parse_args()


def main(data_file: str = args.data_file, model: str = args.model, eval_model: str = args.eval_model) -> str:
    file_name = chat.answer_json_file(data_file, model=model)
    eval.eval_json_file(file_name, model=eval_model)
    return file_name


if __name__ == "__main__":
    file_name = main()
    eval.summarize_result(file_name)
