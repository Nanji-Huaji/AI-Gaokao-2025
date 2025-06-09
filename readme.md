# 2025 年高考（AI版）

## 简介

本仓库的代码能够接收高考数学题目，让  AI 进行解答，并支持对这些答案进行自动评分。

## 项目结构

```
├── chat.py           # AI对话及答题核心功能
├── config.json       # 模型配置信息
├── eval.py           # 答案评分系统
├── main.py           # 主程序入口
├── prompt.py         # 系统及用户提示词模板
├── test.py           # 测试脚本
├── dataset/          # 数据集目录
│   ├── 2025_math_1.json  # 2025年高考数学试题集
│   └── image/        # 题目相关图片
└── results/          # 结果输出目录
    └── result.json   # 模型回答结果
```

## 使用方法

### 环境准备

1. 确保已安装Python 3.7+
2. 安装所需依赖包

```bash
pip install openai backoff
```

3. 配置API密钥（使用环境变量）

```bash
export OPENAI_API_KEY="your_api_key_here"
```

### 使用

运行`main.py`

## 模型配置

可在`config.json`中进行设置模型，我们默认提供了这些模型（假设使用的都是一个API_KEY，你可能需要适当修改代码以使用来自不同API_BASE的模型，我还没跑DeepSeek）：

- **o3**
- **o3-mini**
- **o4-mini**
- **gpt-4o**
- **deepseek-r1**

## 自定义题目

可通过创建符合特定JSON格式的题目文件扩展题库：

```json
[
  {
    "index": 1,
    "content": "题目内容...",
    "type": "选择题|多选题|填空题|解答题",
    "answer": "参考答案",
    "score": 5,
    "img_file": "image/question_x_figure.png"  // 可选
  },
  ...
]
```
