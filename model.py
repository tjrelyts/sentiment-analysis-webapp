# Tyler Santosuosso
# Machine Learning Final Project
# 12/15/2023

# import re
import pandas as pd
# import nltk
from nltk.corpus import stopwords
# from tqdm import tqdm
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

'''
def preprocess_data(text):
    text = text.lower()
    
    text = re.sub(r'@[A-Za-z0-9_]+', 'USER', text) # Replaces user @ with USER 
    text = re.sub(r'http\S+|www\S+|https\S+|#|[^\w\s.,;:!?]', '', text) # Removes links, and all non alphanumeric, while maintaining punctuation

    words = nltk.word_tokenize(text)

    # Removes common English stopwords 
    stop_words = set(stopwords.words("english"))
    words = [word for word in words if word not in stop_words]

    preprocessed_text = " ".join(words)

    return preprocessed_text
'''

df = pd.read_csv("data.csv")
# df = df.dropna(subset=['text']) # Use when loading processed dataset
 
''' # Preprocessing loop (implements loading bar)
tqdm.pandas(desc="Preprocessing")
for index, row in tqdm(df.iterrows(), total=len(df), desc="Processing rows"):
    df.at[index, 'text'] = preprocess_data(row['text'])
'''

# df.to_csv("processed_data.csv", index=False)

vectorizer = CountVectorizer()
text_data = vectorizer.fit_transform(df['text'])
labels = df['target']

# Generates from same seed (80-20 ratio)
X_train, X_test, y_train, y_test = train_test_split(text_data, labels, test_size=0.2, random_state=42)

model = MultinomialNB()
model.fit(X_train, y_train)
#y_pred = model.predict(X_test)

#accuracy = accuracy_score(y_test, y_pred)
#report = classification_report(y_test, y_pred)

#print("Accuracy: ", accuracy)
#print("Classification Report:\n", report)

# Visualization of true positives and negatives versus false positives and negatives
#conf_mat = confusion_matrix(y_test, y_pred)
#sns.heatmap(conf_mat, annot=True, fmt='d', cmap='Blues', xticklabels=['Negative', 'Positive'], yticklabels=['Negative', 'Positive'])
#plt.xlabel('Predicted')
#plt.ylabel('Actual')
##plt.title('Confusion Matrix')
#plt.show()

def analyze(msg):
    text_vec = vectorizer.transform([msg])
    label_pred = model.predict(text_vec)
    if label_pred[0] == 0:
        return "Negative"
    elif label_pred[0] == 4:
        return "Positive"

'''
while True:
    text = [input("Enter: ")]
    text_vec = vectorizer.transform(text)
    label_pred = model.predict(text_vec)

    if label_pred[0] == 0:
        print("Sentiment: Negative")
    elif label_pred[0] == 4:
        print("Sentiment: Positive")
'''
