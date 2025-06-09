from chat import create_chat_completion
import os

messages = [
    {"role": "system", "content": "You are a helpful assistant that translates English to French."},
    {"role": "user", "content": "Translate the following English text to French: 'Hello, how are you?'"},
]

model = "gpt-4o"
api_key = os.getenv("OPENAI_API_KEY")
api_base = "https://api.bltcy.ai"

response = create_chat_completion(system_prompt=messages[0]["content"], user_prompt=messages[1]["content"], model=model)
print(response)
