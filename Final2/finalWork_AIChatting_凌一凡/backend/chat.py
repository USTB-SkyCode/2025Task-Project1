import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import re
import json, pickle
from copy import deepcopy
import ollama
from ollama import embed
import numpy as np
# from sklearn.metrics.pairwise import cosine_similarity
# from prompts import prompts, summary_prompt
from backend.prompts import prompts, summary_prompt

messages_history = []
root = os.path.dirname(__file__)
history_path = os.path.join(root, 'history.pkl')
history_dir = os.path.join(root, 'histories')

# === 聊天函数 ===

def generate_once(model:str = 'qwen3:4b'):
    response = ollama.generate(
        model = model,
        prompt= '帮我写一段rap歌词，主题是方便面，写4个bar',
        options={
            # "temperature":0.7,
            "temperature":1.0,
            # "temperature":2,
            # 'num_ctx': 10,
            'top_k': 50,
            'top_9': 0.9,
            # 'seed': 42,
        }
        )

    print(response['response'])


def chat(model="qwen3:4b"):
    # embeddings = []
    default_messages = [
        # {'role': 'system', 'content': prompts['safety']},
        {'role': 'system', 'content': prompts['short']},
    ]
    messages = [*default_messages]
    
    while True:
        user_input = input('Chat with history: ')
        if user_input == 'end':
            return
        user_input = opt_truncate_content(user_input, 500)  # 内容截断
        print(user_input)
        messages += [{'role': 'user', 'content': user_input}]
        # 将新消息添加到消息列表
        response = ollama.chat(
            model = model,
            messages = messages,
        )
        # 更新消息列表以维持上下文
        reply = response.message.content
        print(reply)
        reply = opt_truncate_content(reply, 1000)  # 内容截断
        messages += [ {'role': 'assistant', 'content': reply} ]
        print(reply + '\n')

        # 更新embedding（暂时不用）
        # embed_resp = ollama.embed(model=model, input=reply)
        # embeddings.append(embed_resp["embeddings"][0])

        # 上下文压缩策略（内容截断、语义压缩、上文总结）
        messages = opt_summary_memory(messages)


def chat_once_with_frontend(id, user_input, model="qwen3:4b"):
    # 加载历史上下文
    # messages = pickle.load(open(history_path, 'rb'))
    messages = load_history(id)

    user_input = opt_truncate_content(user_input, 500)  # 内容截断
    print(user_input)
    messages += [{'role': 'user', 'content': user_input}]
    # 将新消息添加到消息列表
    response = ollama.chat(
        model = model,
        messages = messages,
    )
    # 更新消息列表以维持上下文
    reply = response.message.content
    reply = opt_truncate_content(reply, 1000)  # 内容截断
    messages += [ {'role': 'assistant', 'content': reply} ]

    # 上下文压缩策略（内容截断、语义压缩、上文总结）
    messages = opt_summary_memory(messages, target_size=10)

    # 保存新上下文
    # pickle.dump(messages,open(history_path, 'wb'))
    save_history(id, messages)
    return reply    

# == 聊天记录处理函数 ==

def create_history(id):
    # 校验id是否已经存在
    id_list = [x.split('.')[0] for x in os.listdir(history_dir)]
    if str(id) in id_list:
        return
    # 创建新文件
    messages = init_messages()
    file_path = os.path.join(history_dir,f"{id}.pkl")
    pickle.dump(messages, open(file_path, 'wb'))
    return messages


def load_history(id):
    file_path = os.path.join(history_dir,f"{id}.pkl")
    return pickle.load(open(file_path,'rb'))

def save_history(id, messages):
    file_path = os.path.join(history_dir,f"{id}.pkl")
    return pickle.dump(messages, open(file_path,'wb'))

def load_all_id_list():
    return [x.split('.')[0] for x in os.listdir(history_dir)]

# == 上下文优化相关函数 ==
def init_messages():
    default_messages = [
        # {'role': 'system', 'content': prompts['safety']},
        {'role': 'system', 'content': prompts['short']},
    ]
    return default_messages


def extract_system_prompt(messages):
    return [m for m in messages if m['role'] == 'system'], [m for m in messages if m['role'] != 'system']

def format_messages(messages):
    return '\n'.join([f"{m['role']}: {m['content']}" for m in messages])

def opt_sliding_window(messages: list[dict], window_size: int = 10):
    if len(messages) >= window_size * 2:
        msg_system, msg = extract_system_prompt(messages)
        return msg_system + msg[-window_size:]
    return messages


def opt_truncate_content(content: str, max_tokens=500, ellipsis="..."):
    """
    单条输入/输出过长则将其截断至指定长度
    为啥要ellipsis?
    """
    max_chars = max_tokens * 4
    if len(content) > max_chars:
        return content[:max_tokens] + ellipsis
    return content


def opt_sematic_compress(messages: list[dict], embeddings: list, target_size=5):
    """
    通过ollama.embed计算消息的相似度，取其中最高的n个
    """
    if len(messages) <= target_size * 2:
        return deepcopy(messages)
    
    embeddings_array = np.array(embeddings)
    latest_embedding = embeddings_array[-1].reshape(1, -1)
    
    similarities = cosine_similarity(latest_embedding, embeddings_array)[0]
    top_indices = similarities.argsort()[-target_size:][::-1]
    top_indices.sort()

    # 貌似也应该更新embedding的列表了, 一并返回吧
    return [messages[i] for i in top_indices], [embeddings[i] for i in top_indices]


def opt_summary_memory(messages: list[dict], model="qwen3:4b", target_size=10): 
    if len(messages) <= target_size * 2:
        return deepcopy(messages)
    response = chat(
        model=model,
        messages= messages + [{"role": "user", "content": summary_prompt.format(format_messages(messages))}]
    )
    new_summary = response["message"]["content"]
    msg_system, msg = extract_system_prompt(messages)
    new_messages = msg_system + [{"role": "system", "content": f"对话摘要: {new_summary}"}] + msg[-2:]
    return new_messages


if __name__ == '__main__':
    chat()
    # create_history(12356)
    # print(pickle.load(open(history_dir + './12356.pkl', 'rb')))