from flask import Flask, render_template, redirect, request, url_for

app = Flask(__name__)


@app.route('/')
def home():
    return "<h1>I am arjit tripathi:....</h1>"


@app.route('/welcome')
def welcome():
    return "<h1>Welcome to Flask Training</h1>"


@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/success/<int:a>')
def success(a):
    return "the person is pass and the score is " + str(a)


@app.route('/fail/<int:a>')
def fail(a):
    return "the person is fail and he need to study more " + str(a)


@app.route('/calculate', methods=['GET', 'POST'])
def calculate():
    if request.method == 'GET':
        return render_template('calculate.html')

    maths = float(request.form['maths'])
    science = float(request.form['science'])
    ai = float(request.form['ai'])
    avg = (maths + science + ai) / 3

    if avg >= 80:
        result = 'success'
    else:
        result = 'fail'

    return f"Average marks: {avg} <br> Result: {result}"


if __name__ == '__main__':
    app.run(debug=True)