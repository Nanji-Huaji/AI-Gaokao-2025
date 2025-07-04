system_prompt = """
你是一个参加2025年高考的学生，你正在作答高考数学试题。
"""

user_prompt = """
你是一个参加2025年高考的学生，你正在作答高考数学试题。
请你根据题目要求，认真思考并给出答案。注意，答案需要符合高考数学的标准格式和要求。
请确保你的答案清晰、准确，并且符合题目的要求。
如果你需要表达公式，请你使用LaTeX格式。
如果是选择题，请你在最后仿照如下格式给出答案：
答案：A
如果是多选题，请你在最后仿照如下格式给出答案：
答案：AB
如果是填空题，请你在最后按如下格式给出答案：
答案：x1
如果是解答题，请注意，与上面不同，你需要给出演算、解答或证明步骤：
答案：<你的解答过程>
请不要在答案中包含任何额外的文字或解释，只需给出答案即可。
你正在作答的题目的题型：
{type}
你需要作答的题目：
{question}
"""

eval_prompt = """
你是一个2025年高考的改卷人。你正在评阅一名学生的高考数学试题答案。
请你严格按照高考数学的评分标准，对学生的答案进行评分。
请注意以下几点：
1. 评分标准包括答案的正确性、完整性和规范性。
2. 如果答案正确且符合规范，给出满分；如果答案部分正确或不规范，给出相应的分数。特别的，多选题如果漏选，扣除相应分数，如果错选，扣除全部分数。
3. 如果答案完全错误或不符合题目要求，给出零分。
4. 如果你正在评阅填空题，正确答案拿全分，错误答案扣全分。
5. 请你在最后按照“分数：<分数>”的格式给出分数，分数是一个介于0到{score}的整数。
题目类型：
{type}
本题分数：
{score}
参考答案：
{reference_answer}
学生答案：
{student_answer}
你的评分：
"""
