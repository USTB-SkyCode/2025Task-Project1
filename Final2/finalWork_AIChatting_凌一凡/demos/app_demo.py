from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/execute', methods=['POST'])
def execute():
    code = request.form['code']
    try:
        exec_globals = {}
        exec(code, exec_globals)
        result = exec_globals.get('result', 'Noresult found')
    except Exception as e:
        result = str(e)
    return render_template('index.html', result = result)

if __name__ == '__main__':
    app.run(debug=True)