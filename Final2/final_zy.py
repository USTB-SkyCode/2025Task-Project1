import datetime
import requests             # 爬虫基础库，经典永流传
from openai import OpenAI
import tiktoken

"""
课题一：在原先的AI聊天和历史总结中加入了查询天气、日期、历史记录功能
"""

# 天气系统用的高德
# ⭐不想花钱申请ds的key了，请装作他有，thanks！

try:
    from config import DEEPSEEK_API_KEY, AMAP_WEATHER_KEY, BASE_URL
except ImportError:
    DEEPSEEK_API_KEY = ""
    AMAP_WEATHER_KEY = ""
    BASE_URL = ""
    print("⚠️ 未检测到config.py配置文件，请在本地创建该文件并填入API Key！")

client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url=BASE_URL)
counter = tiktoken.get_encoding("gpt2")
MAX_TOKENS = 2000


def query_weather(city):
    if not AMAP_WEATHER_KEY or AMAP_WEATHER_KEY == "替换成你的高德天气API Key":
        return "❌ 请先配置高德天气API Key"

    # 高德天气API地址（city参数传城市名/城市编码）
    url = f"https://restapi.amap.com/v3/weather/weatherInfo?city={city}&key={AMAP_WEATHER_KEY}&extensions=base"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()     # 请求出问题的话这一步会直接抛出异常
        data = response.json()

        if data["status"] != "1":
            return f"❌ 天气查询失败：{data.get('info', '未知错误')}"

        # 提取天气数据
        live_weather = data["lives"][0]
        return (
            f"🌤️ {live_weather['city']} 实时天气\n"
            f"天气：{live_weather['weather']}\n"
            f"温度：{live_weather['temperature']}℃\n"
            f"风向：{live_weather['winddirection']} {live_weather['windpower']}级\n"
            f"湿度：{live_weather['humidity']}%"
        )
    except Exception as e:
        return f"❌ 天气查询失败：{str(e)}"


def get_current_time():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# 这一步AI给的做法是直接用request库进行post请求，跳过Openai，但是有点麻烦，借用前两节课的代码了
# ps：这么写的话就少了不少东西，当然了，捕获异常少了不少，稳定性估计下降了
def ask(history):
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=history,
            max_tokens=1000
        )
        ai_reply = response.choices[0].message.content

        history.append({"role": "AI", "content": ai_reply})
        return ai_reply
    except Exception as e:
        return f"❌ AI请求失败：{str(e)}"

def count(history):
    total_tokens = 0
    for his in history:
        total_tokens += len(counter.encode(his["role"]))
        total_tokens += len(counter.encode(his["content"]))
    return total_tokens


def main():
    # 欢迎语：要钱，少聊。。。
    print("\n" + "=" * 40)
    print("🎯 Python命令行聊天系统（最终版）")
    print("💡 支持功能：")
    print("   - 输入任意内容：和AI聊天（对接DeepSeek）")
    print("   - 查时间：查看当前系统时间")
    print("   - 查历史：查看所有聊天记录，有部分被AI总结缩减了")
    print("   - 查天气 城市名：查询指定城市天气（例：查天气 北京）")
    print("   - 退出：关闭聊天系统")
    print("=" * 40 + "\n")

    history = []

    while True:
        user_input = input("🧑 你：").strip()

        if user_input.lower() in ["退出", "exit", "quit"]:
            print("🤖 AI：再见啦～下次再聊！")
            break

        if not user_input:
            print("🤖 AI：请输入有效内容哦～")
            continue

        history.append({"role": "user", "content": user_input})

        if user_input == "查时间":
            current_time = get_current_time()
            ai_reply = f"⏰ 当前时间：{current_time}"
            history.append({"role": "AI", "content": ai_reply})

        elif user_input == "查历史":
            if not history:
                ai_reply = "📜 暂无聊天历史记录～"
            else:
                ai_reply = "\n📜 聊天历史记录（最新在前）：\n" + "-" * 30
                for idx, msg in enumerate(reversed(history), 1):  # 倒序显示（最新在前）
                    role = "你" if msg["role"] == "user" else "AI"
                    ai_reply += f"\n{idx}. {role}：{msg['content']}\n" + "-" * 30
                history.append({"role": "AI", "content": "历史记录略"})


        elif user_input.startswith("查天气"):
            city = user_input.replace("查天气", "").strip()
            if not city:
                ai_reply = "❌ 天气查询格式错误：请输入「查天气 城市名」（例：查天气 上海）"
            else:
                ai_reply = query_weather(city)
                history.append({"role": "AI", "content": ai_reply})

        else:
            ai_reply = ask(history)

        print(f"🤖 AI：{ai_reply}\n")

        if count(history) >= MAX_TOKENS - 200:
            history.append({"role": "user", "content": "请总结一下上文的聊天内容，保留关键信息"})
            answer = ask(history)
            print("为防止聊天记录过长，为您总结上文内容\n", answer)
            history = history[-2:]


if __name__ == '__main__':
    main()

"""
写在后面的几句闲言碎语：
理论上直接用Exception捕获异常有点拉，但是基于没有key没跑整个程序和某些人类根源的基因这两条原因，就先这么放着了。
什么？你问没有跑怎么知道没问题？
AI is all you need. That's my answer [手动滑稽]

确实要说这一部分AI提出了很多指导性意见，不过AI的某些思路还是略微有些超前或者麻烦一点的，比如请求部分和数据收集的部分
未来可以考虑试着用AI的post请求和SQlite数据库处理，甚至可以试着来一个前端界面，利用html+css或者直接用pygame之类的库内部实现
至于进一步利用request库和爬虫采集数据的部分，那就是另一场激动人心的冒险了（ps：其实比较占时间，构思程序和运行程序都是）

总而言之，这次就先这样吧，也是废了很多功夫
"""
