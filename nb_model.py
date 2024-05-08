import pandas, sys, numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

import pickle

def accuracy(y_true, y_pred):
    accuracy = np.sum(y_true == y_pred) / len(y_true)
    return accuracy

training_df = pandas.read_csv(sys.argv[1])
training_df.dropna(subset=["content"], inplace=True)
training_data = training_df.to_numpy()

validation_df = pandas.read_csv(sys.argv[2])
validation_df.dropna(subset=["content"], inplace=True)
validation_data = validation_df.to_numpy()

X_train = training_data[:, 1]
y_train = training_data[:, 0].astype(int)

X_test = validation_data[:, 1]
y_test = validation_data[:, 0].astype(int)

vectorizer = CountVectorizer()
X_train = vectorizer.fit_transform(X_train)
X_test = vectorizer.transform(X_test) 

model = MultinomialNB()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
acc = accuracy(y_test, y_pred)
print("Accuracy:", acc)

with open('./data/model.pkl', 'wb') as f:
    pickle.dump(model, f)

with open('./data/vectorizer.pkl', 'wb') as f:
    pickle.dump(vectorizer, f)
