import chat


def main(data_file: str = "dataset/test.json", model: str = "gpt-4o"):
    chat.answer_json_file(data_file, model=model)


if __name__ == "__main__":
    main()
