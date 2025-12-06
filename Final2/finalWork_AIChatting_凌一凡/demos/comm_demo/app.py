from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


# 以下是我加的
@app.route('/getAnswer', methods=['GET', 'POST'])
def get_answer():
    # 获取ajax请求的参数
    data = request.args
    print(data)
    name = data.get("name","not found")
    return {
        "data": f'please remember {name} forever',
        "success": 0,
    }


if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=5000, debug=True)
    app.run(host='0.0.0.0', port=80, debug=True)