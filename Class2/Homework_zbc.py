import os
from openai import OpenAI
from datetime import datetime

# 从环境变量读取 DeepSeek API Key
api_key = os.getenv('DEEPSEEK_API_KEY')
if not api_key:
    print("❌ 错误：请设置 DEEPSEEK_API_KEY 环境变量")
    exit(1)

# 创建 DeepSeek 客户端
client = OpenAI(
    api_key=api_key,
    base_url="https://api.deepseek.com"
)

def get_current_time():
    """获取当前时间并格式化成中文"""
    now = datetime.now()
    return now.strftime("%Y年%m月%d日 %p%I:%M")

def get_weekday():
    """获取星期几"""
    weekday = datetime.now().strftime("%A")
    weekdays_cn = {
        "Monday": "星期一", "Tuesday": "星期二", "Wednesday": "星期三",
        "Thursday": "星期四", "Friday": "星期五", 
        "Saturday": "星期六", "Sunday": "星期日"
    }
    return weekdays_cn.get(weekday, weekday)

def time_assistant(user_query):
    """AI时间助手核心函数"""
    # 获取当前时间信息
    current_time = get_current_time()
    current_weekday = get_weekday()
    current_year = datetime.now().strftime("%Y年")
    
    # 构建给AI的"秘密信息"
    system_prompt = f"""
    你是一个智能时间助手，专门回答与时间、日期相关的问题。
    
    【当前时间信息】
    - 当前时间：{current_time}
    - 今天星期：{current_weekday}
    - 当前年份：{current_year}
    
    回答要求：
    1. 当用户询问时间、日期、星期、年份时，请根据上面的时间信息回答
    2. 回答要自然、友好，就像你真的知道时间一样
    3. 不要提及"系统时间"、"秘密信息"等词语
    4. 如果问题与时间无关，请礼貌地引导用户询问时间相关问题
    5. 可以用一些有趣的方式回答，比如"现在是下午茶时间哦！"
    """
    
    try:
        # 调用 DeepSeek API
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_query}
            ],
            temperature=0.7  # 控制创造性，0-1之间
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        return f"抱歉，我暂时无法回答：{str(e)}"

def main():
    """主程序"""
    print("=" * 50)
    print("🤖 AI时间助手已启动！")
    print("我可以告诉你时间、日期、星期等信息")
    print("输入 '退出' 或 'quit' 结束程序")
    print("=" * 50)
    
    while True:
        # 获取用户输入
        user_input = input("\n👤 你: ").strip()
        
        # 退出条件
        if user_input.lower() in ['退出', 'quit', 'exit', 'bye']:
            print("🤖 助手: 再见！欢迎下次使用～")
            break
            
        if not user_input:
            continue
            
        # 获取AI回复
        print("⏳ 思考中...", end="")
        answer = time_assistant(user_input)
        print("\r🤖 助手:", answer)

# 如果是直接运行这个文件，启动助手
if __name__ == "__main__":
    main()