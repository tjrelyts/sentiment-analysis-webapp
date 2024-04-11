from flask import Flask, render_template, request
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import pickle

app = Flask(__name__)

with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

with open('vectorizer.pkl', 'rb') as f:
    vectorizer = pickle.load(f)

def analyze(str):
    vec = vectorizer.transform(str)
    y_pred = model.predict(vec)

    if y_pred[0] == 2:
        print("Sentiment: Negative")
    elif y_pred[0] == 1:
        print("Sentiment: Positive")
    else:
        print("Sentiment: Neutral")

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        msg = request.form.get('msg')
        analyze([msg])
    return render_template("base.html")

if __name__ == '__main__':
    app.run(debug=True, port=8000)