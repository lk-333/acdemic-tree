from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    print(f"前端发给我的数据:{data}")
    num1 = data['num1']
    num2 = data['num2']
    sum_result = num1 + num2
    return jsonify({'sum': sum_result,'sum2':2})


if __name__ == '__main__':
    app.run(debug=True)
