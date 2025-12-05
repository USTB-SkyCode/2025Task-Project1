import os
from openai import OpenAI
# ❌如果报错 ModuleNotFoundError，请运行下面的命令行👇
# pip install openai -i https://pypi.tuna.tsinghua.edu.cn/simple

# 💡在远程平台运行时，采用下面两行代码
api_key = os.getenv("OPENAI_API_KEY")
base_url = os.getenv("OPENAI_BASE_URL")

# 💡在本地使用自定义的服务时，采用下面两行代码
# api_key = "你的 API Key"
# base_url = "提供商指定的 Base URL"

client = OpenAI(api_key=api_key, base_url=base_url)  # 初始化 OpenAI 客户端

history = []  # 初始化对话历史记录

num = 0 # 初始化对话次数

# 循环多轮对话
while True:
    if num < 10 :
        prompt = input()
        if not prompt:
            break  # 输入为空时退出
    else:
        prompt = '因为对话内容过多，我们准备清空对话历史，请你总结以上对话内容，以便继续为我答疑解惑，请总结后严格回复：我已总结完成，请继续输入'
        history = []
        num = 0
    history.append({"role": "user", "content": prompt})

    response = client.chat.completions.create(
        model="ernie-x1.1-preview",  # 改成提供商指定的模型名称
        messages=history,
        max_tokens=1000
    )

    num += num

    answer = response.choices[0].message.content
    history.append({"role": "assistant", "content": answer})
    print(answer)