import ollama
import re


K = 10  # 一共测试几次
Q = "字符串 \"strawberry\" 中字母 \"r\" 出现了几次？"
A = "3"
MODEL = "qwen3:0.6b"  # 替换为实际的Ollama模型代号

SYSTEM_PROMPT = """请仔细思考问题，并将最终答案用 \\boxed{} 包裹。"""


def extract_box_answer(text: str):
    pattern = r'\\boxed\{([^}]*)\}'
    matches = re.findall(pattern, text)
    return matches[-1] if matches else None


def test_model(k: int, question: str, expected_answer: str, model: str):
    success = 0

    for i in range(k):
        print(f"=== Round {i+1}/{k} ===")

        full_prompt = f"{SYSTEM_PROMPT}\n\n问题：{question}"

        # Query the model
        response = ollama.generate(
            model=model,
            prompt=full_prompt,
            options={"temperature": 0.1}
        )

        output = response["response"]
        print(f"模型输出：{output.replace('\n', ' ')}")

        box_answer = extract_box_answer(output)
        print(f"提取的答案：{box_answer}")

        if box_answer and expected_answer in box_answer:
            print("✔ 正确")
            success += 1
        else:
            print("✘ 错误")

    print(f"\n最终准确率：{success}/{k} = {success/k:.2%}")


if __name__ == "__main__":
    test_model(K, Q, A, MODEL)
