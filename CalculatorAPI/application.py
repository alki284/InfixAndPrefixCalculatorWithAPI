from flask import Flask, request, render_template, jsonify

# Declares flask and location of HTML template.
app = Flask(__name__, template_folder="templates")

# Return HTML file
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/process", methods=["POST"])
def process():
    # Get ops from index.html
    ops = request.form["ops"]
    stack = []
    ops = ops.split(" ")

    # Go through the string.
    while len(ops) > 0:
        i = ops.pop(0)

        if i.isdigit():
            stack.append(int(i))

        else:
            # Digits should be only multi char string, so anything else is incorrect.
            if len(i) > 1:
                return jsonify({"output": "Incorrect Format"})

            elif i in ["+", "-", "*", "/"]:
                stack.append(i)

            # Reaching ')' means end of an operation so needs to be calculated.
            elif i == ")":
                try:
                    digit2 = stack.pop()
                    op = stack.pop()
                    digit1 = stack.pop()
                except IndexError:
                    return jsonify({"output": "Incorrect Format"})

                if op == "+":
                    stack.append(digit1 + digit2)
                elif op == "-":
                    stack.append(digit1 - digit2)
                elif op == "*":
                    stack.append(digit1 * digit2)
                elif op == "/":
                    stack.append(digit1 / digit2)

    # Return the result in json format.
    output = str(stack.pop())
    return jsonify({"output": "The result of your calculation is: " + output})
