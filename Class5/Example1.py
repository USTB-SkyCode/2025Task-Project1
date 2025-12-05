import ollama

r = ollama.generate(
    model='qwen3:0.6b',  # 替换为实际的Ollama模型代号
    prompt='给我一句励志的话',
    options={
        'temperature': 1.2,
        'top_k': 50,
        'top_p': 0.9,
    }
)

print(r['response'])
