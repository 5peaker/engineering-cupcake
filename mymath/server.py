from flask import Flask, request, render_template
@app.route("/")

def render_index_page():
    return render_template("index.html")

app = Flask(__name__)

@app.route("/sum")
def sum_route():
    num1 = float(request.args.get("num1"))
    num2 = float(request.args.get("num2"))
    result = num1 + num2
    return str(result)

@app.route("/sub")
def sub_route():
    num1 = float(request.args.get("num1"))
    num2 = float(request.args.get("num2"))
    result = num1 - num2
    return str(result)

@app.route("/mul")
def mul_route():
    num1 = float(request.args.get("num1"))
    num2 = float(request.args.get("num2"))
    result = num1 * num2
    return str(result)

if __name__ == "__main__":
    app.run(debug=True)