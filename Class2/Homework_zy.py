import os
from openai import OpenAI
import tiktoken

'''
对于与AI聊天上下文过长问题的一种解决思路
'''

# 以在远程平台运行为例
api_key = os.getenv("OPENAI_API_KEY")
base_url = os.getenv("OPENAI_BASE_URL")

client = OpenAI(api_key=api_key, base_url=base_url)

counter = tiktoken.get_encoding("gpt2")
MAX_TOKEN = 2000

def count(history):
    total_tokens = 0
    for his in history:
        total_tokens += len(counter.encode(his["role"]))
        total_tokens += len(counter.encode(his["content"]))
    return total_tokens


def ask(prompt, history):
    history.append({"role": "user", "content": prompt})

    response = client.chat.completions.create(
        model="ernie-x1.1-preview",
        messages=history,
        max_tokens=1000
    )

    ans = response.choices[0].message.content
    history.append({"role": "assistant", "content": ans})
    return ans


def main():
    history = []

    while True:
        prompt = input()
        if not prompt:
            break  # 输入为空时退出

        answer = ask(prompt, history)
        print(answer)

        if count(history) >= MAX_TOKEN - 200:
            prompt = "请总结一下上文的聊天内容，保留关键信息"
            answer = ask(prompt, history)
            print("为防止聊天记录过长，为您总结上文内容\n", answer)
            history = history[-1:]


if __name__ == '__main__':
    main()
