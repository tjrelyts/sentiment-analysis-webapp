from flask import Flask, render_template, request
from model import analyze

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        msg = request.form.get('msg')
        print(analyze(msg))
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True, port=8000)