# import json
from flask import Flask, render_template, request
from backend.chat import chat_once_with_frontend, load_history, create_history, load_all_id_list

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


# @app.route('/execute', methods=['POST'])
# def execute():
#     code = request.form['code']
#     try:
#         exec_globals = {}
#         exec(code, exec_globals)
#         result = exec_globals.get('result', 'No result found')
#     except Exception as e:
#         result = str(e)
#     return render_template('index.html', result = result)


@app.route('/getAnswer', methods=['GET', 'POST'])
def get_answer():
    # 获取ajax请求的参数
    id = request.args.get("id","")
    msg = request.args.get("msg","")
    # 输入模型
    result = chat_once_with_frontend(id, msg)
    # 返回结果
    return {
        "reply": result,
        "success": 0,
    }


@app.route('/loadHistory', methods=['GET', 'POST'])
def load_chat_history():
    # history = json.dumps(history)
    # print(history)
    history_id = request.args.get("id","")
    history = load_history(history_id)
    print('loading history id:', history_id)
    return {
        # "history": json.dumps(history),
        # "history": str(history),
        "history": history,
        "success": 0,
    }


@app.route('/createNewChat', methods=['GET', 'POST'])
def create_new_chat():
    history_id = request.args.get("id","")
    history = create_history(id=history_id)
    print('loading history id:', history_id)
    return {
        "history": history,
        "success": 0,
    }


@app.route('/loadAllID', methods=['GET', 'POST'])
def load_all_id():
    return {
        "ids": load_all_id_list(),
        "success": 0,
    }



if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host='0.0.0.0', port=80, debug=True)
