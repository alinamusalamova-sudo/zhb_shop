from flask import Flask, render_template, request

app = Flask(__name__)


@app.get("/")
def index():
    return '''
    <h1> Привет! </h1>
    <p><a href = "/convert"> Перевести температуру </a></p>
    '''


@app.get("/convert")
def converter():
    value = request.args.get("value", type=float)
    direction = request.args.get("direction")
    result = None
    if value is not None and direction:
        if direction == "c_to_f":
            result = value * 9 / 5 + 32
            unit_from = "°C"
            unit_to = "°F"
        elif direction == "f_to_c":
            result = (value - 32) * 5 / 9
            unit_from = "°F"
            unit_to = "°C"
        else:
            result = None
            unit_from = unit_to = ""
    else:
        unit_from = unit_to = ""

    return render_template(
        "convert.html",
        result=result,
        value=value,
        direction=direction,
        unit_from=unit_from,
        unit_to=unit_to
    )

if __name__ == "__main__":
    app.run(debug=True)