from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # 允许跨域请求

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message', '')
    
    # 在这里处理用户消息，调用你的AI模型
    # 这里只是一个简单示例
    ai_reply = process_message(user_message)
    
    return jsonify({'reply': ai_reply})

def process_message(message):
    # 这里实现你的AI逻辑
    # 可以是调用预训练模型、API或其他处理方式
    if '你好' in message:
        return '你好！很高兴为你服务。'
    elif '名字' in message:
        return '我是AI助手，专门为你提供帮助。'
    else:
        return f'我收到了你的消息："{message}"。这是一个示例回复，实际应用中我会提供更有意义的回答。'

if __name__ == '__main__':
    app.run(debug=True, port=5000)