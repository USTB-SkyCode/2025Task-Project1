import os
from openai import OpenAI

api_key = os.getenv("OPENAI_API_KEY")
base_url = os.getenv("OPENAI_BASE_URL")

client = OpenAI(api_key=api_key, base_url=base_url)

history = [];maxn = 10;n = 0;a = 0
while n < maxn:
    prompt = input("user:")
    if not prompt:
        break
    
    n += 1
    history.append({"role": "user", "content": prompt})

    response = client.chat.completions.create(
        model="ernie-x1.1-preview",
        messages=history,
        max_tokens=1000
)
    answer = response.choices[0].message.content
    history.append({"role": "assistant", "content": answer})
    print("AI:",answer)

    if n == maxn-1:
        print("AI小助手提醒您：再进行一轮对话就达到最大次数限制啦！")
        a = int(input("若想保留上述对话内容总结，请输入1；否则请输入0："))

    if n == maxn:
        if a == 1:
            summary_prompt = "请帮我总结一下以下对话内容，要求只保留以下对话内容的关键信息：" + str(history)
            summary_response = client.chat.completions.create(  
                model="ernie-x1.1-preview",
                messages=summary_prompt
                max_tokens=1000
            )
            summary = summary_response.choices[0].message.content
            history = [{"role": "system", "content": summary}]
            print("已保留上述对话内容总结，可继续对话")
        else:
            print("对话已结束")