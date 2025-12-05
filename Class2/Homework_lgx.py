import os
from openai import OpenAI
import datetime
# ❌如果报错 ModuleNotFoundError，请运行下面的命令行👇
# pip install openai -i https://pypi.tuna.tsinghua.edu.cn/simple

# 💡在远程平台运行时，采用下面两行代码
api_key = os.getenv("OPENAI_API_KEY")
base_url = os.getenv("OPENAI_BASE_URL")

# 💡在本地使用自定义的服务时，采用下面两行代码
# api_key = "你的 API Key"
# base_url = "提供商指定的 Base URL"

client = OpenAI(api_key=api_key, base_url=base_url)  # 初始化 OpenAI 客户端

def res(m):
    response = client.chat.completions.create(
        model="ernie-x1.1-preview",  # 改成提供商指定的模型名称
        messages= m,
        max_tokens=1000
    )
    return response.choices[0].message.content

history = []  # 初始化对话历史记录
history_summary = [] # 初始化对话历史总结

# 循环多轮对话
while True:
    prompt = input()
    if not prompt:
        break  # 输入为空时退出

    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sys_message = {"role": "system", "content": f"现在的时间是{time}."}
    history.append({"role": "user", "content": prompt})

    messages_to_send = [sys_message] + history_summary + history
    response = res(messages_to_send)
    
    if len(history) > 11:
        dele_history = history[:11]
        sum_question = {"role": "system", "content":f"{dele_history}这是之前的对话记录，将其总结成一段话."}
        summary_response = res([sum_question])
        history_summary = [{"role": "system", "content":f"这是之前对话内容的总结，依据这些内容回答问题: {summary_response}"}]
        history = history[11:]

    history.append({"role": "assistant", "content": response})
    print(response)

