from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def calculator():
    result = None
    num1 = ""
    num2 = ""

    if request.method == 'POST':
        num1 = request.form.get('num1', '')
        num2 = request.form.get('num2', '')
        operation = request.form.get('operation')

        try:
            a = float(num1)
            b = float(num2)
        except ValueError:
            result = 'Please enter valid numbers.'
            return render_template('task.html', result=result, num1=num1, num2=num2)

        if operation == '+':
            result = a + b
        elif operation == '-':
            result = a - b
        elif operation == '*':
            result = a * b
        elif operation == '/':
            if b == 0:
                result = 'Cannot divide by zero.'
            else:
                result = a / b
        else:
            result = 'Invalid operation.'

    return render_template('task.html', result=result, num1=num1, num2=num2)


if __name__ == '__main__':
    app.run(debug=True)
