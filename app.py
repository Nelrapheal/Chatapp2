from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    exp = data.get("expression", "")

    try:
        result = eval(exp)
        return jsonify({"result": result})
    except:
        return jsonify({"result": "error"})

if __name__ == "__main__":
    app.run(debug=True)
