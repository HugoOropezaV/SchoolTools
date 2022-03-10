from flask import Flask, render_template, request

app = Flask(__name__)


@app.get('/')
def hello_world():
    return render_template("index.html", nombre1="nombre1")


@app.post("/mirespuesta")
def factorial():

    fact = 1
    for x in range(2,1+int(request.form.get("num"))):
        fact = fact *(x)

    return render_template("index.html", fact= fact)


if __name__ == '__main__':
    app.run()
