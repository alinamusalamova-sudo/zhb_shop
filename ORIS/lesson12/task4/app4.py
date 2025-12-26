from flask import Flask, render_template, request

app = Flask(__name__)


@app.get("/")
def index():
    return '''
    <h1> Привет! </h1>
    <p><a href = "/calc"> Использовать калькулькатор! </a></p>
    '''


@app.get("/calc")
def calculator():
    a = request.args.get("a", type=float)
    b = request.args.get("b", type=float)
    op = request.args.get("op")

    result = None
    error = None

    if a is not None and b is not None and op:
        if op == "+":
            result = a + b
        elif op == "-":
            result = a - b
        elif op == "*":
            result = a * b
        elif op == "/":
            if b == 0:
                error = "Ошибка: деление на ноль!"
            else:
                result = a / b

    return render_template("calc.html", result=result, error=error, a=a, b=b, op=op)


if __name__ == "__main__":
    app.run(debug=True)